from fastapi import APIRouter, Depends, HTTPException, status
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent
from langchain import SerpAPIWrapper
from langchain.tools import BaseTool
import os

# *************************************************Imports*********************************************************************************************************

os.environ['GROQ_API_KEY'] = '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'
os.environ['SERPAPI_API_KEY'] = "06686a17c95e60077066dd48fea5971302ef8ceae9e1008b7fe7d46fcf38f289"

# *************************************************APi-Keys*********************************************************************************************************

dummy_router = APIRouter()
agent_instructions = "Reply to queries based only on encryption and decryption algorithms like, AES,DES,RSA,ECC. Do not deviate from these topics"
search = SerpAPIWrapper()

llm = ChatGroq(
            # model="llama3-70b-8192",
            # model="llama3-8b-8192",
            model="mixtral-8x7b-32768",
            max_tokens = 100,
)

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


all_tools = [googleQuery()]

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

@dummy_router.post("/post-query/{query}")
async def psotQuery(query: str):


    returnResult = agent.run(query)
    print(returnResult)

    return {
        "user":query, 
        "Chatbot" : returnResult ,

    }



