"""
Obesity Treatment Multi-Agent Crew
Complete system with 5 specialized agents working together
"""

from crewai import Crew, Process
from agents import (
    create_data_analyst_agent,
    create_dietician_agent,
    create_medical_advisor_agent,
    create_fitness_trainer_agent,
    create_care_coordinator_agent
)
from tasks.all_tasks import (
    create_analysis_task,
    create_diet_plan_task,
    create_medical_evaluation_task,
    create_fitness_plan_task,
    create_coordination_task
)
from tools.patient_data_tool import PatientDataLoader, get_random_patient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


class ObesityTreatmentCrew:
    """
    Complete multi-agent crew for obesity treatment planning
    Agents: Data Analyst, Dietician, Medical Advisor, Fitness Trainer, Care Coordinator
    """

    def __init__(self):
        """Initialize all agents"""
        # Verify API key
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OPENAI_API_KEY not found. Please create .env file with your API key."
            )

        print("\n" + "="*60)
        print("INITIALIZING OBESITY TREATMENT MULTI-AGENT SYSTEM")
        print("="*60 + "\n")

        # Create all agents
        print("[1/5] Creating Data Analyst Agent...")
        self.data_analyst = create_data_analyst_agent()

        print("[2/5] Creating Dietician Agent...")
        self.dietician = create_dietician_agent()

        print("[3/5] Creating Medical Advisor Agent...")
        self.medical_advisor = create_medical_advisor_agent()

        print("[4/5] Creating Fitness Trainer Agent...")
        self.fitness_trainer = create_fitness_trainer_agent()

        print("[5/5] Creating Care Coordinator Agent...")
        self.care_coordinator = create_care_coordinator_agent()

        print("\n[OK] All agents initialized successfully!\n")

        # Initialize data loader
        self.data_loader = PatientDataLoader()

    def create_treatment_plan(self, patient_data):
        """
        Create a complete treatment plan for a patient using all agents

        Args:
            patient_data: Dictionary containing patient information

        Returns:
            str: Final integrated treatment plan
        """
        print("\n" + "="*60)
        print("CREATING COMPREHENSIVE TREATMENT PLAN")
        print("="*60 + "\n")

        print(f"Patient ID: {patient_data.get('patient_id', 'Unknown')}")
        print(f"Age: {patient_data.get('age')} years")
        print(f"BMI: {patient_data.get('bmi'):.1f} ({patient_data.get('bmi_category')})")
        print(f"Location: {patient_data.get('location_context')}")
        print(f"Wealth Index: {patient_data.get('wealth_index')}")
        print("\n" + "-"*60 + "\n")

        # Create tasks for all agents
        print("Setting up agent tasks...\n")

        # Task 1: Data Analysis
        analysis_task = create_analysis_task(self.data_analyst, patient_data)

        # Task 2: Diet Plan (depends on analysis)
        diet_task = create_diet_plan_task(self.dietician, patient_data, "{analysis}")

        # Task 3: Medical Evaluation (depends on analysis)
        medical_task = create_medical_evaluation_task(
            self.medical_advisor, patient_data, "{analysis}"
        )

        # Task 4: Fitness Plan (depends on analysis)
        fitness_task = create_fitness_plan_task(
            self.fitness_trainer, patient_data, "{analysis}"
        )

        # Task 5: Treatment Coordination (depends on all previous tasks)
        coordination_task = create_coordination_task(self.care_coordinator, patient_data)

        # Note: CrewAI 0.1.32+ handles task dependencies automatically
        # based on the sequential process order. Context is no longer set manually.

        # Create crew with all agents and tasks
        crew = Crew(
            agents=[
                self.data_analyst,
                self.dietician,
                self.medical_advisor,
                self.fitness_trainer,
                self.care_coordinator
            ],
            tasks=[
                analysis_task,
                diet_task,
                medical_task,
                fitness_task,
                coordination_task
            ],
            process=Process.sequential,
            verbose=True
        )

        # Execute the crew
        print("\nStarting multi-agent collaboration...\n")
        print("="*60)
        result = crew.kickoff()
        print("="*60 + "\n")

        return result

    def analyze_random_patient(self):
        """Analyze a random patient from the NFHS dataset"""
        print("\nFetching random patient from NFHS dataset...")
        patient = self.data_loader.get_random_patient()
        return self.create_treatment_plan(patient)

    def analyze_patient_by_criteria(self, state=None, residence_type=None,
                                    bmi_category=None, wealth_index=None):
        """Analyze a patient matching specific criteria"""
        print(f"\nSearching for patient: State={state}, Residence={residence_type}, "
              f"BMI Category={bmi_category}, Wealth={wealth_index}")

        patients = self.data_loader.get_patients_by_criteria(
            state=state,
            residence_type=residence_type,
            bmi_category=bmi_category,
            wealth_index=wealth_index,
            limit=1
        )

        if not patients:
            print("No patients found matching criteria")
            return None

        patient = patients[0]
        return self.create_treatment_plan(patient)


def main():
    """Main function to test the complete system"""
    try:
        # Create the crew
        crew = ObesityTreatmentCrew()

        # Option 1: Random patient
        print("\n" + "="*60)
        print("OPTION: Analyzing random patient from NFHS dataset")
        print("="*60)

        result = crew.analyze_random_patient()

        # Display final result
        print("\n" + "="*60)
        print("FINAL INTEGRATED TREATMENT PLAN")
        print("="*60 + "\n")

        # Save result to file with proper UTF-8 encoding
        output_file = "treatment_plan_output.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(result))
        print(f"[OK] Treatment plan saved to: {output_file}")

        # Handle Unicode output for Windows console
        try:
            print(result)
        except UnicodeEncodeError:
            # Fallback: encode to ASCII with replacement for special chars
            print(str(result).encode('ascii', 'replace').decode('ascii'))
            print(f"\n[NOTE] Some special characters couldn't be displayed.")
            print(f"       View the full plan with proper formatting in: {output_file}")

        # Option 2: Specific criteria (commented out - uncomment to use)
        # print("\n\nOPTION: Analyzing specific patient type...")
        # result = crew.analyze_patient_by_criteria(
        #     state="Maharashtra",
        #     residence_type="Urban",
        #     bmi_category="Obese"
        # )

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        print("\nTroubleshooting:")
        print("1. Ensure .env file exists with OPENAI_API_KEY")
        print("2. Verify data file: data/indian_obesity_data_clean.csv")
        print("3. Run: uv sync (to install dependencies)")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
