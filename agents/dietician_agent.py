"""
Dietician Agent - The Indian Nutrition Specialist
Creates personalized meal plans for obesity management
"""

from crewai import Agent
from langchain_openai import ChatOpenAI
import yaml
import os


def load_agent_config():
    """Load agent configuration from YAML file"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'agents.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config['dietician']


def create_dietician_agent(llm=None):
    """
    Create and return the Dietician Agent

    Args:
        llm: Language model to use (optional, defaults to GPT-4o-mini)

    Returns:
        Agent: Configured Dietician Agent
    """
    # Load configuration
    config = load_agent_config()

    # Set up LLM if not provided
    if llm is None:
        llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.7
        )

    # Create agent
    agent = Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        verbose=config['verbose'],
        allow_delegation=config['allow_delegation'],
        llm=llm
    )

    return agent


if __name__ == "__main__":
    # Test agent creation
    print("Creating Dietician Agent...")
    agent = create_dietician_agent()
    print(f"Agent created successfully!")
    print(f"Role: {agent.role}")
    print(f"Goal: {agent.goal}")
