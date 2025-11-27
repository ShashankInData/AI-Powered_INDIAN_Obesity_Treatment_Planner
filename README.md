---
title: AI Obesity Treatment Planner
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.44.1
app_file: app.py
pinned: false
---

# 🏥 AI-Powered Obesity Treatment Planner for India

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A **comprehensive multi-agent AI system** for personalized obesity treatment planning, specifically designed for the **Indian healthcare context**. This system uses **5 specialized AI agents** working together with RAG-enhanced medical knowledge to create evidence-based, culturally appropriate treatment plans.

---

## 🎯 Why This Matters

India faces a growing obesity epidemic:
- **24% of women** and **22% of men** are overweight or obese
- Regional variations in diet, lifestyle, and healthcare access create unique challenges
- One-size-fits-all Western approaches don't account for Indian food culture and socioeconomic factors

**This tool bridges that gap** by providing:
- State-specific meal plans (Telangana: rice/jowar vs Punjab: roti/dal)
- Gender-aware recommendations based on Indian obesity data
- Cost-conscious medical advice with Indian Rupee estimates
- Culturally appropriate exercise plans (yoga, traditional activities)

---

## ✨ Key Features

### 🤖 Multi-Agent AI System
**5 specialized AI agents** collaborate to create comprehensive treatment plans:

1. **Data Analyst** - Analyzes health metrics, risk factors, and lifestyle patterns
2. **Dietician** - Creates 7-day personalized Indian meal plans
3. **Medical Advisor** - Evaluates medication needs and lab tests
4. **Fitness Trainer** - Designs progressive 4-week exercise programs
5. **Care Coordinator** - Synthesizes everything into a 30-day action plan

### 📊 Data-Driven & Evidence-Based
- **9,730 real patient records** from NFHS-5 (National Family Health Survey)
- **WHO obesity guidelines** (2023) with Asian BMI cutoffs
- **RAG (Retrieval Augmented Generation)** using ChromaDB vector database
- Medical research on Indian obesity patterns and regional variations

### 🇮🇳 India-Specific Intelligence
- **State-specific food databases** for all Indian states
- **Regional dietary patterns** (28 states + 8 UTs covered)
- **Vegetarian/Non-vegetarian/Semi-vegetarian** meal customization
- **Indian medication costs** (₹ prices for Orlistat, Metformin, GLP-1 agonists)
- **Urban/Rural context** for exercise recommendations
- **Wealth index awareness** for budget-appropriate suggestions

### 🎨 Modern User Experience
- **Gender selection** with Indian obesity statistics
- **Feet/inches input** (what people actually know, not cm!)
- **Color-coded BMI display** with Asian cutoffs:
  - 🟢 Green: Normal (18.5-23)
  - 🟡 Yellow: Overweight (23-27.5)
  - 🔴 Red: Obese (≥27.5)
- **Real-time BMI calculation** as you type
- **Smart vegetarian filter** (no chicken/fish for vegetarians!)
- **14 comprehensive input factors** for personalized plans

---

## 🚀 How It Works

### The Magic Behind the Scenes

```
📥 Your Input (14 factors)
    ↓
🤖 5 AI Agents Collaborate
    ↓
📚 RAG System Retrieves Relevant Knowledge
    ├─ WHO Guidelines
    ├─ Indian Medical Research
    ├─ 9,730 Similar Patient Cases
    ├─ State Food Databases
    └─ Medication Cost Data
    ↓
📋 Comprehensive Treatment Plan Generated
    ├─ 7-Day Meal Plan (State-Specific)
    ├─ 4-Week Exercise Program
    ├─ Medical Recommendations
    ├─ Cost Breakdown (₹)
    └─ 30-Day Action Plan
```

### What Makes This Different?

1. **Context-Aware RAG**: Not just generic AI responses - retrieves actual medical knowledge, similar patient outcomes, and regional data
2. **Multi-Agent Collaboration**: Each agent specializes in one domain, then they work together (like a real medical team!)
3. **Cultural Intelligence**: Knows that Maharashtra prefers rice while Punjab prefers roti, that vegetarian means NO fish/chicken/eggs
4. **Cost-Conscious**: Every recommendation includes Indian market prices in Rupees (₹)
5. **Gender-Specific**: Tailors approach based on how obesity manifests differently in Indian men vs women

---

## 📋 Input Factors (14 Total)

The AI analyzes **all 14 factors** to create your personalized plan:

### Personal Information
- Name (optional, for personalization)
- **Age** (18-80 years)
- **Gender** (Female/Male) - New! Based on Indian obesity data

### Physical Metrics
- **Height** (feet/inches - user-friendly!)
- **Weight** (kg)
- **BMI** (auto-calculated with color coding)

### Dietary Preferences
- **Vegetarian/Non-vegetarian/Semi-vegetarian**
- Smart filtering ensures veg plans have NO non-veg items!

### Lifestyle & Activity
- **Do you walk/exercise?** (Yes/No/Don't Know)
- **Daily steps** (Sedentary to Very Active)
- **Smoking status** (affects metabolism)
- **Alcohol consumption** (affects calorie intake)

### Location & Demographics
- **State** (all 28 states + 8 UTs)
- **Residence** (Urban/Rural)
- **Wealth Index** (for budget-appropriate plans)

---

## 🎓 How We Built This

### The Technology Stack

- **CrewAI** - Multi-agent orchestration framework
- **OpenAI GPT-4o** - Powers the 5 AI agents
- **LangChain** - RAG (Retrieval Augmented Generation) framework
- **ChromaDB** - Vector database for medical knowledge embeddings
- **Sentence Transformers** - Text embeddings for semantic search
- **Gradio 4.44.1** - Modern web interface
- **Pandas** - Data processing for 9,730 patient records

### The Knowledge Base

**Pre-indexed medical knowledge** in ChromaDB vector database:

1. **WHO Obesity Guidelines (2023)**
   - Asian BMI cutoffs (different from Western standards)
   - Treatment protocols
   - Comorbidity management

2. **Indian Medical Research**
   - Obesity prevalence by state and gender
   - Regional dietary patterns
   - Cultural considerations

3. **Medication Database**
   - Orlistat, Metformin, Semaglutide, Liraglutide
   - Dosages, side effects, contraindications
   - **Indian market costs** (₹100-20,000/month)

4. **9,730 NFHS-5 Patient Records**
   - Real anonymized data
   - Used for similarity search (find patients like you)
   - Provides evidence-based outcomes

5. **State Food Databases (All 36 Regions)**
   - Staple foods, traditional dishes
   - Protein sources (veg/non-veg differentiated)
   - Local vegetables, foods to avoid
   - Regional cooking methods

### The Architecture

```python
# Simplified version of how it works:

1. User Input → Validate & Calculate BMI
2. Get State Food Context (Telangana vs Punjab vs Kerala)
3. Pass to 5 AI Agents Sequentially:

   Agent 1 (Data Analyst):
   - Analyzes health metrics + lifestyle
   - Identifies risk factors
   → Output feeds into Agent 2

   Agent 2 (Dietician):
   - Retrieves state foods from ChromaDB
   - Creates 7-day meal plan
   - Filters by veg/non-veg preference
   → Output feeds into Agent 3

   Agent 3 (Medical Advisor):
   - Retrieves WHO guidelines from ChromaDB
   - Evaluates medication needs
   - Recommends lab tests with costs
   → Output feeds into Agent 4

   Agent 4 (Fitness Trainer):
   - Retrieves exercise protocols
   - Designs 4-week progressive plan
   - Adjusts for urban/rural context
   → Output feeds into Agent 5

   Agent 5 (Care Coordinator):
   - Synthesizes all recommendations
   - Creates 30-day action plan
   - Calculates total costs
   → Final comprehensive plan!
```

---

## 💡 Cool Features You'll Love

### 1. Real-Time BMI Color Coding
As you adjust height/weight, BMI updates instantly with color-coded visual feedback:
- 🟢 **Green** - You're in the healthy range!
- 🟡 **Yellow** - Slightly overweight, let's optimize
- 🔴 **Red** - Significant weight to lose, we'll help!

### 2. Smart Vegetarian Filter
**The Problem**: Old version showed "Fish, Chicken" for vegetarians
**The Solution**: Sophisticated filtering logic
```python
# Only shows veg proteins for vegetarians:
vegetarian_proteins = ['Lentils', 'Dal', 'Paneer', 'Curd',
                       'Buttermilk', 'Tofu', 'Soy',
                       'Chickpeas', 'Beans']
```

### 3. Gender-Aware Recommendations
**Why it matters**:
- Women in India face higher obesity rates (24% vs 22%)
- Different hormonal factors, pregnancy/postpartum considerations
- Social/cultural factors around food and exercise

**What the AI does**:
- Tailors meal portions and macros
- Adjusts exercise intensity and type
- Considers gender-specific health risks

### 4. State Food Intelligence
**Example**: If you're from Telangana:
- **Staples**: Rice, Jowar, Bajra (NOT wheat roti!)
- **Traditional Dishes**: Pesarattu, Pulihora, Gongura
- **Proteins**: Mutton, Chicken, Lentils
- **Recommendations**: "Use less oil in sambar, steam idlis instead of frying dosas"

### 5. Cost Transparency
Every recommendation includes costs:
- **Meal Plan**: Weekly grocery cost (₹)
- **Medications**: Monthly cost (₹100-20,000 depending on type)
- **Lab Tests**: ₹2,500-4,500 for initial assessment
- **Equipment**: If needed (yoga mat, resistance bands)

### 6. 🎲 Load Sample Patient Button
Test with pre-loaded NFHS data to see the system in action!

---

## 📊 What You Get

Your personalized treatment plan includes:

### 📋 Treatment Plan Tab
- Executive summary with your goals
- Week-by-week action plan (Weeks 1-4)
- Integrated diet + exercise + medical recommendations
- Success metrics and monitoring schedule
- Patient checklist (top 5 actions to start NOW)

### 🍛 Regional Food Guide Tab
- Your state-specific food recommendations
- 7-day meal plan with exact portions
- Calorie/macro breakdown
- Shopping list with costs
- Meal prep tips

### 🔍 Agent Logs Tab
- See what each AI agent is thinking!
- Transparency into how decisions are made
- Technical details for the curious

---

## 💰 Cost Information

### To Run This App
- **Per Treatment Plan**: ~$0.30-0.50 (OpenAI GPT-4o API costs)
- **Time**: 1-3 minutes to generate comprehensive plan

### For Users (Estimated Costs in ₹)
- **Monthly Food Costs**: Included in meal plans
- **Medications** (if recommended):
  - Orlistat: ₹2,000-5,000/month
  - Metformin: ₹100-500/month
  - GLP-1 agonists (Semaglutide): ₹15,000-20,000/month
- **Lab Tests**: ₹2,500-4,500 (one-time initial assessment)
- **Exercise Equipment**: ₹500-2,000 (yoga mat, resistance bands)

---

## 🛠️ For Developers: Local Setup

### Prerequisites
```bash
Python 3.9+
OpenAI API Key
```

### Installation

1. **Clone the repository**
```bash
git clone https://huggingface.co/spaces/[YOUR-USERNAME]/obesity-treatment-planner
cd obesity-treatment-planner
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
Create a `.env` file:
```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o
```

4. **Run the app**
```bash
python app.py
```

The interface will open at `http://localhost:7860`

---

## 📁 Project Structure

```
obesity_multi_agent/
├── app.py                          # Main Gradio application
├── crew.py                         # Multi-agent orchestration
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
│
├── agents/                         # 5 AI Agent definitions
│   ├── data_analyst_agent.py
│   ├── dietician_agent.py
│   ├── medical_advisor_agent.py
│   ├── fitness_trainer_agent.py
│   └── care_coordinator_agent.py
│
├── tasks/                          # Task definitions
│   └── all_tasks.py                # All 5 agent tasks
│
├── tools/                          # Custom tools
│   ├── medical_knowledge_rag.py    # RAG for medical knowledge
│   ├── patient_data_indexer.py     # Patient similarity search
│   ├── patient_data_tool.py        # NFHS data loader
│   └── rag_tool.py                 # RAG integration
│
├── config/                         # Configuration
│   ├── agents.yaml                 # Agent configurations
│   └── tasks.yaml                  # Task configurations
│
├── data/                           # Patient data
│   └── indian_obesity_data_clean.csv  # 9,730 NFHS-5 records
│
└── chroma_db/                      # Vector database (pre-built)
    ├── Medical knowledge embeddings
    └── Patient data embeddings
```

---

## 🎯 Use Cases

### For Patients
- Get personalized, culturally appropriate obesity treatment plans
- Understand your health metrics with clear visual feedback
- Access evidence-based recommendations for free
- Learn about costs before committing to treatments

### For Healthcare Providers
- Supplement patient consultations with AI-generated plans
- Save time on initial assessment and plan creation
- Ensure cultural appropriateness of recommendations
- Provide cost-transparent options to patients

### For Researchers
- Analyze patterns in 9,730 real patient records
- Study effectiveness of culturally tailored interventions
- Explore multi-agent AI architectures for healthcare
- Benchmark different treatment approaches

### For Developers
- Learn CrewAI multi-agent systems
- Understand RAG implementation with ChromaDB
- See production-ready Gradio UI patterns
- Study healthcare AI application architecture

---

## ⚠️ Important Disclaimers

### Medical Disclaimer
This system is for **educational and informational purposes only**. It is NOT:
- A substitute for professional medical advice
- A diagnostic tool
- A prescription service
- A replacement for in-person healthcare

**Always consult qualified healthcare professionals** before:
- Starting any weight loss program
- Taking new medications
- Making significant diet/exercise changes
- If you have underlying health conditions

### Data Privacy
- Patient input data is logged **anonymously** for analytics
- **No names** are stored in logs
- Data stays local to this application
- Complies with privacy best practices

### AI Limitations
- Recommendations are based on general medical knowledge
- May not account for your specific medical history
- Cannot see your lab results or perform examinations
- Should be validated by real healthcare providers

---

## 🔒 Security & Privacy

### API Key Security
- **NEVER** commit `.env` file to Git
- Use Hugging Face Spaces Secrets for deployment
- API keys are excluded via `.gitignore`

### Data Handling
- Patient names are optional and not logged
- Only anonymized metrics are saved
- Logs stored locally, not shared
- NFHS data is already de-identified

### Sensitive Files Excluded
The `.gitignore` ensures these are never uploaded:
- `.env` (API keys)
- `logs/` (user data)
- `chroma_db/` (vector database - too large)
- `.venv/` (virtual environment)

---

## 🌟 What's New (Latest Version)

### ✨ Major Improvements
1. **Gender Selection** - Male/Female with Indian obesity statistics
2. **BMI Color Coding** - Visual feedback with Asian cutoffs
3. **Feet/Inches Input** - User-friendly height entry
4. **Smart Vegetarian Filter** - NO non-veg for vegetarian users!
5. **All 14 Factors to AI** - Complete data integration
6. **Real-time BMI Calculation** - Updates as you type
7. **Enhanced Error Handling** - Graceful failures with helpful messages

### 🐛 Bug Fixes
- Fixed vegetarian filter showing non-veg proteins
- Fixed BMI calculation using Asian cutoffs (not Western)
- Fixed height input UX (feet/inches > cm)
- Fixed event handlers for Gradio 4.44.1 compatibility
- Fixed dependency conflicts (huggingface-hub version)

---

## 📚 Learn More

### About the Data
- **NFHS-5**: National Family Health Survey (2019-21)
- **Sample Size**: 9,730 de-identified patient records
- **Coverage**: All Indian states and UTs
- **Metrics**: BMI, age, residence, socioeconomic status

### About the AI
- **Model**: OpenAI GPT-4o (128k context, multimodal)
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB (open-source, Python-native)
- **Framework**: CrewAI (multi-agent orchestration)

### About Obesity in India
- **Prevalence**: 24% women, 22% men (NFHS-5)
- **Urban vs Rural**: Higher in urban areas
- **State Variations**: Kerala (highest), Bihar (lowest)
- **Health Impact**: Leading cause of diabetes, heart disease

---

## 🤝 Contributing

This is an open educational project. Improvements welcome!

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Test locally
4. Update documentation
5. Submit pull request

### Areas for Improvement
- Additional languages (Hindi, Tamil, etc.)
- More states in food database
- Integration with wearable devices
- Progress tracking over time
- Community features (support groups)

---

## 📞 Support & Feedback

### Issues or Questions?
- **Hugging Face Discussions**: Use the Community tab
- **GitHub Issues**: Report bugs or request features
- **Documentation**: Check this README first

### Acknowledgments
- **NFHS-5**: For providing open patient data
- **WHO**: For obesity guidelines and research
- **CrewAI**: For the multi-agent framework
- **Hugging Face**: For hosting infrastructure
- **Indian Medical Research Community**: For regional insights

---

## 📜 License

This project is licensed under the **MIT License** - see LICENSE file for details.

Free to use, modify, and distribute with attribution.

---

## 📊 Statistics

- **9,730** patient records analyzed
- **36** Indian regions covered (28 states + 8 UTs)
- **5** specialized AI agents
- **14** input factors considered
- **4** weeks of exercise programming
- **7** days of meal planning
- **30** days of integrated action planning

---

## 🎓 Citation

If you use this project in research or education, please cite:

```bibtex
@software{ai_obesity_planner_2024,
  title={AI-Powered Obesity Treatment Planner for India},
  author={[Shashank_Bodapati]},
  year={2025},
  url={https://huggingface.co/spaces/[ShashhankIndata]/obesity-treatment-planner},
  note={Multi-agent AI system for culturally appropriate obesity treatment planning}
}
```

---

## 🚀 Future Roadmap

- [ ] Multi-language support (Hindi, Tamil, Telugu, Bengali)
- [ ] Progress tracking dashboard
- [ ] Integration with health wearables
- [ ] Community support features
- [ ] Telemedicine integration
- [ ] Nutritional analysis from food photos
- [ ] Recipe database with calorie information
- [ ] Mental health support integration

---

**Built with ❤️ for India's health**

**Version**: 2.0.0
**Last Updated**: November 2024
**Status**: ✅ Production Ready

---

**Ready to get healthy?** Click "Use this Space" above to start your personalized treatment plan! 🏥
