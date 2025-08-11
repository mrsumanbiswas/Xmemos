import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated, List
import operator

# Load environment variables from .env file
load_dotenv()

# Define the state for our graph
class AgentState(TypedDict):
    messages: Annotated[List[any], operator.add]

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GEMINI_API_KEY"))

# Define the function that will be called by the graph
def call_model(state):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

# Define the graph
workflow = StateGraph(AgentState)

# Add the 'call_model' node
workflow.add_node("agent", call_model)

# Set the entrypoint
workflow.set_entry_point("agent")

# Add a finish condition
workflow.add_edge("agent", END)

# Compile the graph
app = workflow.compile()

def run_agent(input_text):
    """
    Runs the AI agent with the given input text.
    """
    inputs = {"messages": [HumanMessage(content=input_text)]}
    response = app.invoke(inputs)
    return response['messages'][-1].content

def main():
    """
    Main function to run the AI agent.
    """
    user_input = input()
    if user_input.strip():
        response = run_agent(user_input)
        print(response)

if __name__ == "__main__":
    main()
