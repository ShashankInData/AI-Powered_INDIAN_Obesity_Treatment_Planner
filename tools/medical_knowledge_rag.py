"""
Medical Knowledge RAG System
Provides retrieval-augmented generation capabilities for obesity treatment agents
"""

from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import os
from typing import List, Dict


class MedicalKnowledgeRAG:
    """RAG system for medical knowledge retrieval"""

    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize the RAG system with ChromaDB vector store"""
        self.persist_directory = persist_directory

        # Use sentence-transformers for embeddings
        print("Loading sentence-transformers model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Initialize ChromaDB
        self.vectorstore = None

    def create_medical_knowledge_base(self):
        """Create vector store with medical knowledge documents"""

        # Medical knowledge documents for obesity treatment
        medical_docs = self._get_medical_documents()

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

        splits = text_splitter.split_documents(medical_docs)

        print(f"Creating vector store with {len(splits)} document chunks...")

        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            collection_name="medical_knowledge",
            persist_directory=self.persist_directory
        )

        print(f"Vector store created successfully at {self.persist_directory}")
        return self.vectorstore

    def load_existing_vectorstore(self):
        """Load existing vector store from disk"""
        if not os.path.exists(self.persist_directory):
            raise FileNotFoundError(f"No vector store found at {self.persist_directory}")

        self.vectorstore = Chroma(
            collection_name="medical_knowledge",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

        print("Loaded existing vector store")
        return self.vectorstore

    def query_medical_knowledge(self, query: str, k: int = 5) -> List[Document]:
        """Query the medical knowledge base"""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Call create_medical_knowledge_base() or load_existing_vectorstore() first")

        results = self.vectorstore.similarity_search(query, k=k)
        return results

    def query_with_scores(self, query: str, k: int = 5) -> List[tuple]:
        """Query with similarity scores"""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized")

        results = self.vectorstore.similarity_search_with_score(query, k=k)
        return results

    def _get_medical_documents(self) -> List[Document]:
        """Get medical knowledge documents for obesity treatment"""

        documents = []

        # WHO Obesity Guidelines
        who_guidelines = Document(
            page_content="""
WHO Obesity Guidelines (2023):

Classification of BMI for Adults:
- Underweight: BMI < 18.5
- Normal weight: BMI 18.5-24.9
- Overweight: BMI 25.0-29.9
- Obese Class I: BMI 30.0-34.9
- Obese Class II: BMI 35.0-39.9
- Obese Class III: BMI ≥ 40.0

For Asian populations, WHO recommends lower thresholds:
- Overweight: BMI ≥ 23.0
- Obese: BMI ≥ 27.5

Treatment Recommendations:
1. Lifestyle modifications (diet + exercise) as first-line treatment
2. Target weight loss: 5-10% of body weight over 6 months
3. Caloric deficit: 500-750 kcal/day for gradual weight loss
4. Physical activity: At least 150 minutes/week of moderate-intensity exercise
5. Pharmacotherapy for BMI ≥ 30 or BMI ≥ 27 with comorbidities
6. Bariatric surgery for BMI ≥ 40 or BMI ≥ 35 with comorbidities

Comorbidities Associated with Obesity:
- Type 2 diabetes mellitus
- Hypertension
- Cardiovascular disease
- Dyslipidemia
- Sleep apnea
- Osteoarthritis
- Fatty liver disease
- Depression and anxiety
""",
            metadata={"source": "WHO Guidelines", "year": 2023}
        )
        documents.append(who_guidelines)

        # Indian Obesity Research
        indian_research = Document(
            page_content="""
Indian Obesity Research Findings:

Prevalence in India (NFHS-5, 2019-21):
- Urban women: 29.8% overweight/obese
- Rural women: 19.7% overweight/obese
- Rapid increase in last decade across all states

Regional Variations:
- Higher prevalence: Kerala, Punjab, Goa, Tamil Nadu
- Urban-rural gap narrowing
- Wealth index strongly correlates with obesity

Dietary Patterns in India:
- High carbohydrate intake (rice, wheat, millets)
- Vegetarian diets common (40% of population)
- Traditional foods: dal, vegetables, chapati, rice
- Increasing consumption of processed foods and sugary beverages

Culturally Appropriate Interventions:
1. Focus on traditional Indian diets (whole grains, legumes, vegetables)
2. Portion control rather than food elimination
3. Walking and yoga as primary exercise modalities
4. Family-based interventions (cooking, eating together)
5. Consider religious fasting practices
6. Address stigma and mental health aspects

Cost-Effective Strategies:
- Use locally available seasonal produce
- Home-based exercises (no gym membership needed)
- Generic medications when pharmacotherapy indicated
- Community health worker support
- mHealth interventions (WhatsApp, SMS)
""",
            metadata={"source": "Indian Medical Research", "topic": "Obesity"}
        )
        documents.append(indian_research)

        # Medications for Obesity
        medications = Document(
            page_content="""
Pharmacotherapy for Obesity in India:

1. Orlistat (Xenical)
   - Mechanism: Lipase inhibitor, reduces fat absorption by 30%
   - Dosage: 120mg three times daily with meals
   - Indications: BMI ≥ 30 or BMI ≥ 27 with comorbidities
   - Side effects: GI symptoms (oily stools, flatulence)
   - Cost in India: ₹500-700/month
   - Available as generic

2. Metformin (off-label for obesity)
   - Mechanism: Insulin sensitizer, reduces hepatic glucose production
   - Dosage: 500-1000mg twice daily
   - Indications: Obesity with insulin resistance, PCOS, pre-diabetes
   - Side effects: GI upset, vitamin B12 deficiency (long-term)
   - Cost in India: ₹100-300/month
   - First-line for obesity with metabolic syndrome

3. Semaglutide (GLP-1 agonist) - Wegovy, Ozempic
   - Mechanism: GLP-1 receptor agonist, reduces appetite
   - Dosage: 2.4mg weekly (subcutaneous)
   - Indications: BMI ≥ 30 or BMI ≥ 27 with comorbidities
   - Weight loss: 15-20% of body weight
   - Side effects: Nausea, vomiting, diarrhea, pancreatitis risk
   - Cost in India: ₹15,000-20,000/month (expensive)
   - Not widely available, limited to urban centers

4. Liraglutide (GLP-1 agonist) - Saxenda
   - Mechanism: GLP-1 receptor agonist
   - Dosage: 3.0mg daily (subcutaneous)
   - Weight loss: 8-10% of body weight
   - Cost in India: ₹12,000-15,000/month
   - More accessible than semaglutide

Prescribing Guidelines:
- Start with lifestyle modifications for 3-6 months
- Add pharmacotherapy if insufficient weight loss
- Monitor for side effects monthly
- Reassess effectiveness at 3 months (minimum 5% weight loss expected)
- Continue only if showing benefit
- Consider cost and patient ability to afford long-term treatment

Contraindications:
- Pregnancy and breastfeeding
- Uncontrolled hypertension
- History of eating disorders
- Severe psychiatric illness
- GI disorders (for orlistat)
""",
            metadata={"source": "Drug Database", "topic": "Obesity Medications"}
        )
        documents.append(medications)

        # Dietary Guidelines for India
        diet_guidelines = Document(
            page_content="""
Evidence-Based Dietary Guidelines for Obesity Management in India:

Macronutrient Distribution:
- Carbohydrates: 45-55% of total calories (focus on complex carbs)
- Protein: 15-25% of total calories (1.2-1.6g/kg for weight loss)
- Fat: 25-35% of total calories (emphasize healthy fats)

Indian Meal Planning Principles:
1. Whole grains: Brown rice, whole wheat, millets (jowar, bajra, ragi)
2. Protein sources:
   - Vegetarian: Dal, legumes, paneer, tofu, Greek yogurt
   - Non-vegetarian: Chicken, fish, eggs
3. Vegetables: 5-7 servings/day, variety of colors
4. Fruits: 2-3 servings/day, preferably whole fruits
5. Healthy fats: Mustard oil, groundnut oil, nuts, seeds
6. Limit: Refined flour (maida), white rice, sugar, fried foods

Portion Control (for weight loss):
- Rice/roti: 1-2 small servings (½-1 cup cooked rice or 2 small rotis)
- Dal: 1 cup cooked
- Vegetables: 2 cups cooked
- Protein: Palm-sized portion (100-150g)
- Oil: 2-3 teaspoons/day total

Sample Indian Weight Loss Meal Plan:
Breakfast (300-350 kcal):
- 2 small vegetable poha/upma/idli OR
- 2 small moong dal chilla with mint chutney OR
- Oats porridge with fruits and nuts

Mid-morning (100-150 kcal):
- 1 fruit OR
- 1 cup buttermilk OR
- Handful of roasted chickpeas

Lunch (400-450 kcal):
- 1 cup brown rice/2 small whole wheat rotis
- 1 cup dal
- 1-2 cups mixed vegetables
- Small bowl of curd

Evening (100-150 kcal):
- Green tea with 2-3 digestive biscuits OR
- Sprouted salad OR
- Roasted makhana

Dinner (350-400 kcal):
- 2 small rotis OR 1 small bowl quinoa
- 1 cup vegetables
- Small portion grilled chicken/paneer/dal
- Salad

Total: 1500-1700 kcal/day (for gradual weight loss)

Foods to Limit:
- Refined carbs: White rice, maida products, biscuits
- Sugary items: Sweets, sugar-sweetened beverages
- Fried foods: Pakoras, samosas, fried snacks
- Processed foods: Chips, instant noodles, ready-to-eat meals
- Excessive salt

Hydration:
- 2-3 liters water/day
- Green tea, herbal teas (no sugar)
- Limit fruit juices (prefer whole fruits)
- Avoid sugary drinks and alcohol
""",
            metadata={"source": "Nutrition Guidelines", "region": "India"}
        )
        documents.append(diet_guidelines)

        # Exercise Guidelines
        exercise_guidelines = Document(
            page_content="""
Exercise Guidelines for Obesity Management (Indian Context):

WHO Recommendations for Weight Loss:
- Moderate-intensity: 150-300 minutes/week
- Vigorous-intensity: 75-150 minutes/week
- Resistance training: 2-3 days/week
- Reduce sedentary time

Culturally Appropriate Physical Activities:

1. Walking:
   - Most accessible in India (no equipment/cost)
   - Start: 15-20 minutes/day
   - Progress: 30-60 minutes/day, 5-7 days/week
   - Target: Brisk pace (can talk but not sing)

2. Yoga:
   - Highly accepted across India
   - Combines physical activity, stress management, mindfulness
   - Effective styles for weight loss: Power yoga, Vinyasa
   - Duration: 30-45 minutes, 4-5 days/week

3. Home-Based Exercises:
   - Bodyweight exercises: Squats, lunges, push-ups, planks
   - Stair climbing (common in urban India)
   - Skipping rope
   - No gym membership required

4. Traditional Activities:
   - Cycling (for transportation and exercise)
   - Dancing (Zumba, Bollywood dance)
   - Household chores (cleaning, gardening)
   - Playing with children

5. Resistance Training:
   - Bodyweight exercises
   - Resistance bands (affordable, portable)
   - Water bottles/household items as weights
   - 2-3 days/week, major muscle groups

Exercise Progression for Beginners:
Week 1-2: 15-20 min walking, light stretching
Week 3-4: 25-30 min walking, add 10 min bodyweight exercises
Week 5-8: 30-40 min walking, 15 min strength training, add yoga
Week 9-12: 40-60 min mixed cardio, 20-25 min strength, yoga

Safety Considerations:
- Medical clearance for BMI >35 or comorbidities
- Start slow, gradual progression
- Avoid exercise in extreme heat (common in India)
- Morning or evening exercise preferred
- Stay hydrated
- Proper footwear for walking

Barriers in Indian Context & Solutions:
- Heat: Exercise early morning or evening
- Lack of space: Home-based exercises, walking in neighborhoods
- Cultural norms (women): Women-only groups, home exercises
- Cost: Free activities (walking, bodyweight exercises)
- Time: Break into 10-15 min sessions throughout day

Monitoring Intensity:
- Talk test: Can talk but not sing
- Target heart rate: 60-70% of max (220 - age)
- RPE scale: 5-6 out of 10 for moderate intensity
""",
            metadata={"source": "Exercise Guidelines", "region": "India"}
        )
        documents.append(exercise_guidelines)

        # Lab Tests and Monitoring
        lab_tests = Document(
            page_content="""
Laboratory Tests and Monitoring for Obesity Management:

Initial Assessment (Baseline):
1. Fasting Blood Glucose (FBG) / HbA1c
   - Screen for diabetes/pre-diabetes
   - Cost: ₹50-150 (FBG), ₹300-500 (HbA1c)

2. Lipid Profile (Fasting)
   - Total cholesterol, LDL, HDL, triglycerides
   - Screen for dyslipidemia
   - Cost: ₹300-600

3. Thyroid Function Tests (TSH, T3, T4)
   - Rule out hypothyroidism
   - Cost: ₹400-800

4. Liver Function Tests (LFTs)
   - Screen for fatty liver disease
   - Cost: ₹400-700

5. Kidney Function Tests
   - Serum creatinine, urea, eGFR
   - Cost: ₹300-500

6. Complete Blood Count (CBC)
   - Screen for anemia, other abnormalities
   - Cost: ₹200-400

7. Vitamin D, B12 (optional but recommended)
   - Common deficiencies in India
   - Cost: ₹600-1000

8. Blood Pressure Measurement
   - Screen for hypertension
   - Free at clinics

9. Waist Circumference
   - Measure central obesity
   - Free

Total Cost for Initial Tests: ₹2,500-4,500

Follow-Up Monitoring:

Month 1:
- Weight, BMI, waist circumference
- Blood pressure
- Assess adherence, side effects

Month 3:
- Weight, BMI, waist circumference
- Repeat FBG/HbA1c (if abnormal at baseline)
- Lipid profile (if abnormal)
- Cost: ₹500-1000

Month 6:
- Full reassessment
- Repeat all baseline abnormal tests
- Consider liver function if on medications
- Cost: ₹1000-2000

Red Flags Requiring Immediate Medical Attention:
- Rapid weight gain with edema (fluid retention)
- Chest pain, shortness of breath
- Severe fatigue, dizziness
- Uncontrolled blood sugar (>200 mg/dL)
- Signs of depression or eating disorder

Success Criteria (at 3 months):
- Weight loss ≥ 5% of baseline
- Improved or stable lab parameters
- Adherence to lifestyle modifications
- No significant adverse effects
- Improved quality of life

If Not Meeting Goals:
- Reassess adherence
- Address barriers
- Consider intensifying intervention
- Evaluate for pharmacotherapy
- Rule out medical causes
""",
            metadata={"source": "Clinical Guidelines", "topic": "Lab Tests"}
        )
        documents.append(lab_tests)

        print(f"Created {len(documents)} medical knowledge documents")
        return documents

    def add_custom_documents(self, documents: List[Document]):
        """Add custom documents to the vector store"""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

        splits = text_splitter.split_documents(documents)
        self.vectorstore.add_documents(splits)

        print(f"Added {len(splits)} document chunks to vector store")


# Utility function for agents to use
def get_medical_context(query: str, rag_system: MedicalKnowledgeRAG, k: int = 3) -> str:
    """
    Get relevant medical context for a query
    Returns formatted string to include in agent context
    """
    results = rag_system.query_medical_knowledge(query, k=k)

    if not results:
        return "No relevant medical information found."

    context = "Relevant Medical Knowledge:\n\n"
    for i, doc in enumerate(results, 1):
        context += f"Source {i} ({doc.metadata.get('source', 'Unknown')}):\n"
        context += doc.page_content + "\n\n"

    return context


if __name__ == "__main__":
    # Initialize and create vector store
    rag = MedicalKnowledgeRAG()
    rag.create_medical_knowledge_base()

    # Test query
    print("\n" + "="*50)
    print("Testing RAG System")
    print("="*50 + "\n")

    query = "What medications are recommended for obesity with BMI 32?"
    print(f"Query: {query}\n")

    context = get_medical_context(query, rag, k=2)
    print(context)
