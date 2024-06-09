import langchain
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredExcelLoader
from langchain.document_loaders.csv_loader import CSVLoader # this will come later
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from .models import DocumentUpload
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, PodSpec, ServerlessSpec
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate,AIMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
# from langchain.chains.question_answering import StuffDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain # added this line and commennted the out the line above
from langchain_core.load.serializable import Serializable
import os
import pinecone
from langchain_community.document_loaders.csv_loader import CSVLoader, UnstructuredCSVLoader
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import logging
from langchain_community.utilities import SQLDatabase
from langchain_community.docstore.document import Document
from langchain_groq import ChatGroq
from langchain.output_parsers.structured import StructuredOutputParser, ResponseSchema

logging.basicConfig(level=logging.DEBUG)


load_dotenv()



# embeddings = OpenAIEmbeddings(OPENAI_API_KEY)



 #Initialize Pinecone
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')
PINECONE_INDEX_NAME = 'app5'

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("app5")

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")  # Adjust model as needed








 

 

# getting and loading the data
def data_ingestion_txt(file_path:str, encoding:str=None):
    loader = TextLoader(file_path)
    documents = loader.load()

    # splitting the data into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)


    if encoding is not None:
        docs = text_splitter.split_documents(documents, encoding='utf-8')
    else:
        docs = text_splitter.split_documents(documents)
    return docs


def get_embeddings(docs, metadata_filter=None):
    load_dotenv()
    """
    Retrieves embeddings for a list of documents.

    Args:
        docs (list): A list of documents.

    Returns:
        PineconeVectorStore: A vector store containing the embeddings of the documents.
    """
    Pinecone(
        api_key=os.environ.get('pinecone'),
    )

    if metadata_filter is not None:
        docs = [doc for doc in docs if all(doc.metadata.get(key) == value for key, value in metadata_filter.items())]

   
    

    vector_store = PineconeVectorStore.from_documents(
        docs,
        embedding=OpenAIEmbeddings(),
        index_name='app5',
    )

    return vector_store










# open ai llm
def get_openai_llm():
    """
    Creates an instance of the OpenAI language model (LLM) interface.

    Returns:
        llm (ChatOpenAI): An instance of the OpenAI language model for the LLM interface.
    """
    # llm = ChatOpenAI(temperature=0)
    llm = ChatGroq(model="Llama3-70b-8192", temperature=0, groq_api_key="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")


    return llm











def get_response_llm(llm, vector_store, question, file_id, chat_history:list, metadata_filter=None):
    """
    Retrieves the answer to a question using a language model and a vector store.

    Args:
        llm (LanguageModel): The language model used for retrieval.
        vector_store (VectorStore): The vector store used for retrieval.
        question (str): The question to retrieve the answer for.
        file_id (int): The unique file identifier.
        metadata_filter (dict, optional): Additional metadata filters.

    Returns:
        str: The answer to the question.
    """ 
    search_kwargs = {
        "k": 3,  # Increase k to return more results
        "filter": {"file_name": os.path.basename(file_id)}
    }

    response_schemas = [
        ResponseSchema(name="response", description="The formatted response", type="string")
    ]

    parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = parser.get_format_instructions()

    prompt = f"""
    you are a friendly AI assistant, users will ask questions about a file. 
    Please make sure to through the files properly to retrieve information from the file based on the users query
    for analysis tasks in csv and xlsx files you are going to make sure to analyze data properly, make sure not to show too much working in your response to avoid ambiguous response.
    Also make sure to keep the chat history in mind while reponding to the questions.
    
    Conversation History: {chat_history}
    Question: {question}
    """

    chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(search_type="similarity", search_kwargs=search_kwargs)

            )

    answer = chain.invoke({
        "query": prompt,
        "chat_history":chat_history
        })

    return answer




def format_answer(answer):
    """
    Formats the LLM response to include bullet points or other dynamic text elements.

    Args:
        answer (str): The raw answer from the LLM.

    Returns:
        str: The formatted answer.
    """
    # Simple example of formatting with bullet points
    formatted_answer = answer.replace('\n', '\n- ')
    if not formatted_answer.startswith('- '):
        formatted_answer = '- ' + formatted_answer

    return formatted_answer











# Retrieval augumented generation for Docx(microsoft word files

def data_ingestion_docx(file_path:str):
    loader = Docx2txtLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    docs = text_splitter.split_documents(documents)

    for i, doc in enumerate(docs):
        doc.metadata["file_name"] = os.path.basename(file_path)
        doc.metadata["doc_id"] = f"{file_path}_{i}"

    return docs



def data_ingestion_pdf(file_path:str):
    """
    This function takes a file path as input and performs data ingestion from a PDF file.
    
    Parameters:
    file_path (str): The path of the PDF file to be ingested.
    
    Returns:
    list: A list of pages extracted from the PDF file.
    """
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()

    for i, page in enumerate(pages):
        page.metadata["file_name"] = os.path.basename(file_path)
        page.metadata["doc_id"] = f"{file_path}_{i}"

     

    return pages



    
def data_ingestion_xlsx(file_path: str):
    """
    Loads data from an Excel file and returns a list of documents.

    Args:
        file_path (str): The path to the Excel file.

    Returns:
        List[Document]: A list of documents loaded from the Excel file.
    """
    loader = UnstructuredExcelLoader(file_path, mode="single")
    docs = loader.load()

    for i, doc in enumerate(docs):
        doc.metadata["file_name"] = os.path.basename(file_path)
        doc.metadata["doc_id"] = f"{file_path}_{i}"

    return docs






def data_ingestion_csv(file_path:str):
    loader = UnstructuredCSVLoader(file_path)
    docs = loader.load()

    for i, doc in enumerate(docs):
        doc.metadata["file_name"] = os.path.basename(file_path)
        doc.metadata["doc_id"] = f"{file_path}_{i}"

    return docs

        
        


def queryCSV(llm, question: str, file_path):
    # Query csv 
    try:
        file_path=file_path
        agent = create_csv_agent(llm=llm, path=file_path, verbose=True)
        result = agent.invoke(prompt)
        res = json.dumps(result)
        return res
    except Exception as e:
        print(e)






