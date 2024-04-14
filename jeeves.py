from crewai import Agent, Task, Crew, Process
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    CSVSearchTool
)
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain.agents import Tool
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_experimental.utilities import PythonREPL
from db import db_connect
from langchain_openai import ChatOpenAI
import os

db = SQLDatabase(db_connect())

llm_model = ChatOpenAI(model_name=os.getenv("OPENAI_MODEL_NAME"), temperature=0) # Ollama(model="gemma:2b")

file_tool = FileReadTool(file_path='documents/schema.txt')
csv_tool = CSVSearchTool()
sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm_model)
sql_tools = sql_toolkit.get_tools()
sql_tools.extend([file_tool, csv_tool])
python_repl = PythonREPL()
python_tool = Tool(
    name="python_repl",
    description="A Python shell. Use python_repl.run with the positional argument 'command' to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run,
)

db_agent = Agent(
    role = "Database Engineer",
    goal = "Write efficient SQL queries and manage the company's PostgreSQL database",
    backstory="""
    You are a database engineer at a large company. You are responsible for managing and accessing the company's PostgreSQL database.
    """,
    tools = sql_tools,
    llm = llm_model
)

swe_agent = Agent(
    role = "Software Engineer",
    goal = "Write efficient and bug free code in Python",
    backstory="""
    You are a software engineer at a large company. You are tasked with writing quality code in Python.
    """,
    tools = [file_tool, csv_tool],
    llm = llm_model
)

qa_agent = Agent(
    role = "Quality Assurance Engineer",
    goal = "Test the code written by the software engineer to ensure it is bug free",
    backstory="""You are a quality assurance engineer at a large company. You are tasked with testing and running the code written by the software engineer.""",
    tools = [python_tool],
    llm = llm_model
)

data_agent = Agent(
    role = "Data Scientist",
    goal = "Analyse data and generate insights in a comprehensive and understandable format",
    backstory="""
    You are a data scientist at a large company. You are responsible for analysing data and presenting insights to stakeholders.
    """,
    tools = [python_tool],
    llm = llm_model
)

def sql_task(task):
    return Task(
    description=f"""Write and run SQL queries to aid in answering the user's question or command: {task}. Details of the SQL schema can be found in the documents/schema.txt file. 
    If updates are made to the schema, the schema.txt file should be updated accordingly. If a document is needed, it can be found in the documents directory. """,
    expected_output="""The SQL query to be run.""",
    agent=db_agent
)

def run_sql_task():
    return Task(
    description="""
    Run the given SQL query using the SQLDatabaseTool.'
    To use the SQLDatabaseTool, pass the inputs as a comma-separated list. Do not use any keyword arguments.""",
    expected_output="""The output of the SQL query, or None if no output is expected.""",
    agent=db_agent
    )

def python_task(task):
    return Task(
    description=f"Write Python code to aid in answering the user's question or command: {task}. If a document is needed, it can be found in the documents directory.",
    expected_output="""Python code that performs the specified task.""",
    agent=swe_agent
)

def testing_task():
    return Task(
    description=f"""Test the code written by the software engineer to ensure it is bug free. If it contains bugs, modify the code to fix them. If the code is bug free,
    run the code using the repl tool.""",
    expected_output="""Output of the run code, or None if no output is expected.""",
    agent=qa_agent
)

def analysis_task(task):
    return Task(
    description=f"Based on the user's query: {task}, analyse the data and generate insights using Python. Where necessary, use the Python shell to execute code.",
    expected_output="""A comprehensive analysis of the data provided, including any insights or conclusions drawn from the analysis. 
    Visualisations using packages such as matplotlib or seaborn are encouraged.""",
    agent=data_agent
)

if __name__ == "__main__":
    load_dotenv()

    while True:
        user_input = input("Enter your question or command: ")
        
        crew = Crew(agents=[db_agent, swe_agent, qa_agent, data_agent],
                    tasks=[sql_task(user_input), run_sql_task(), python_task(user_input), testing_task(), analysis_task(user_input)],
                    process=Process.hierarchical,
                    manager_llm=llm_model,
                    verbose=2)
        
        result = crew.kickoff()
        print(result)

