import langchain
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredExcelLoader
from langchain.document_loaders.csv_loader import CSVLoader # this will come later
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from .models import DocumentUpload
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import PyPDFLoader
load_dotenv() 


# the code to load and embed text files into the databae and
#prepare for querying
embeddings = OpenAIEmbeddings()


 

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


#vector embedding and vectorstore(Pinecone)

def get_embeddings(docs):
    """
    Retrieves embeddings for a list of documents.

    Args:
        docs (list): A list of documents.

    Returns:
        PineconeVectorStore: A vector store containing the embeddings of the documents.
    """
    Pinecone(
        api_key=PINECONE_API_KEY,
    )

    vector_store = PineconeVectorStore.from_documents(
        docs,
        embedding=OpenAIEmbeddings(),
        index_name=INDEX_NAME
    )

    return vector_store








# open ai llm
def get_openai_llm():
    """
    Creates an instance of the OpenAI language model (LLM) interface.

    Returns:
        llm (ChatOpenAI): An instance of the OpenAI language model for the LLM interface.
    """
    llm = ChatOpenAI(temperature=0)

    return llm







def get_response_llm(llm, vector_store, question):
    """
    Retrieves the answer to a question using a language model and a vector store.

    Args:
        llm (LanguageModel): The language model used for retrieval.
        vector_store (VectorStore): The vector store used for retrieval.
        question (str): The question to retrieve the answer for.

    Returns:
        str: The answer to the question.
    """
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever = vector_store.as_retriever(
            search_type="mmr", search_kwargs={"k":3}
        ),
    )
    answer = chain.invoke(question)
    return answer







# Retrieval augumented generation for Docx(microsoft word files

def data_ingestion_docx(file_path:str):
    loader = Docx2txtLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    docs = text_splitter.split_documents(documents)
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

    return docs






        
        

    


