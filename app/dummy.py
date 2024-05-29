from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import auth, models, schemas, security
from app.db import get_db
import json

from fastapi import FastAPI, HTTPException, UploadFile, File
from langchain_core.documents import Document

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.agents import load_tools,Tool,create_tool_calling_agent,initialize_agent
from langchain import SerpAPIWrapper
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain.tools import BaseTool

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import AgentExecutor
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.document_loaders import UnstructuredPowerPointLoader
import pandas as pd 
from psycopg2.extras import RealDictCursor
import psycopg2


import os

# *************************************************Imports*********************************************************************************************************

os.environ['GROQ_API_KEY'] = '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'
os.environ['SERPAPI_API_KEY'] = "06686a17c95e60077066dd48fea5971302ef8ceae9e1008b7fe7d46fcf38f289"

# *************************************************APi-Keys*********************************************************************************************************




dummy_router = APIRouter()
inputTokenSize = 200
agent_instructions = "Reply to queries based only on encryption and decryption algorithms like, AES,DES,RSA,ECC. Do not deviate from these topics"
search = SerpAPIWrapper()





# Creation of llm model
llm = ChatGroq(
            # model="llama3-70b-8192",
            # model="llama3-8b-8192",
            model="mixtral-8x7b-32768",
            max_tokens = 100,
)







# Tool for sql agent, to perform operation on interet usfig serp api
class googleQuery(BaseTool):
    name = "googleQuery"
    description="Performs internet-based queries using Google's search engine. Make sure you only stick to encryption and decryption related queries. If anything other than that is asked simply say I don't know. Don't try to makeup answers"
    
    def _run(self, quert: str)->str:
        result = search.run(quert)
        print(result)
        result = result
        return result

    async def _arun(self, quert: str)->str:
        raise NotImplementedError("\nnot supported\n")


# Main agent without sql agent
all_tools = [googleQuery()]

# Main agent with sql agent
# all_tools = [sqlQuery()]

# Agent initialization with tools
agent = initialize_agent(
        tools=all_tools, 
        temperature=0,
        llm=llm, 
        agent="zero-shot-react-description",
        verbose=True,
        agent_instructions=agent_instructions,
        # return_intermediate_steps=True,
        handle_parsing_errors=True,
        max_iterations=20,
        # max_execution_time=20
    )





  

# Api endpoint to ask queries for the model
@dummy_router.post("/post-query/{query}")
async def psotQuery(query: str,current_user: schemas.UserInDB = Depends(auth.get_current_user),db: Session = Depends(get_db)):


    returnResult = agent.run(query)
    print(returnResult)

    return {
        "user":query, 
        "Chatbot" : returnResult ,

    }



# Api endpount for streamlit to bypass auth
@dummy_router.post("/post-query-no-auth/{query}")
async def psotQuery(query: str,db: Session = Depends(get_db)):
    print(query)
    returnResult = agent.run(query)
    return  returnResult