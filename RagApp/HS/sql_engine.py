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


from dotenv import load_dotenv
load_dotenv()


embeddings = OpenAIEmbeddings()


class Commaseperatedoutput(BaseOutputParser):
    def parse(self, text:str):
        return text.strip().split(",")


def get_sql_chain(db):
    template = """
        You are a data analyst at a data company, You are interacting with a user who is asking you questions about the company's database.
        Based on the table schema below, write a SQL query that would answer the users's question and give the user the answer to the question he or she has asked, Take the conversation history into account.
        You do not have to show the SQL query you ran to get the response


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
    llm = ChatGroq(model="Llama3-70b-8192", temperature=0,  groq_api_key="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")


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

    return chain.invoke({
        "question": user_question,
        "chat_history": chat_history,
    })





def init_database(user:str, password:str, host:str, port:str, database:str) -> SQLDatabase:
    db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)

