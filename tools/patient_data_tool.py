"""
Patient Data Loader Tool
Loads patient data from the NFHS dataset (9,730 records)
Columns: BMI, Weight_kg, Height_cm, BMI_Category, Age, State, Urban_Rural, Wealth_Index
"""

import pandas as pd
import os
from typing import Dict, Optional, List
import random


# State mapping (based on NFHS-5 state codes)
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


class PatientDataLoader:
    """Loads and manages patient data from NFHS dataset"""

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the patient data loader

        Args:
            data_path: Path to the CSV file. If None, uses default location.
        """
        if data_path is None:
            # Default path relative to project root
            project_root = os.path.dirname(os.path.dirname(__file__))
            data_path = os.path.join(project_root, 'data', 'indian_obesity_data_clean.csv')

        self.data_path = data_path
        self.df = None
        self.load_data()

    def load_data(self):
        """Load the CSV data into memory"""
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"[OK] Loaded {len(self.df):,} patient records from NFHS dataset")
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Data file not found at {self.data_path}. "
                "Please ensure indian_obesity_data_clean.csv is in the data/ directory."
            )

    def get_random_patient(self) -> Dict:
        """
        Get a random patient from the dataset

        Returns:
            Dict containing patient information
        """
        if self.df is None:
            raise ValueError("Data not loaded")

        patient_row = self.df.sample(n=1).iloc[0]
        return self._format_patient_data(patient_row)

    def get_patient_by_index(self, index: int) -> Dict:
        """
        Get a specific patient by index

        Args:
            index: Row index in the dataset

        Returns:
            Dict containing patient information
        """
        if self.df is None:
            raise ValueError("Data not loaded")

        if index < 0 or index >= len(self.df):
            raise ValueError(f"Index {index} out of range (0-{len(self.df)-1})")

        patient_row = self.df.iloc[index]
        return self._format_patient_data(patient_row)

    def get_patients_by_criteria(self,
                                  state: Optional[str] = None,
                                  residence_type: Optional[str] = None,
                                  bmi_category: Optional[str] = None,
                                  wealth_index: Optional[str] = None,
                                  limit: int = 10) -> List[Dict]:
        """
        Get patients matching specific criteria

        Args:
            state: State name to filter by
            residence_type: 'Urban' or 'Rural'
            bmi_category: BMI category to filter by
            wealth_index: Wealth index category
            limit: Maximum number of patients to return

        Returns:
            List of patient dictionaries
        """
        if self.df is None:
            raise ValueError("Data not loaded")

        filtered_df = self.df.copy()

        if state:
            # Find state code
            state_code = None
            for code, name in STATE_MAPPING.items():
                if name.lower() == state.lower():
                    state_code = code
                    break
            if state_code:
                filtered_df = filtered_df[filtered_df['State'] == state_code]

        if residence_type:
            residence_code = 1 if residence_type.lower() == "urban" else 2
            filtered_df = filtered_df[filtered_df['Urban_Rural'] == residence_code]

        if bmi_category:
            filtered_df = filtered_df[filtered_df['BMI_Category'].str.lower() == bmi_category.lower()]

        if wealth_index:
            wealth_code = None
            for code, name in WEALTH_MAPPING.items():
                if name.lower() == wealth_index.lower():
                    wealth_code = code
                    break
            if wealth_code:
                filtered_df = filtered_df[filtered_df['Wealth_Index'] == wealth_code]

        # Sample up to limit records
        if len(filtered_df) > limit:
            filtered_df = filtered_df.sample(n=limit)

        return [self._format_patient_data(row) for _, row in filtered_df.iterrows()]

    def _format_patient_data(self, row: pd.Series) -> Dict:
        """
        Format a pandas row into a structured patient dictionary

        Args:
            row: Pandas series representing a patient

        Returns:
            Formatted patient dictionary
        """
        # Get state name
        state_code = int(row['State']) if pd.notna(row['State']) else 0
        state_name = STATE_MAPPING.get(state_code, "Unknown")

        # Get residence type
        residence_code = int(row['Urban_Rural']) if pd.notna(row['Urban_Rural']) else 0
        residence_type = RESIDENCE_MAPPING.get(residence_code, "Unknown")

        # Get wealth index
        wealth_code = int(row['Wealth_Index']) if pd.notna(row['Wealth_Index']) else 0
        wealth_index = WEALTH_MAPPING.get(wealth_code, "Unknown")

        patient_data = {
            "patient_id": f"NFHS_{row.name}",
            "age": int(row['Age']) if pd.notna(row['Age']) else None,
            "height_cm": float(row['Height_cm']) if pd.notna(row['Height_cm']) else None,
            "weight_kg": float(row['Weight_kg']) if pd.notna(row['Weight_kg']) else None,
            "bmi": float(row['BMI']) if pd.notna(row['BMI']) else None,
            "bmi_category": row['BMI_Category'] if pd.notna(row['BMI_Category']) else "Unknown",
            "state": state_name,
            "residence_type": residence_type,
            "wealth_index": wealth_index,
        }

        # Add derived information for treatment planning
        patient_data["location_context"] = f"{residence_type} area in {state_name}"
        patient_data["socioeconomic_status"] = wealth_index

        # Generate contextual data for Indian context
        patient_data["dietary_context"] = self._get_dietary_context(state_name, residence_type)
        patient_data["physical_activity_context"] = self._get_activity_context(residence_type, wealth_index)

        return patient_data

    def _get_dietary_context(self, state: str, residence: str) -> str:
        """Generate dietary context based on location"""
        if residence == "Rural":
            return "Traditional Indian diet with locally grown crops, rice/wheat based meals"
        else:
            return "Urban diet with mix of traditional and modern foods, increased processed food access"

    def _get_activity_context(self, residence: str, wealth: str) -> str:
        """Generate activity context based on socioeconomic factors"""
        if residence == "Rural":
            return "Moderate to high physical labor in agriculture or manual work"
        elif wealth in ["Richest", "Richer"]:
            return "Sedentary office work, limited physical activity, gym access available"
        else:
            return "Mix of manual and sedentary work, limited structured exercise"

    def get_dataset_stats(self) -> Dict:
        """
        Get statistics about the dataset

        Returns:
            Dictionary with dataset statistics
        """
        if self.df is None:
            raise ValueError("Data not loaded")

        stats = {
            "total_records": len(self.df),
            "bmi_categories": self.df['BMI_Category'].value_counts().to_dict(),
            "average_bmi": float(self.df['BMI'].mean()),
            "average_age": float(self.df['Age'].mean()),
            "average_weight": float(self.df['Weight_kg'].mean()),
            "average_height": float(self.df['Height_cm'].mean()),
        }

        # Add state distribution
        state_counts = self.df['State'].value_counts().to_dict()
        stats["states"] = {STATE_MAPPING.get(k, f"Unknown_{k}"): v for k, v in state_counts.items()}

        # Add residence type distribution
        residence_counts = self.df['Urban_Rural'].value_counts().to_dict()
        stats["residence_types"] = {RESIDENCE_MAPPING.get(k, f"Unknown_{k}"): v for k, v in residence_counts.items()}

        # Add wealth index distribution
        wealth_counts = self.df['Wealth_Index'].value_counts().to_dict()
        stats["wealth_distribution"] = {WEALTH_MAPPING.get(k, f"Unknown_{k}"): v for k, v in wealth_counts.items()}

        return stats


# Convenience functions for quick access
_loader_instance = None


def get_loader() -> PatientDataLoader:
    """Get or create the singleton data loader instance"""
    global _loader_instance
    if _loader_instance is None:
        _loader_instance = PatientDataLoader()
    return _loader_instance


def get_random_patient() -> Dict:
    """Quick function to get a random patient"""
    return get_loader().get_random_patient()


def get_patient(index: int) -> Dict:
    """Quick function to get a specific patient by index"""
    return get_loader().get_patient_by_index(index)


if __name__ == "__main__":
    # Test the data loader
    print("\n" + "="*60)
    print("TESTING PATIENT DATA LOADER")
    print("="*60 + "\n")

    loader = PatientDataLoader()

    # Show dataset stats
    print("Dataset Statistics:")
    stats = loader.get_dataset_stats()
    print(f"Total Records: {stats['total_records']:,}")
    print(f"Average BMI: {stats['average_bmi']:.2f}")
    print(f"Average Age: {stats['average_age']:.1f} years")
    print(f"Average Weight: {stats['average_weight']:.1f} kg")
    print(f"Average Height: {stats['average_height']:.1f} cm")

    print("\nBMI Categories:")
    for category, count in stats['bmi_categories'].items():
        print(f"  {category}: {count:,}")

    print("\nResidence Type Distribution:")
    for rtype, count in stats['residence_types'].items():
        print(f"  {rtype}: {count:,}")

    # Get a random patient
    print("\n" + "="*60)
    print("RANDOM PATIENT SAMPLE")
    print("="*60 + "\n")

    patient = loader.get_random_patient()
    for key, value in patient.items():
        print(f"{key}: {value}")

    # Get patients from specific state
    print("\n" + "="*60)
    print("PATIENTS FROM MAHARASHTRA (Urban, Overweight)")
    print("="*60 + "\n")

    patients = loader.get_patients_by_criteria(
        state="Maharashtra",
        residence_type="Urban",
        bmi_category="Overweight",
        limit=3
    )

    if patients:
        for i, p in enumerate(patients, 1):
            print(f"\nPatient {i}:")
            print(f"  ID: {p['patient_id']}")
            print(f"  Age: {p['age']} years")
            print(f"  BMI: {p['bmi']:.1f} ({p['bmi_category']})")
            print(f"  Weight: {p['weight_kg']:.1f} kg, Height: {p['height_cm']:.1f} cm")
            print(f"  Location: {p['location_context']}")
            print(f"  Wealth: {p['wealth_index']}")
    else:
        print("No patients found matching criteria")
