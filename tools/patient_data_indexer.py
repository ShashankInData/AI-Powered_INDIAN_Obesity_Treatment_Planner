"""
Patient Data Indexer
Indexes NFHS patient data in ChromaDB for similarity search and historical outcome retrieval
"""

import pandas as pd
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import List
import os

# State mapping (from NFHS-5)
STATE_MAPPING = {
    1: "Andhra Pradesh", 2: "Arunachal Pradesh", 3: "Assam", 4: "Bihar",
    5: "Chhattisgarh", 6: "Goa", 7: "Gujarat", 8: "Haryana",
    9: "Himachal Pradesh", 10: "Jharkhand", 11: "Karnataka", 12: "Kerala",
    13: "Madhya Pradesh", 14: "Maharashtra", 15: "Manipur", 16: "Meghalaya",
    17: "Mizoram", 18: "Nagaland", 19: "Odisha", 20: "Punjab",
    21: "Rajasthan", 22: "Sikkim", 23: "Tamil Nadu", 24: "Telangana",
    25: "Tripura", 26: "Uttar Pradesh", 27: "Uttarakhand", 28: "West Bengal",
    29: "Delhi", 30: "Jammu & Kashmir", 31: "Ladakh", 32: "Andaman & Nicobar",
    33: "Chandigarh", 34: "Dadra & Nagar Haveli", 35: "Lakshadweep", 36: "Puducherry"
}

RESIDENCE_MAPPING = {
    1: "Urban",
    2: "Rural"
}

WEALTH_MAPPING = {
    1: "Poorest",
    2: "Poorer",
    3: "Middle",
    4: "Richer",
    5: "Richest"
}


class PatientDataIndexer:
    """Index patient data for RAG retrieval"""

    def __init__(self, csv_path: str, persist_directory: str = "./chroma_db"):
        """Initialize with patient data CSV and vector store directory"""
        self.csv_path = csv_path
        self.persist_directory = persist_directory
        self.df = None
        self.vectorstore = None

        # Load embeddings model
        print("Loading sentence-transformers model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def load_patient_data(self):
        """Load patient data from CSV"""
        print(f"Loading patient data from {self.csv_path}...")
        self.df = pd.read_csv(self.csv_path)
        print(f"Loaded {len(self.df)} patient records")
        return self.df

    def create_patient_documents(self, sample_size: int = None) -> List[Document]:
        """
        Convert patient records to LangChain documents

        Args:
            sample_size: If specified, only index a sample of patients (for faster processing)
        """
        if self.df is None:
            self.load_patient_data()

        # Sample data if requested (for faster testing/development)
        if sample_size:
            df_to_index = self.df.sample(n=min(sample_size, len(self.df)), random_state=42)
            print(f"Sampling {len(df_to_index)} patients for indexing")
        else:
            df_to_index = self.df
            print(f"Indexing all {len(df_to_index)} patient records")

        documents = []

        for idx, row in df_to_index.iterrows():
            # Map encoded values to readable names
            state_name = STATE_MAPPING.get(int(row["State"]), "Unknown")
            residence_type = RESIDENCE_MAPPING.get(int(row["Urban_Rural"]), "Unknown")
            wealth_index = WEALTH_MAPPING.get(int(row["Wealth_Index"]), "Unknown")

            # Create a text description of the patient for embedding
            patient_text = self._create_patient_description(row, state_name, residence_type, wealth_index)

            # Create document with patient text and metadata
            doc = Document(
                page_content=patient_text,
                metadata={
                    "patient_id": f"NFHS_{idx}",
                    "age": int(row["Age"]),
                    "height": float(row["Height_cm"]),
                    "weight": float(row["Weight_kg"]),
                    "bmi": float(row["BMI"]),
                    "bmi_category": str(row["BMI_Category"]),
                    "state": state_name,
                    "residence_type": residence_type,
                    "wealth_index": wealth_index,
                    "record_type": "patient_data"  # To distinguish from medical knowledge
                }
            )
            documents.append(doc)

        print(f"Created {len(documents)} patient documents")
        return documents

    def _create_patient_description(self, row, state_name: str, residence_type: str, wealth_index: str) -> str:
        """Create a natural language description of a patient for embedding"""

        # Create description that captures patient characteristics
        description = f"""
Patient Profile:
- Demographics: {row['Age']} year old from {state_name}, {residence_type} area
- Socioeconomic Status: {wealth_index} wealth index
- Physical Measurements: Height {row['Height_cm']}cm, Weight {row['Weight_kg']}kg
- Body Mass Index: {row['BMI']:.2f} ({row['BMI_Category']})
- Health Classification: {row['BMI_Category']} BMI category
"""

        # Add clinical context based on BMI category
        if row['BMI_Category'] == 'Obese':
            description += """
- Clinical Concerns: High risk for obesity-related comorbidities including type 2 diabetes, hypertension, cardiovascular disease
- Treatment Priority: Weight loss of 5-10% recommended, lifestyle modifications essential, consider pharmacotherapy
"""
        elif row['BMI_Category'] == 'Overweight':
            description += """
- Clinical Concerns: Moderate risk for metabolic syndrome and chronic diseases
- Treatment Priority: Weight management through diet and exercise, prevent progression to obesity
"""
        elif row['BMI_Category'] == 'Normal':
            description += """
- Clinical Status: Healthy weight range
- Treatment Priority: Maintenance of current weight, healthy lifestyle habits
"""
        elif row['BMI_Category'] == 'Underweight':
            description += """
- Clinical Concerns: Risk of nutritional deficiencies, weakened immunity
- Treatment Priority: Weight gain through balanced nutrition, rule out underlying conditions
"""

        # Add regional context
        description += f"""
- Regional Considerations: Patient from {state_name} - consider local food availability, cultural dietary practices, and regional health infrastructure
- Socioeconomic Context: {wealth_index} wealth index - treatment plan should be cost-appropriate and accessible
"""

        return description.strip()

    def index_patients(self, sample_size: int = None):
        """
        Index patient data in ChromaDB

        Args:
            sample_size: If specified, only index a sample of patients
                        Recommended: 500-1000 for testing, None for full dataset
        """
        # Create patient documents
        documents = self.create_patient_documents(sample_size=sample_size)

        print("Creating vector store for patient data...")
        print("This may take several minutes for large datasets...")

        # Create or load vector store
        # Use a separate collection for patient data
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name="patient_data",
            persist_directory=self.persist_directory
        )

        print(f"Patient data indexed successfully in {self.persist_directory}")
        return self.vectorstore

    def find_similar_patients(self, query: str, k: int = 5) -> List[Document]:
        """
        Find similar patients based on a query

        Args:
            query: Natural language description of patient characteristics
            k: Number of similar patients to return
        """
        if self.vectorstore is None:
            # Load existing vector store
            self.vectorstore = Chroma(
                collection_name="patient_data",
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )

        results = self.vectorstore.similarity_search(query, k=k)
        return results

    def find_similar_patients_with_scores(self, query: str, k: int = 5) -> List[tuple]:
        """Find similar patients with similarity scores"""
        if self.vectorstore is None:
            self.vectorstore = Chroma(
                collection_name="patient_data",
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )

        results = self.vectorstore.similarity_search_with_score(query, k=k)
        return results


def get_similar_patient_context(query: str, indexer: PatientDataIndexer, k: int = 3) -> str:
    """
    Get context about similar patients for agent use

    Args:
        query: Description of target patient
        indexer: PatientDataIndexer instance
        k: Number of similar patients to retrieve

    Returns:
        Formatted string with similar patient information
    """
    results = indexer.find_similar_patients(query, k=k)

    if not results:
        return "No similar patient records found."

    context = f"Similar Patient Cases (found {len(results)} similar patients):\n\n"

    for i, doc in enumerate(results, 1):
        meta = doc.metadata
        context += f"Patient {i} (ID: {meta['patient_id']}):\n"
        context += f"- Age: {meta['age']} years\n"
        context += f"- BMI: {meta['bmi']:.2f} ({meta['bmi_category']})\n"
        context += f"- Location: {meta['state']}, {meta['residence_type']}\n"
        context += f"- Wealth Index: {meta['wealth_index']}\n"
        context += f"- Height: {meta['height']}cm, Weight: {meta['weight']}kg\n\n"

    return context


if __name__ == "__main__":
    # Path to patient data
    csv_path = "data/indian_obesity_data_clean.csv"

    # Initialize indexer
    indexer = PatientDataIndexer(csv_path)

    # Index a sample of patients for testing (1000 patients)
    # For production, use sample_size=None to index all 9,730 patients
    print("\n" + "="*60)
    print("INDEXING PATIENT DATA")
    print("="*60 + "\n")

    # Start with 1000 patients for faster testing
    indexer.index_patients(sample_size=1000)

    # Test query
    print("\n" + "="*60)
    print("TESTING PATIENT SIMILARITY SEARCH")
    print("="*60 + "\n")

    query = "41 year old obese patient from rural Andhra Pradesh with BMI 27"
    print(f"Query: {query}\n")

    context = get_similar_patient_context(query, indexer, k=3)
    print(context)

    print("\n" + "="*60)
    print("Patient data indexing complete!")
    print("Vector store location: ./chroma_db")
    print("Collection name: patient_data")
    print("="*60)
