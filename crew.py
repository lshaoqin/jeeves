from crewai import Agent, Task, Crew, Process
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    CSVSearchTool
)
from dotenv import load_dotenv
from langchain_community.llms import Ollama

# To Load Local models through Ollama
llm_model = Ollama(model="gemma:2b")

docs_tool = DirectoryReadTool(directory='documents')
file_tool = FileReadTool()
csv_tool = CSVSearchTool()

db_agent = Agent(
    role = "Database Engineer",
    goal = "Write efficient SQL queries and manage the company's PostgreSQL database",
    backstory="""
    You are a database engineer at a large company. You are responsible for managing and accessing the company's PostgreSQL database.
    """,
    tools = [docs_tool, file_tool, csv_tool],
    llm = llm_model
)

swe_agent = Agent(
    role = "Software Engineer",
    goal = "Write efficient and bug free code in Python and run SQL queries using psycopg2",
    backstory="""
    You are a software engineer tasked with writing code in Python.
    """,
    tools = [docs_tool, file_tool, csv_tool],
    llm = llm_model
)

data_agent = Agent(
    role = "Data Scientist",
    goal = "Analyse data and generate insights in a comprehensive and understandable format",
    backstory="""
    You are a data scientist at a large company. You are responsible for analysing data and presenting insights to stakeholders.
    """,
    tools = [],
    llm = llm_model
)

def python_task(task):
    return Task(
    description=f"Write Python code to aid in answering the user's question or command: {task}",
    expected_output="""Python code that performs the specified task, interacting with the database using psycopg2.
     The code should return None if no output is expected, or the output of the task if it is expected.""",
    agent=swe_agent
)

def analysis_task(data):
    return Task(
    description=f"Based on the following input: {data}, analyse the data and generate insights.",
    expected_output="""A comprehensive analysis of the data provided, including any insights or conclusions drawn from the analysis.""",
    agent=data_agent
)

if __name__ == "__main__":
    load_dotenv()

    while True:
        user_input = input("Enter your question or command: ")
        
        py_task = python_task(user_input)
        crew = Crew(agents=[db_agent, swe_agent],
                    tasks=[py_task],
                    verbose=2)
        
        result = crew.kickoff()
        print(result)

