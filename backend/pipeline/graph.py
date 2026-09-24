from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Literal
from pipeline.prompts import SYSTEM_PROMPT
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from retrieval.vector_store import retrieve_context
from pipeline.schemas import SQLResponse
from pipeline.validator import validator_sql
from pipeline.executor import execute_query
import json
load_dotenv()

# Shared state structure
class pipelineState(TypedDict):
    question:str
    retrieved_context:dict
    generated_sql:str
    execution_result:dict
    retry_count:int
    
def generate_sql_node(state:pipelineState):
    
    # Takes question from state
    question = state['question']
    
    # Initialize the object of LLM
    llm = ChatGroq(model='qwen/qwen3.8-27b')
    
    # Extracts result from ChromaDB
    retrieved_context = retrieve_context(question)
    
    # Extracts required information from RAG's output as it contains IDs, documents and metadatas
    documents = retrieved_context['documents'][0]
    
    schema_context = []
    example_queries = []
    
    # Fills variables from extracted result
    for document in documents:
        # If output contains table and description then it is handled here
        if "Table:" in document:
            schema_context.append(document)
        # If output contains SQL queries and question then it is handled here
        elif 'Question:' in document and "SQL:" in document:
            example_queries.append(document)
    
    # Converts List into single string 
    schema_context = "\n\n".join(schema_context)
    example_queries = "\n\n".join(example_queries)

    # Values are injected into System Prompt
    system_prompt = SYSTEM_PROMPT.format(
        schema_context = schema_context,
        example_queries = example_queries
    )
    
    # LLM is called
    response = llm.invoke([
        {
            'role':'system',
            'content':system_prompt
        },
        {
            'role':'user',
            'content':question
        }
    ])
    
    
    # Converts JSON into python dictionary
    response_text = response.content
    
    # Remove Markdown code fences if the LLM added them
    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "", 1)
        response_text = response_text.replace("```", "", 1)
        response_text = response_text.strip()

    
    response_data = json.loads(response_text)

    # Pydantic validates the result
    sql_response = SQLResponse(**response_data)

    # State is updated 
    return{
        "retrieved_context":retrieved_context,
        "generated_sql":sql_response.sql
    }
    
def validate_node(state:pipelineState):
    
    # Takes generated sql 
    sql = state['generated_sql']
    
    # Verifies the SQL
    is_valid,reason = validator_sql(sql)

    if is_valid:
        # Verification Successful
        return{
            "execution_result":{
                "valid":True,
                "reason":reason
            }
        }
    # Verification Failed
    return{
        "execution_result":{
            "valid":False,
            "error":reason
        }
    }
    
def execute_node(state:pipelineState):
    # Takes the generated query
    sql = state['generated_sql']
    
    # Executes the generated query
    output = execute_query(sql)
    
    return {
        "execution_result":output
    }
    
def handle_error_node(state:pipelineState):
    
    # Extracts result after execution
    execution_result = state['execution_result']
    
    # Fetches retry count
    retry_count = state['retry_count']
    
    # Retrieves error message
    error_message = execution_result.get("error","Unknown execution error")

    # Checks if retry limit is reached or not 
    if retry_count<2:
        return{
            'execution_result':{
                'success':False,
                'error':error_message
            },
            "retry_count":retry_count+1
        }
    
    return{
        'execution_result':{
            'success':False,
            'error':error_message
        },
        'retry_count':2
    }
    
def summarize_node(state:pipelineState):
    # Use LLM Object
    llm = ChatGroq(model='qwen/qwen3.8-27b')
    
    # Fetches execution result
    execution_result = state['execution_result']

    prompt = f"""
    You are a helpful data assistant.

    The following SQL query was executed successfully:

    Columns:
    {execution_result["columns"]}

    Results:
    {execution_result["rows"]}

    Summarize these results in plain English.
    Be concise and directly answer the user's original question.
    Do not write SQL.
    """
    
    # Uses LLM to summarize the output
    response = llm.invoke(prompt)
    
    # Returns the summary from LLM to state
    return{
        'execution_result':{
            **execution_result,
            'summary':response.content
        }
    }
    
def validation_router(state:pipelineState):
    
    # Checks if the validation was successful or not 
    execution_result = state['execution_result']

    if execution_result.get('valid') is True:
        return 'execute'
    return "handle_error"

def execution_router(state:pipelineState):
    execution_result = state['execution_result']

    # Checks if execution is successful
    if execution_result.get('success') is True:
        return 'summarize'

    return 'handle_error'

def retry_router(state:pipelineState):
    
    # Checks for retry limit
    if state['retry_count']<2:
        return 'retry'
    return 'stop'
    
# Initialize Graph Object
workflow = StateGraph(pipelineState)

# Add Nodes
workflow.add_node('summarize_node',summarize_node)
workflow.add_node('generate_sql_node',generate_sql_node)
workflow.add_node('validate_node',validate_node)
workflow.add_node('execute_node',execute_node)
workflow.add_node('handle_error_node',handle_error_node)

# Add Edges
workflow.add_edge(START,"generate_sql_node")
workflow.add_edge("generate_sql_node","validate_node")

# Conditional edge handling for validation (Success/Failure)
workflow.add_conditional_edges(
    'validate_node',
    validation_router,
    {
        'execute':'execute_node',
        'handle_error':'handle_error_node'
    }
)

# Conditional edge handling for execution (Success/Failure)
workflow.add_conditional_edges(
    'execute_node',
    execution_router,
    {
        'summarize':'summarize_node',
        'handle_error':'handle_error_node'
    }
)

# Conditional edge handling for error (retry)
workflow.add_conditional_edges(
    'handle_error_node',
    retry_router,
    {
        'retry':'generate_sql_node',
        'stop':END
    }
)

workflow.add_edge('summarize_node',END)

# Compile Graph
app = workflow.compile()