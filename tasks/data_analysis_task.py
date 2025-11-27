"""
Data Analysis Task
Defines the task for analyzing patient obesity data
"""

from crewai import Task
import yaml
import os


def load_task_config():
    """Load task configuration from YAML file"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'tasks.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config['analyze_patient_data']


def create_data_analysis_task(agent, patient_data):
    """
    Create and return the Data Analysis Task

    Args:
        agent: The agent that will execute this task
        patient_data: Dictionary containing patient information

    Returns:
        Task: Configured Data Analysis Task
    """
    # Load configuration
    config = load_task_config()

    # Format patient data for the task
    formatted_data = format_patient_data(patient_data)

    # Create task
    task = Task(
        description=config['description'].format(patient_data=formatted_data),
        expected_output=config['expected_output'],
        agent=agent
    )

    return task


def format_patient_data(data):
    """
    Format patient data into a readable string

    Args:
        data: Dictionary containing patient information

    Returns:
        str: Formatted patient data string
    """
    formatted = []
    for key, value in data.items():
        # Convert key from snake_case to Title Case
        formatted_key = key.replace('_', ' ').title()
        formatted.append(f"- {formatted_key}: {value}")

    return "\n    ".join(formatted)


if __name__ == "__main__":
    # Test task creation
    from agents.data_analyst_agent import create_data_analyst_agent

    print("Creating test task...")
    agent = create_data_analyst_agent()

    sample_data = {
        "age": 25,
        "gender": "Female",
        "height": 165,
        "weight": 75,
        "bmi": 27.5,
        "physical_activity": "Low",
        "family_history": "Yes"
    }

    task = create_data_analysis_task(agent, sample_data)
    print("Task created successfully!")
    print(f"\nDescription preview:\n{task.description[:200]}...")
