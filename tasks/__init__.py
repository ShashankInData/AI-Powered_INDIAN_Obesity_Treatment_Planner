"""
Tasks package for the Obesity Treatment Multi-Agent System
"""

from .data_analysis_task import create_data_analysis_task
from .all_tasks import (
    create_analysis_task,
    create_diet_plan_task,
    create_medical_evaluation_task,
    create_fitness_plan_task,
    create_coordination_task
)

__all__ = [
    'create_data_analysis_task',
    'create_analysis_task',
    'create_diet_plan_task',
    'create_medical_evaluation_task',
    'create_fitness_plan_task',
    'create_coordination_task'
]
