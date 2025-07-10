from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models import ChatOpenAI
import threading
from agents.tools import rf_diffusion_tool, pdb_search_tool

# example prompt: design a protein using the pdb 1R42 and contigs A20-24/0 20-100 and hotspots A21, A22

class Agent:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_agent(cls):
        with cls._lock:
            if cls._instance is None:
                print("Creating new agent...")
                llm = ChatOpenAI(model="gpt-4o-mini")
                tools = [rf_diffusion_tool, pdb_search_tool]
                cls._instance = initialize_agent(
                    tools=tools,
                    llm=llm,
                    agent=AgentType.OPENAI_FUNCTIONS,
                    verbose=True,
                    agent_kwargs={
                        "system_message": (
                            "You are a protein design assistant. "
                            "When asked to design a protein based on a PDB ID, use `pdb_search_tool` "
                            "to get the full structure text, then call `rf_diffusion_tool` with that content."
                        )
                    }
                )
            return cls._instance