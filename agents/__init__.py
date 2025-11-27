"""
Agents package for the Obesity Treatment Multi-Agent System
"""

from .data_analyst_agent import create_data_analyst_agent
from .dietician_agent import create_dietician_agent
from .medical_advisor_agent import create_medical_advisor_agent
from .fitness_trainer_agent import create_fitness_trainer_agent
from .care_coordinator_agent import create_care_coordinator_agent

__all__ = [
    'create_data_analyst_agent',
    'create_dietician_agent',
    'create_medical_advisor_agent',
    'create_fitness_trainer_agent',
    'create_care_coordinator_agent'
]
