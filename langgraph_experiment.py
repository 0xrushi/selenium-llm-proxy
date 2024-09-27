from typing import Annotated, Any, Dict, List, Optional, TypedDict
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
import requests
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langchain.prompts import PromptTemplate

from langchain.llms.base import LLM
from typing import Any, List, Optional
import requests
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SimpleCustomLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer sk-fake-key-12345"  # Make sure to set your API_KEY
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        logger.debug(f"Sending request to custom LLM. Headers: {headers}, Data: {data}")
        
        try:
            response = requests.post("http://127.0.0.1:5000/v1/chat/completions", json=data, headers=headers)
            logger.debug(f"Received response. Status code: {response.status_code}, Content: {response.text}")
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            logger.error(f"Error in CustomLLM request: {str(e)}")
            raise

    @property
    def _identifying_params(self) -> dict[str, Any]:
        return {"name": "custom_llm"}
# Initialize the custom LLM
custom_llm = SimpleCustomLLM(api_url="http://127.0.0.1:5000", api_key="sk-fake-key-12345")

# Define the state
class State(TypedDict):
    ideas: List[str]
    analysis: Optional[str]

# Define the nodes
def generate_ideas(state: State) -> dict:
    prompt = PromptTemplate.from_template(
        "You are an Ideation Specialist. Your goal is to come up with innovative business ideas. "
        "Generate 3 innovative business ideas in the tech sector. "
        "Present each idea in a concise manner."
    )
    ideas = custom_llm(prompt.format())
    state["ideas"] = ideas.split("\n")
    return state

def analyze_ideas(state: State) -> dict:
    ideas = "\n".join(state["ideas"])
    prompt = PromptTemplate.from_template(
        "You are a Business Analyst with years of experience in market research and business strategy. "
        "Evaluate the following business ideas and rank them based on market potential and feasibility:\n\n"
        "{ideas}\n\n"
        "Provide a brief analysis for each idea."
    )
    analysis = custom_llm(prompt.format(ideas=ideas))
    state["analysis"] = analysis
    return state

# Define the graph
workflow = StateGraph(State)

# Add nodes to the graph
workflow.add_node("generate_ideas", generate_ideas)
workflow.add_node("analyze_ideas", analyze_ideas)

# Connect the nodes
workflow.add_edge("generate_ideas", "analyze_ideas")

# Set the entry point
workflow.set_entry_point("generate_ideas")

# Set the output node
workflow.add_edge("analyze_ideas", END)

# Compile the graph
app = workflow.compile()

# Run the graph
final_state = app.invoke({
    "ideas": [],
    "analysis": None
})

print("Final State:")
print("Ideas:")
for idea in final_state["ideas"]:
    print(f"- {idea}")
print("\nAnalysis:")
print(final_state["analysis"])