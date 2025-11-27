"""
All Tasks for the Obesity Treatment Multi-Agent System
Centralized task creation for all agents
"""

from crewai import Task
import yaml
import os


def load_tasks_config():
    """Load all task configurations from YAML file"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'tasks.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def format_patient_data(data):
    """Format patient data into a readable string"""
    formatted = []
    for key, value in data.items():
        formatted_key = key.replace('_', ' ').title()
        formatted.append(f"- {formatted_key}: {value}")
    return "\n    ".join(formatted)


def create_analysis_task(agent, patient_data):
    """Create data analysis task"""
    config = load_tasks_config()['analyze_patient_data']
    formatted_data = format_patient_data(patient_data)

    return Task(
        description=config['description'].format(patient_data=formatted_data),
        expected_output=config['expected_output'],
        agent=agent
    )


def create_diet_plan_task(agent, patient_data, diagnostic_report):
    """Create diet plan task"""
    config = load_tasks_config()['create_diet_plan']
    formatted_data = format_patient_data(patient_data)

    return Task(
        description=config['description'].format(
            patient_data=formatted_data,
            diagnostic_report=diagnostic_report
        ),
        expected_output=config['expected_output'],
        agent=agent
    )


def create_medical_evaluation_task(agent, patient_data, diagnostic_report):
    """Create medical evaluation task"""
    config = load_tasks_config()['evaluate_medical_needs']
    formatted_data = format_patient_data(patient_data)

    return Task(
        description=config['description'].format(
            patient_data=formatted_data,
            diagnostic_report=diagnostic_report
        ),
        expected_output=config['expected_output'],
        agent=agent
    )


def create_fitness_plan_task(agent, patient_data, diagnostic_report):
    """Create fitness plan task"""
    config = load_tasks_config()['create_fitness_plan']
    formatted_data = format_patient_data(patient_data)

    return Task(
        description=config['description'].format(
            patient_data=formatted_data,
            diagnostic_report=diagnostic_report
        ),
        expected_output=config['expected_output'],
        agent=agent
    )


def create_coordination_task(agent, patient_data):
    """Create treatment coordination task"""
    config = load_tasks_config()['coordinate_treatment_plan']
    formatted_data = format_patient_data(patient_data)

    # Note: The specialist recommendations will be automatically provided
    # by CrewAI from previous tasks
    return Task(
        description=config['description'].format(
            patient_data=formatted_data,
            diagnostic_report="{diagnostic_report}",
            diet_plan="{diet_plan}",
            medical_evaluation="{medical_evaluation}",
            fitness_plan="{fitness_plan}"
        ),
        expected_output=config['expected_output'],
        agent=agent
    )
