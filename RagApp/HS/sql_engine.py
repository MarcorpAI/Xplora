import os
from sqlalchemy import create_engine, inspect
import pandas as pd
from langchain_community.utilities import SQLDatabase
from langchain_community.docstore.document import Document
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import OpenAIEmbeddings
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_core.output_parsers import BaseOutputParser
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool


from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

class Commaseperatedoutput(BaseOutputParser):
    def parse(self, text:str):
        return text.strip().split(",")




def init_database(user:str, password:str, host:str, port:str, database:str) -> SQLDatabase:
    db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)


def get_sql_chain(db):
    template = """
        You are a data analyst at a data company, You are interacting with a user who is asking you questions about the company's database.
        Based on the table schema below, write a SQL query that would answer the users's question and give the user the answer to the question he or she has asked, Take the conversation history into account.
        make sure for each question youre asked look at the previous question the user has asked in the chat history incase the user has asked a follow up question as regard to the previous question. 
        You do not have to show the SQL query you ran to get the response.
        before you answer any questions, think deep, think deeply 
        and take not of spacing in your response. take note of new lines and give a well structured response in your answers .
        do not give jampackked answers.
        Also note that it is important that you respond in markdown format when necessary, and ignore the hash symbols.
        Include headings with bold text when dealing with responses the requires that.
        when listing out items make sure you list each item in seperate lines to achieve a well structured answer.
        make sure you display a well structured answer for the user or the viewer to be able to understand what he or she is reading.
        Respond in Rich Text format





        <SCHEMA>{schema}<SCHEMA>

        Conversation History: {chat_history}

        write only the SQL query and nothing else. Do not wrap the SQL query in any other Text, not even backticks.

        For example:
        Question: which 3 artists have the most tracks?
        SQL Query: SELECT artists, COUNT(*) as track_count FROM track GROUP BY Artists ORDER BY track_count DESC LIMIT 3;

        Question: Name 10 artists
        SQL Query: SELECT Name FROM artist LIMIT 10;

        Your Turn:

        Question: {question}
        SQL Query:
    
        """
    prompt = ChatPromptTemplate.from_template(template)
    # llm = ChatOpenAI(temperature=0)
    llm = ChatGroq(model="Llama3-8b-8192", temperature=0,  groq_api_key=groq_api_key)


    def get_schema(_):
        return db.get_table_info()
    
    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )
    

def get_response(user_question:str, db:SQLDatabase, chat_history:list):
    sql_chain = get_sql_chain(db)

    template = """
       You are a data analyst at a company, you are interacting with a user who is asking you questions about the company's database.
       when you are asked a question give a definite answer and do not hallucinate reponses. and also repond with the answer you get from the SQL query you run
       Based on the table schema below, question, sql query and sql response, write a natural language reponse.
       You do not have to show the SQL query you ran to get the response 
       Avoid using markdown or HTML formatting in your response.
       Include headings with bold text when dealing with responses the requires that.
       when listing out items make sure you list each item in seperate lines to achieve a well structured answer.
       make sure you display a well structured answer for the user or the viewer to be able to understand what he or she is reading.
       Respond in Rich Text format


       Conversation history: {chat_history}
       SQL Query: <SQL>{query}</SQL>
       User Question: {question}
       SQL Response: {response}"""
    
    prompt = ChatPromptTemplate.from_template(template)
    # llm = ChatOpenAI(temperature=0)
    llm = ChatGroq(model="llama3-70b-8192", temperature=0, groq_api_key="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")

    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: db.get_table_info(),
            response=lambda vars: db.run(vars["query"]),
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    answer =  chain.invoke({
        "question": user_question,
        "chat_history": chat_history,
    })
    
    return str(answer)










def init_database_postgres(user:str, password:str, host:str, port:str, database:str) -> SQLDatabase:
    try:
        db_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(db_uri, poolclass=QueuePool)
        return SQLDatabase(engine)
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise


