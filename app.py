"""
Modern UI for AI Obesity Treatment System - Gradio 4.44.1
Complete redesign with state-specific food recommendations and dietary preferences
"""

import gradio as gr
import pandas as pd
from crew import ObesityTreatmentCrew
from tools.patient_data_tool import PatientDataLoader, STATE_MAPPING
import sys
from io import StringIO
import datetime
import os
import csv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# USAGE LOGGING SYSTEM
# ============================================================================

def log_patient_input(patient_data):
    """
    Log patient inputs to CSV for analytics (anonymized)
    Saves: timestamp, age, BMI, state, lifestyle factors (NO names)
    """
    try:
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)

        log_file = logs_dir / "patient_usage.csv"
        file_exists = log_file.exists()

        with open(log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'timestamp', 'patient_id', 'age', 'gender', 'height_cm', 'weight_kg', 'bmi',
                'bmi_category', 'state', 'residence', 'wealth_index', 'diet_preference',
                'physical_activity', 'daily_steps', 'smoking_status', 'alcohol_consumption'
            ])

            if not file_exists:
                writer.writeheader()

            # Log only anonymized data (NO patient name)
            log_entry = {
                'timestamp': datetime.datetime.now().isoformat(),
                'patient_id': patient_data.get('patient_id', 'unknown'),
                'age': patient_data.get('age', ''),
                'gender': patient_data.get('gender', ''),
                'height_cm': patient_data.get('height_cm', ''),
                'weight_kg': patient_data.get('weight_kg', ''),
                'bmi': patient_data.get('bmi', ''),
                'bmi_category': patient_data.get('bmi_category', ''),
                'state': patient_data.get('state', ''),
                'residence': patient_data.get('residence_type', ''),
                'wealth_index': patient_data.get('wealth_index', ''),
                'diet_preference': patient_data.get('dietary_preference', ''),
                'physical_activity': patient_data.get('physical_activity', ''),
                'daily_steps': patient_data.get('daily_steps', ''),
                'smoking_status': patient_data.get('smoking_status', ''),
                'alcohol_consumption': patient_data.get('alcohol_consumption', '')
            }

            writer.writerow(log_entry)
            print(f"[LOG] Patient input logged: {patient_data.get('patient_id')}")

    except Exception as e:
        print(f"[WARNING] Failed to log patient input: {str(e)}")

# ============================================================================
# STATE-SPECIFIC FOOD DATABASE
# ============================================================================

STATE_FOOD_DATABASE = {
    "Telangana": {
        "staples": ["Rice", "Jowar", "Bajra"],
        "typical_dishes": ["Hyderabadi biryani", "Pesarattu", "Sarva pindi", "Jonna rotte"],
        "proteins": ["Mutton", "Chicken", "Lentils"],
        "vegetables": ["Gongura", "Brinjal", "Beans", "Ridge gourd"],
        "avoid": ["Excess oil in biryani", "Deep-fried pakoras", "Heavy cream-based curries"],
        "recommendations": {
            "Vegetarian": "Replace white rice with brown rice or jowar. Increase dal portions. Reduce oil in preparations.",
            "Non-vegetarian": "Grilled chicken over biryani. Reduce portion sizes. Avoid fried preparations.",
            "Semi-vegetarian": "Dal-based meals 4 days/week. Grilled meats 2-3 days. Focus on jowar rotis instead of white rice."
        }
    },
    "Andhra Pradesh": {
        "staples": ["Rice", "Ragi", "Jowar"],
        "typical_dishes": ["Pesarattu", "Pulihora", "Pappu", "Gongura"],
        "proteins": ["Lentils", "Fish", "Chicken"],
        "vegetables": ["Brinjal", "Okra", "Ridge gourd", "Drumstick"],
        "avoid": ["Excessive oil in curries", "Deep-fried pickles", "Excess ghee in sweets"],
        "recommendations": {
            "Vegetarian": "Ragi dosa, steamed idli, lentil curries with reduced oil in sambar.",
            "Non-vegetarian": "Grilled fish with minimal oil, chicken curry with reduced coconut, tandoori preparations.",
            "Semi-vegetarian": "Dal preparations and grilled fish twice weekly, avoid fried fish."
        }
    },
    "Maharashtra": {
        "staples": ["Rice", "Wheat (chapati)", "Jowar", "Bajra"],
        "typical_dishes": ["Bhakri", "Pithla", "Varan bhaat", "Misal pav"],
        "proteins": ["Lentils", "Chicken", "Fish", "Mutton"],
        "vegetables": ["Bhendi", "Palak", "Methi", "Cabbage"],
        "avoid": ["Excess oil in misal", "Deep-fried vada pav", "Heavy peanut-based chutneys"],
        "recommendations": {
            "Vegetarian": "Multigrain bhakri, steamed dhokla, reduce oil in thalipeeth, increase salad intake.",
            "Non-vegetarian": "Grilled bombil (Bombay duck), tandoori chicken, reduce mutton frequency.",
            "Semi-vegetarian": "Vegetarian meals 5 days/week with fish 2 days, focus on jowar."
        }
    },
    "Tamil Nadu": {
        "staples": ["Rice", "Ragi", "Kambu"],
        "typical_dishes": ["Idli", "Dosa", "Sambar", "Rasam", "Curd rice"],
        "proteins": ["Lentils", "Fish", "Chicken"],
        "vegetables": ["Drumstick", "Snake gourd", "Ash gourd", "Banana stem"],
        "avoid": ["Excess oil in dosa", "Deep-fried vada", "Sugar-laden payasam"],
        "recommendations": {
            "Vegetarian": "Ragi idli, steamed pongal, increase sambar vegetables, reduce coconut oil.",
            "Non-vegetarian": "Fish curry with minimal oil, grilled chicken, chettinad style with spices not oil.",
            "Semi-vegetarian": "Fish preparations 3 times weekly, focus on steamed preparations."
        }
    },
    "Kerala": {
        "staples": ["Rice", "Tapioca", "Wheat"],
        "typical_dishes": ["Appam", "Puttu", "Fish curry", "Thoran", "Avial"],
        "proteins": ["Fish", "Chicken", "Lentils", "Coconut"],
        "vegetables": ["Plantain", "Yam", "Beans", "Drumstick"],
        "avoid": ["Excess coconut oil", "Heavy coconut milk curries", "Fried banana chips"],
        "recommendations": {
            "Vegetarian": "Steamed puttu with kadala curry, reduce coconut in avial, increase vegetable thoran.",
            "Non-vegetarian": "Fish moilee with reduced coconut milk, grilled fish, avoid fried preparations.",
            "Semi-vegetarian": "Fish 3-4 times weekly, reduce coconut oil, focus on steamed dishes."
        }
    },
    "Karnataka": {
        "staples": ["Rice", "Ragi", "Jowar"],
        "typical_dishes": ["Ragi mudde", "Bisi bele bath", "Jolada rotti", "Akki roti"],
        "proteins": ["Lentils", "Chicken", "Fish"],
        "vegetables": ["Carrot", "Beans", "Palya vegetables"],
        "avoid": ["Excess ghee in bisi bele bath", "Deep-fried bonda", "Heavy oil in curries"],
        "recommendations": {
            "Vegetarian": "Ragi mudde with sambar, increase vegetable palya, reduce ghee.",
            "Non-vegetarian": "Grilled chicken, fish curry with minimal oil, tandoori preparations.",
            "Semi-vegetarian": "Ragi-based meals with fish twice weekly, focus on millets."
        }
    },
    "Gujarat": {
        "staples": ["Wheat (rotli)", "Bajra", "Jowar"],
        "typical_dishes": ["Dhokla", "Khichdi", "Thepla", "Undhiyu"],
        "proteins": ["Lentils", "Buttermilk", "Curd"],
        "vegetables": ["Bottle gourd", "Ridge gourd", "Fenugreek", "Cluster beans"],
        "avoid": ["Excess sugar in dishes", "Deep-fried farsans", "Heavy ghee usage"],
        "recommendations": {
            "Vegetarian": "Steamed dhokla, reduce sugar in dal, multigrain rotli, increase raw salads.",
            "Non-vegetarian": "Not typically applicable - focus on protein from dal and dairy.",
            "Semi-vegetarian": "Maintain vegetarian base, add fish once weekly for coastal regions."
        }
    },
    "Punjab": {
        "staples": ["Wheat (roti)", "Rice", "Makki (corn)"],
        "typical_dishes": ["Makki ki roti", "Sarson da saag", "Dal makhani", "Chole"],
        "proteins": ["Lentils", "Chicken", "Paneer", "Curd"],
        "vegetables": ["Spinach", "Mustard greens", "Radish", "Onions"],
        "avoid": ["Excess butter/ghee", "Heavy cream in dal", "Deep-fried pakoras"],
        "recommendations": {
            "Vegetarian": "Reduce butter in saag, use low-fat paneer, increase salad portions.",
            "Non-vegetarian": "Tandoori chicken without cream, reduce butter chicken frequency.",
            "Semi-vegetarian": "Dal-based meals 4-5 days, grilled chicken 2-3 days, reduce dairy fats."
        }
    },
    "West Bengal": {
        "staples": ["Rice", "Wheat"],
        "typical_dishes": ["Fish curry", "Luchi", "Posto", "Shukto"],
        "proteins": ["Fish", "Lentils", "Eggs"],
        "vegetables": ["Bitter gourd", "Pumpkin", "Plantain", "Potato"],
        "avoid": ["Excess mustard oil in fish curry", "Deep-fried luchi", "Heavy sweets"],
        "recommendations": {
            "Vegetarian": "Shukto without excess oil, steamed vegetables, reduce potato usage.",
            "Non-vegetarian": "Steamed fish, reduce oil in curry, avoid fried fish.",
            "Semi-vegetarian": "Fish 4-5 times weekly, reduce oil, focus on steamed preparations."
        }
    },
    "Rajasthan": {
        "staples": ["Wheat (roti)", "Bajra", "Jowar"],
        "typical_dishes": ["Dal baati churma", "Gatte ki sabzi", "Ker sangri"],
        "proteins": ["Lentils", "Buttermilk", "Mutton (occasional)"],
        "vegetables": ["Beans", "Ker berries", "Sangri beans"],
        "avoid": ["Excess ghee in baati", "Deep-fried preparations", "Heavy sugar in churma"],
        "recommendations": {
            "Vegetarian": "Reduce ghee in dal baati, increase green vegetables, multigrain rotis.",
            "Non-vegetarian": "Reduce mutton frequency, focus on lentil proteins.",
            "Semi-vegetarian": "Primarily vegetarian with occasional lean meat, focus on bajra."
        }
    },
    "Delhi": {
        "staples": ["Wheat (roti)", "Rice"],
        "typical_dishes": ["Chole bhature", "Parathas", "Street food"],
        "proteins": ["Paneer", "Chicken", "Lentils"],
        "vegetables": ["Mixed vegetables", "Cauliflower", "Peas"],
        "avoid": ["Deep-fried bhature", "Excess butter in parathas", "Heavy street food"],
        "recommendations": {
            "Vegetarian": "Steamed preparations over fried, reduce paneer frequency, increase salads.",
            "Non-vegetarian": "Grilled chicken, tandoori items, reduce curry richness.",
            "Semi-vegetarian": "Balance with 3-4 vegetarian days, focus on grilled preparations."
        }
    }
}

# Add default for states not in database
DEFAULT_STATE_DATA = {
    "staples": ["Rice", "Wheat", "Millets"],
    "typical_dishes": ["Regional variations of Indian cuisine"],
    "proteins": ["Lentils", "Chicken", "Fish"],
    "vegetables": ["Seasonal local vegetables"],
    "avoid": ["Excess oil and ghee", "Deep-fried foods", "Refined sugars"],
    "recommendations": {
        "Vegetarian": "Focus on whole grains, increase vegetables, reduce oil, add protein from lentils and dairy.",
        "Non-vegetarian": "Grilled/baked meats, fish 2-3 times weekly, reduce red meat, avoid fried preparations.",
        "Semi-vegetarian": "Vegetarian meals 4-5 days with fish/chicken 2-3 days, focus on whole grains."
    }
}

# ============================================================================
# CUSTOM CSS FOR MODERN UI
# ============================================================================

CUSTOM_CSS = """
/* Modern Medical UI Theme */
.gradio-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Card styling */
.input-section {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border: 1px solid #e1e8ed;
}

/* Section headers */
.section-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #0066cc;
}

/* Info boxes */
.info-box {
    background: #e8f4fd;
    border-left: 4px solid #0066cc;
    padding: 1rem;
    border-radius: 6px;
    margin: 1rem 0;
}

.warning-box {
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 1rem;
    border-radius: 6px;
    margin: 1rem 0;
}

/* Primary button styling */
.primary-btn button {
    background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 0.75rem 2rem !important;
    font-size: 1.05rem !important;
}
"""

# ============================================================================
# MODERN GRADIO INTERFACE
# ============================================================================

class ModernGradioInterface:
    """Modern Gradio interface with enhanced UX"""

    def __init__(self):
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found")
        self.crew = None
        self.data_loader = None
        print("Modern UI initialized (lazy loading)")

    def _ensure_initialized(self):
        """Lazy initialization"""
        if self.crew is None:
            print("Initializing AI crew...")
            self.crew = ObesityTreatmentCrew()
        if self.data_loader is None:
            print("Loading patient data...")
            self.data_loader = PatientDataLoader()

    def calculate_bmi(self, weight_kg, height_cm):
        """Calculate BMI with proper None handling"""
        try:
            # Handle None, empty string, or invalid values
            if weight_kg is None or weight_kg == "" or float(weight_kg) <= 0:
                return 0.0, "Invalid"
            if height_cm is None or height_cm == "" or float(height_cm) <= 0:
                return 0.0, "Invalid"

            weight_kg = float(weight_kg)
            height_cm = float(height_cm)

            height_m = height_cm / 100
            bmi = weight_kg / (height_m ** 2)

            # Asian BMI cutoffs
            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi < 23.0:
                category = "Normal"
            elif 23.0 <= bmi < 27.5:
                category = "Overweight"
            else:
                category = "Obese"

            return round(bmi, 2), category
        except (ValueError, TypeError, ZeroDivisionError):
            return 0.0, "Invalid"

    def cm_to_feet_inches(self, cm):
        """Convert cm to feet and inches"""
        try:
            if cm is None or cm == "" or float(cm) <= 0:
                return 0, 0.0
            cm = float(cm)
            total_inches = cm / 2.54
            feet = int(total_inches // 12)
            inches = round(total_inches % 12, 1)
            return feet, inches
        except (ValueError, TypeError):
            return 0, 0.0

    def feet_inches_to_cm(self, feet, inches):
        """Convert feet and inches to cm"""
        try:
            feet = float(feet) if feet is not None and feet != "" else 0
            inches = float(inches) if inches is not None and inches != "" else 0
            total_inches = (feet * 12) + inches
            return round(total_inches * 2.54, 1)
        except (ValueError, TypeError):
            return 0.0

    def get_state_food_recommendations(self, state, diet_pref):
        """Get state-specific food recommendations"""
        state_data = STATE_FOOD_DATABASE.get(state, DEFAULT_STATE_DATA)

        recommendation_text = state_data['recommendations'].get(diet_pref,
                                state_data['recommendations'].get('Vegetarian', ''))

        output = f"""
### 🍛 State-Specific Dietary Recommendations: {state}

**Your Dietary Preference:** {diet_pref}

#### Typical Staples in {state}:
{', '.join(state_data['staples'])}

#### Traditional Dishes:
{', '.join(state_data['typical_dishes'])}

#### Recommended Protein Sources ({diet_pref}):
{', '.join([p for p in state_data['proteins'] if (diet_pref == 'Non-vegetarian' or diet_pref == 'Semi-vegetarian' or p in ['Lentils', 'Dal', 'Paneer', 'Curd', 'Buttermilk', 'Tofu', 'Soy', 'Chickpeas', 'Beans'])])}

#### Local Vegetables:
{', '.join(state_data['vegetables'])}

---

### ⚠️ Foods to AVOID:
{chr(10).join(['• ' + item for item in state_data['avoid']])}

---

### ✅ Recommended Approach ({diet_pref}):
{recommendation_text}

---

### 📊 Daily Intake Guidelines:

**Sugar Limit:**
• Maximum: 25g/day (6 teaspoons)
• Reduce in tea/coffee
• Avoid sugary drinks and packaged juices
• Check food labels for hidden sugars

**Salt Limit:**
• Maximum: 5g/day (1 teaspoon)
• Use herbs and spices for flavor
• Avoid processed/packaged foods
• Don't add salt at the table

**Hydration:**
• Drink 8-10 glasses of water daily
• Avoid sweetened beverages
• Include buttermilk, coconut water
"""
        return output

    def generate_treatment_plan(
        self,
        name, age, gender, height_cm, weight, diet_preference,
        does_walking, daily_steps, smoking_status, alcohol_consumption,
        state, residence_type, wealth_index,
        progress=gr.Progress()
    ):
        """Generate comprehensive treatment plan"""

        try:
            # Show loading animation immediately
            loading_msg = """
<div style="text-align: center; padding: 60px 40px;">
    <div style="display: inline-flex; gap: 8px; margin-bottom: 20px;">
        <div style="width: 12px; height: 12px; border-radius: 50%; background: #2563eb; animation: pulse 1.5s ease-in-out infinite;"></div>
        <div style="width: 12px; height: 12px; border-radius: 50%; background: #2563eb; animation: pulse 1.5s ease-in-out 0.2s infinite;"></div>
        <div style="width: 12px; height: 12px; border-radius: 50%; background: #2563eb; animation: pulse 1.5s ease-in-out 0.4s infinite;"></div>
    </div>
    <p style="color: #64748b; font-size: 16px; font-weight: 500; margin: 0;">AI agents are analyzing your profile...</p>
    <p style="color: #94a3b8; font-size: 13px; margin: 8px 0 0 0;">This usually takes 1-3 minutes</p>
</div>

<style>
@keyframes pulse {
    0%, 100% { opacity: 0.3; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.2); }
}
</style>
"""

            # Validate inputs
            if not height_cm or not weight or not age:
                return "❌ Error: Please fill all required fields", "", ""

            height_cm = float(height_cm)
            weight = float(weight)
            age = int(age)

            if height_cm <= 0 or weight <= 0 or age < 18:
                return "❌ Error: Invalid height, weight, or age values", "", ""

            progress(0.05, desc="Initializing...")

            # Return loading message while processing starts
            yield loading_msg, "", ""

            self._ensure_initialized()

            # Calculate BMI
            bmi, bmi_category = self.calculate_bmi(weight, height_cm)

            if bmi == 0.0:
                return "❌ Error: Invalid BMI calculation", "", ""

            progress(0.1, desc="Analyzing patient data...")

            # Get food recommendations
            food_recommendations = self.get_state_food_recommendations(state, diet_preference)

            # Create patient data
            feet, inches = self.cm_to_feet_inches(height_cm)
            patient_data = {
                "patient_id": f"HF_USER_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "patient_name": name if name and name.strip() else "Anonymous",
                "age": age,
                "gender": gender,
                "height_cm": height_cm,
                "weight_kg": weight,
                "bmi": bmi,
                "bmi_category": bmi_category,
                "state": state,
                "residence_type": residence_type,
                "wealth_index": wealth_index,
                "dietary_preference": diet_preference,
                "location_context": f"{residence_type} area in {state}",
                "socioeconomic_status": wealth_index,
                # Lifestyle factors
                "physical_activity": does_walking,
                "daily_steps": daily_steps,
                "smoking_status": smoking_status,
                "alcohol_consumption": alcohol_consumption,
            }

            # Log patient input (anonymized - no name)
            log_patient_input(patient_data)

            progress(0.3, desc="AI agents analyzing...")

            # Capture agent output
            captured_output = StringIO()
            sys.stdout = captured_output

            try:
                result = self.crew.create_treatment_plan(patient_data)
                progress(1.0, desc="Complete!")
            finally:
                sys.stdout = sys.__stdout__

            agent_logs = captured_output.getvalue()
            treatment_plan = str(result)

            # Format summary
            name_display = f"**Patient:** {patient_data['patient_name']}\n" if patient_data['patient_name'] != "Anonymous" else ""

            summary = f"""
# 📋 Patient Summary

{name_display}**ID:** {patient_data['patient_id']}
**Age:** {age} years | **Height:** {height_cm} cm ({feet}' {inches}") | **Weight:** {weight} kg
**BMI:** {bmi} ({bmi_category}) | **Location:** {state}, {residence_type}
**Dietary Preference:** {diet_preference} | **Socioeconomic Status:** {wealth_index}

---

# 🤖 AI-Generated Comprehensive Treatment Plan

{treatment_plan}
"""

            yield summary, food_recommendations, agent_logs

        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            import traceback
            traceback.print_exc()
            yield error_msg, "", str(e)

    def create_interface(self):
        """Create modern Gradio interface"""

        state_options = sorted(list(STATE_MAPPING.values()))

        # Gradio 6.x doesn't accept css parameter, only title
        with gr.Blocks(title="AI Obesity Treatment Planner") as interface:

            # Header
            gr.Markdown("""
            # 🏥 AI-Powered INDIAN Obesity Treatment Planner
            ### Personalized Treatment Plans with Regional Dietary Insights

            **5 Specialized AI Agents** working together with **WHO Guidelines** + **9,730 Patient Records** + **State-Specific Food Culture**
            """, elem_id="header")

            with gr.Row():
                gr.HTML('<div class="info-box">📊 <strong>Data-Driven:</strong> Evidence-based recommendations from medical research</div>')
                gr.HTML('<div class="info-box">🍛 <strong>Cultural:</strong> State-specific meal plans (e.g., Telangana: rice/jowar, not roti)</div>')
                gr.HTML('<div class="info-box">🤖 <strong>AI-Powered:</strong> Multi-agent system for comprehensive analysis</div>')

            # Main content
            with gr.Row():
                # LEFT: Inputs
                with gr.Column(scale=1):

                    gr.HTML('<div class="section-header">👤 Personal Information</div>')
                    name_input = gr.Textbox(label="Patient Name (Optional)", placeholder="Enter name...")
                    age_input = gr.Number(value=35, label="Age (years)", minimum=18, maximum=80, step=1)

                    gender_input = gr.Radio(
                        choices=["Female", "Male"],
                        value="Female",
                        label="Gender",
                        info="📊 In India, obesity rates are higher in women (24%) vs men (22%)"
                    )

                    gr.HTML('<div class="section-header">📏 Height & Weight</div>')

                    gr.Markdown("**Height** *(Most people know their height in feet/inches)*")
                    with gr.Row():
                        feet_input = gr.Number(label="Feet", minimum=3, maximum=8, step=1, value=5)
                        inches_input = gr.Number(label="Inches", minimum=0, maximum=11.9, step=0.1, value=3)

                    # Hidden CM field for calculations
                    height_cm_input = gr.Number(value=160, label="Height (cm) - auto-calculated", minimum=100, maximum=250, visible=False)

                    weight_input = gr.Number(value=75, label="Weight (kg)", minimum=30, maximum=200)

                    gr.HTML('<div class="section-header">📊 Your BMI</div>')
                    bmi_display = gr.HTML(value="""<div style="padding: 15px; text-align: center; border-radius: 8px; background: #fef9c3;">
                    <div style="font-size: 32px; font-weight: bold; color: #854d0e;">29.30</div>
                    <div style="font-size: 16px; color: #854d0e; margin-top: 5px;">⚠️ Overweight</div>
                    </div>""")

                    gr.HTML('<div class="section-header">🥗 Dietary Preferences</div>')
                    diet_preference = gr.Radio(
                        choices=["Vegetarian", "Non-vegetarian", "Semi-vegetarian"],
                        value="Vegetarian",
                        label="Food Preference",
                        info="Meal plans will be customized to your preference"
                    )

                    gr.HTML('<div class="section-header">🏃 Physical Activity & Lifestyle</div>')

                    # Walking/Exercise
                    does_walking = gr.Radio(
                        choices=["Yes", "No", "Don't Know"],
                        value="Don't Know",
                        label="Do you walk regularly or exercise?",
                        info="Help us understand your current activity level"
                    )

                    daily_steps = gr.Radio(
                        choices=["< 2000 steps (Sedentary)", "2000-5000 steps (Low Active)",
                                "5000-10000 steps (Active)", "10000+ steps (Very Active)", "Not Applicable"],
                        value="Not Applicable",
                        label="Daily Steps (if known)",
                        info="Average steps per day"
                    )

                    # Smoking & Alcohol
                    smoking_status = gr.Radio(
                        choices=["Never", "Former Smoker", "Current Smoker (< 10/day)", "Current Smoker (10+/day)"],
                        value="Never",
                        label="Smoking Status",
                        info="Affects metabolism and treatment approach"
                    )

                    alcohol_consumption = gr.Radio(
                        choices=["Never", "Occasional (1-2 times/month)", "Moderate (1-2 times/week)", "Frequent (3+ times/week)"],
                        value="Never",
                        label="Alcohol Consumption",
                        info="Important for dietary planning"
                    )

                    gr.HTML('<div class="section-header">📍 Location & Demographics</div>')
                    state_input = gr.Dropdown(choices=state_options, value="Maharashtra", label="State")
                    residence_input = gr.Radio(choices=["Urban", "Rural"], value="Urban", label="Residence Type")
                    wealth_input = gr.Dropdown(
                        choices=["Poorest", "Poorer", "Middle", "Richer", "Richest"],
                        value="Middle",
                        label="Socioeconomic Status"
                    )

                    with gr.Row():
                        generate_btn = gr.Button("🚀 Generate Treatment Plan", variant="primary", size="lg")
                    with gr.Row():
                        random_btn = gr.Button("🎲 Load Sample Patient", variant="secondary")

                    gr.HTML('<div class="warning-box">⏱️ <strong>Time:</strong> 1-3 minutes | 💰 <strong>Cost:</strong> ~$0.30-0.50 (GPT-4o)</div>')

                # RIGHT: Outputs
                with gr.Column(scale=2):
                    with gr.Tabs():
                        with gr.Tab("📋 Treatment Plan"):
                            treatment_output = gr.Markdown(value="*Your comprehensive treatment plan will appear here...*")

                        with gr.Tab("🍛 Regional Food Guide"):
                            food_output = gr.Markdown(value="*State-specific dietary recommendations will appear here...*")

                        with gr.Tab("🔍 Agent Logs"):
                            logs_output = gr.Textbox(label="AI Activity", lines=20, interactive=False)

            gr.Markdown("""
            ---
            **Technology:** CrewAI · GPT-4o · ChromaDB · Gradio 6.0.0 | **Data:** NFHS-5 (9,730 records) · WHO Guidelines · Indian Medical Research
            """)

            # Event handlers
            def update_bmi_display(weight, height_cm):
                """Update BMI when weight or height changes with color coding"""
                try:
                    if not weight or not height_cm:
                        return """<div style="padding: 15px; text-align: center; border-radius: 8px; background: #f1f5f9;">
                        <div style="font-size: 28px; font-weight: bold; color: #94a3b8;">0.00</div>
                        <div style="font-size: 14px; color: #64748b;">Invalid</div></div>"""

                    bmi, category = self.calculate_bmi(weight, height_cm)

                    # Color coding: Green (Normal), Yellow (Overweight), Red (Obese), Gray (Underweight)
                    if category == "Normal":
                        bg_color = "#dcfce7"
                        text_color = "#166534"
                        icon = "✅"
                    elif category == "Overweight":
                        bg_color = "#fef9c3"
                        text_color = "#854d0e"
                        icon = "⚠️"
                    elif category == "Obese":
                        bg_color = "#fee2e2"
                        text_color = "#991b1b"
                        icon = "🔴"
                    else:  # Underweight
                        bg_color = "#e0e7ff"
                        text_color = "#3730a3"
                        icon = "ℹ️"

                    return f"""<div style="padding: 15px; text-align: center; border-radius: 8px; background: {bg_color};">
                    <div style="font-size: 32px; font-weight: bold; color: {text_color};">{bmi}</div>
                    <div style="font-size: 16px; color: {text_color}; margin-top: 5px;">{icon} {category}</div>
                    </div>"""
                except:
                    return """<div style="padding: 15px; text-align: center; border-radius: 8px; background: #f1f5f9;">
                    <div style="font-size: 28px; font-weight: bold; color: #94a3b8;">0.00</div>
                    <div style="font-size: 14px; color: #64748b;">Invalid</div></div>"""

            def update_from_cm(height_cm):
                """Update feet/inches when cm changes"""
                try:
                    if not height_cm:
                        return 5, 3.0
                    feet, inches = self.cm_to_feet_inches(height_cm)
                    return feet, inches
                except:
                    return 5, 3.0

            def update_from_feet(feet, inches):
                """Update cm when feet/inches changes"""
                try:
                    cm = self.feet_inches_to_cm(feet, inches)
                    return cm
                except:
                    return 160

            # Wire up conversions
            feet_input.change(
                fn=update_from_feet,
                inputs=[feet_input, inches_input],
                outputs=[height_cm_input]
            )

            inches_input.change(
                fn=update_from_feet,
                inputs=[feet_input, inches_input],
                outputs=[height_cm_input]
            )

            # Update BMI when values change
            weight_input.change(
                fn=update_bmi_display,
                inputs=[weight_input, height_cm_input],
                outputs=[bmi_display]
            )

            feet_input.change(
                fn=lambda f, i, w: update_bmi_display(w, update_from_feet(f, i)),
                inputs=[feet_input, inches_input, weight_input],
                outputs=[bmi_display]
            )

            inches_input.change(
                fn=lambda f, i, w: update_bmi_display(w, update_from_feet(f, i)),
                inputs=[feet_input, inches_input, weight_input],
                outputs=[bmi_display]
            )

            # Generate treatment with auto-scroll to output area
            generate_btn.click(
                fn=self.generate_treatment_plan,
                inputs=[name_input, age_input, gender_input, height_cm_input, weight_input, diet_preference,
                       does_walking, daily_steps, smoking_status, alcohol_consumption,
                       state_input, residence_input, wealth_input],
                outputs=[treatment_output, food_output, logs_output],
                js="""
                (...args) => {
                    // Scroll to the output area to show progress
                    setTimeout(() => {
                        // Find the treatment output area and scroll it into view
                        const tabs = document.querySelector('.tabs');
                        if (tabs) {
                            tabs.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }
                    }, 100);
                    // Return args unchanged for form submission
                    return args;
                }
                """
            )

            # Load random patient
            def load_random():
                if self.data_loader is None:
                    self.data_loader = PatientDataLoader()
                patient = self.data_loader.get_random_patient()
                bmi, category = self.calculate_bmi(patient['weight_kg'], patient['height_cm'])
                feet, inches = self.cm_to_feet_inches(patient['height_cm'])

                # Generate BMI HTML with color coding
                bmi_html = update_bmi_display(patient['weight_kg'], patient['height_cm'])

                return (
                    "", patient['age'], patient['height_cm'], patient['weight_kg'],
                    "Vegetarian", patient['state'], patient['residence_type'],
                    patient['wealth_index'], bmi_html, feet, inches
                )

            random_btn.click(
                fn=load_random,
                outputs=[name_input, age_input, height_cm_input, weight_input, diet_preference,
                        state_input, residence_input, wealth_input, bmi_display,
                        feet_input, inches_input]
            )

        return interface


# Launch
if __name__ == "__main__":
    print("="*60)
    print("MODERN AI OBESITY TREATMENT SYSTEM")
    print("="*60)

    if not os.getenv("OPENAI_API_KEY"):
        print("\n[ERROR] OPENAI_API_KEY not found!")
        sys.exit(1)

    try:
        print("\nCreating modern interface...")
        app = ModernGradioInterface()
        interface = app.create_interface()
        print("\n[OK] Interface created!")
        print("[*] Launching...")

        interface.queue()
        interface.launch(server_name="0.0.0.0", server_port=7860, share=False)
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
