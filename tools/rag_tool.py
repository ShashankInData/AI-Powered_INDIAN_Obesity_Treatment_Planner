"""
RAG Tool for CrewAI Agents
Provides retrieval-augmented generation capabilities using medical knowledge and patient data
"""

from crewai.tools import tool
from typing import Optional
import sys
import os

# Add parent directory to path to import other tools
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from medical_knowledge_rag import MedicalKnowledgeRAG, get_medical_context
from patient_data_indexer import PatientDataIndexer, get_similar_patient_context


# Initialize RAG systems (singleton pattern for efficiency)
_medical_rag = None
_patient_indexer = None


def get_medical_rag():
    """Get or create medical knowledge RAG instance"""
    global _medical_rag
    if _medical_rag is None:
        _medical_rag = MedicalKnowledgeRAG()
        try:
            _medical_rag.load_existing_vectorstore()
            print("[RAG] Loaded existing medical knowledge vector store")
        except FileNotFoundError:
            print("[RAG] Creating new medical knowledge vector store...")
            _medical_rag.create_medical_knowledge_base()
    return _medical_rag


def get_patient_indexer():
    """Get or create patient data indexer instance"""
    global _patient_indexer
    if _patient_indexer is None:
        _patient_indexer = PatientDataIndexer(csv_path="data/indian_obesity_data_clean.csv")
        print("[RAG] Initialized patient data indexer")
    return _patient_indexer


@tool("Query Medical Knowledge")
def query_medical_knowledge(query: str) -> str:
    """
    Query the medical knowledge base for evidence-based information.

    Use this tool to get information about:
    - WHO obesity guidelines and BMI classifications
    - Medications for obesity (Orlistat, Metformin, Semaglutide, Liraglutide)
    - Indian dietary guidelines and meal planning
    - Exercise recommendations for obesity management
    - Laboratory tests and monitoring protocols
    - Regional health considerations for India

    Args:
        query: Natural language question about medical knowledge

    Returns:
        Relevant medical knowledge and guidelines

    Example queries:
        - "What are the WHO guidelines for obesity treatment?"
        - "Which medications are recommended for BMI 32?"
        - "What dietary recommendations are appropriate for Indian patients?"
        - "What lab tests should be ordered for an obese patient?"
        - "Exercise guidelines for sedentary patients"
    """
    try:
        rag = get_medical_rag()
        context = get_medical_context(query, rag, k=3)
        return context
    except Exception as e:
        return f"Error retrieving medical knowledge: {str(e)}"


@tool("Find Similar Patient Cases")
def find_similar_patients(patient_description: str) -> str:
    """
    Find similar patient cases from the NFHS dataset (9,730 patient records).

    Use this tool to retrieve historical patient data that matches the current patient's profile.
    This helps in evidence-based treatment planning by finding what worked for similar patients.

    Args:
        patient_description: Natural language description of the patient's key characteristics

    Returns:
        Information about 3 similar patients including their demographics, BMI, location, and socioeconomic status

    Example descriptions:
        - "35 year old obese patient from rural Maharashtra with BMI 31"
        - "28 year old overweight urban patient from Kerala, middle wealth index"
        - "42 year old female with BMI 29 from rural Uttar Pradesh, poorer wealth index"
        - "Young adult male, BMI 33, obese, from urban Tamil Nadu, richer wealth index"
    """
    try:
        indexer = get_patient_indexer()
        context = get_similar_patient_context(patient_description, indexer, k=3)
        return context
    except Exception as e:
        return f"Error finding similar patients: {str(e)}"


@tool("Get Evidence-Based Treatment Guidelines")
def get_treatment_guidelines(condition: str, patient_context: str = "") -> str:
    """
    Get comprehensive evidence-based treatment guidelines for a specific condition or scenario.

    Use this tool when you need detailed clinical guidelines for treatment planning.
    Combines medical knowledge with patient context for personalized recommendations.

    Args:
        condition: The medical condition or treatment scenario
        patient_context: Optional patient-specific context (BMI, age, location, etc.)

    Returns:
        Evidence-based treatment guidelines and recommendations

    Example usage:
        - condition="obesity management", patient_context="BMI 32, rural India, low income"
        - condition="weight loss diet plan", patient_context="vegetarian patient from South India"
        - condition="exercise program for obesity", patient_context="sedentary office worker with BMI 30"
        - condition="pharmacotherapy for obesity", patient_context="BMI 35 with pre-diabetes"
    """
    try:
        # Construct query with patient context
        if patient_context:
            query = f"{condition} for patient with {patient_context}"
        else:
            query = condition

        rag = get_medical_rag()
        context = get_medical_context(query, rag, k=4)
        return context
    except Exception as e:
        return f"Error retrieving treatment guidelines: {str(e)}"


@tool("Search Indian-Specific Health Data")
def search_indian_health_data(query: str) -> str:
    """
    Search for India-specific health information and recommendations.

    Use this tool to get culturally appropriate and region-specific information for Indian patients.
    Covers dietary practices, cost considerations, regional variations, and local healthcare context.

    Args:
        query: Question about Indian health context, dietary patterns, or regional considerations

    Returns:
        India-specific health information and recommendations

    Example queries:
        - "Traditional Indian foods for weight loss"
        - "Cost of obesity medications in India"
        - "Regional obesity prevalence in Kerala"
        - "Vegetarian protein sources for Indian diet"
        - "Affordable exercise options for rural India"
        - "Cultural considerations for obesity treatment in India"
    """
    try:
        rag = get_medical_rag()

        # Add India-specific context to query
        enhanced_query = f"India specific: {query}"
        context = get_medical_context(enhanced_query, rag, k=3)

        return context
    except Exception as e:
        return f"Error searching Indian health data: {str(e)}"


# Export all tools as a list for easy import
rag_tools = [
    query_medical_knowledge,
    find_similar_patients,
    get_treatment_guidelines,
    search_indian_health_data
]


if __name__ == "__main__":
    # Test the RAG tools
    print("\n" + "="*60)
    print("TESTING RAG TOOLS")
    print("="*60 + "\n")

    # Test 1: Query medical knowledge
    print("Test 1: Query Medical Knowledge")
    print("-" * 60)
    result = query_medical_knowledge("What medications are recommended for obesity with BMI 32?")
    print(result[:500] + "...\n")

    # Test 2: Find similar patients
    print("\nTest 2: Find Similar Patients")
    print("-" * 60)
    result = find_similar_patients("41 year old obese patient from rural Andhra Pradesh with BMI 27")
    print(result[:500] + "...\n")

    # Test 3: Get treatment guidelines
    print("\nTest 3: Get Treatment Guidelines")
    print("-" * 60)
    result = get_treatment_guidelines(
        condition="weight loss diet plan",
        patient_context="vegetarian patient from South India, BMI 30"
    )
    print(result[:500] + "...\n")

    # Test 4: Search Indian-specific data
    print("\nTest 4: Search Indian Health Data")
    print("-" * 60)
    result = search_indian_health_data("Cost-effective exercise options for rural India")
    print(result[:500] + "...\n")

    print("="*60)
    print("RAG TOOLS TEST COMPLETE")
    print("="*60)
