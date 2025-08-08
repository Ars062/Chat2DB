# from langchain_community.llms import Ollama
# from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
# from langchain_community.llms import Ollama
# from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain.utilities import SQLDatabase
from langchain_community.utilities import SQLDatabase
# from langchain_community.llms import Ollama
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent, AgentType
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX
from langchain.chains.sql_database.prompt import _mysql_prompt

from langchain.prompts import FewShotPromptTemplate
from few_short_questions import few_short_questions
import sys
import os

from dotenv import load_dotenv
load_dotenv() 
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192"
)
db_user = "root"
db_password = "Ars10762%40"  #  Escaped '@' as '%40'
db_host = "localhost"
db_port = "3306"
db_name = "atliq_tshirts"

uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
# print("✅ Connecting using:", uri)

db = SQLDatabase.from_uri(uri)
# print(db.get_table_names())
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorize=[ " ".join( str(v) for v in example.values()) for example in few_short_questions]
vectorstore=FAISS.from_texts(vectorize, embedding=embeddings ,metadatas=few_short_questions)
mysql_prompt="""You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURDATE() function to get the current date, if the question involves "today".

Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here
No pre-amble."""

example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore, 
    k=2,
    input_keys=["input"]  # will compare only the 'Question' field
)
example_prompt = PromptTemplate(
    input_variables=["input", "SQLQuery", "SQLResult", "Answer"],
    template="\nQuestion: {input}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
 )
few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=_mysql_prompt,
    suffix=PROMPT_SUFFIX,
    input_variables=["input"], 
    partial_variables={
        "tools": "{tools}",
        "tool_names": "{tool_names}",
        "agent_scratchpad": "{agent_scratchpad}"  
    }
)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    prompt=few_shot_prompt,

)
def run_sql_agent(query: str) -> str:
    try:
        return agent_executor.run({"input": query})
    except Exception as e:
        if hasattr(e, "llm_output"):
            print("⚠️ Raw LLM Output (Not parsable by ReAct):")
            print(e.llm_output)
        else:
            print("⚠️ Unknown Error:")
            print(e) 


# if __name__ == "__main__":
#     qsn1= "How many t-shirts do we have left for nike in extra small size and white color?"
#     response = run_sql_agent( qsn1)

#     print(response)
