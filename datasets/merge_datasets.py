import pandas as pd
import numpy as np
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)

def load_pima_data():
    """Load and preprocess the PIMA dataset."""
    pima = pd.read_csv("pima dataset/pima_diabetes.csv")
    
    # Standardize column names to match NHANES
    pima = pima.rename(columns={
        'BloodPressure': 'BPXSY1',  # Using systolic BP as the main BP measurement
        'BMI': 'BMXBMI',
        'Age': 'RIDAGEYR',
        'Glucose': 'LBXGLU',
        'Pregnancies': 'RHD148',  # Number of pregnancies
        'SkinThickness': 'BMXWT',  # Using weight as a proxy for skin thickness
        'Insulin': 'LBXIN',
        'DiabetesPedigreeFunction': 'DIABETES_PEDIGREE',
        'Outcome': 'DIQ010'  # Diabetes diagnosis (1 = yes, 0 = no)
    })
    
    # Add missing columns with default values
    pima['RIAGENDR'] = 2  # 2 = Female (PIMA dataset is all females)
    pima['BPXDI1'] = pima['BPXSY1'] - 40  # Estimate diastolic BP
    
    # Add source column
    pima['DATA_SOURCE'] = 'PIMA'
    
    return pima

def load_nhanes_data():
    """Load and preprocess NHANES data with available columns."""
    print("Loading NHANES demographic data...")
    # Try to load basic demographic data
    try:
        demo_cols = ['SEQN', 'RIDAGEYR', 'RIAGENDR']
        demo = pd.read_csv("NHANES dataset/demographic.csv", usecols=demo_cols)
        print("  - Loaded demographic data with columns:", demo.columns.tolist())
    except Exception as e:
        print(f"  - Error loading demographic data: {e}")
        demo = pd.DataFrame(columns=['SEQN', 'RIDAGEYR', 'RIAGENDR'])
    
    print("Loading NHANES examination data...")
    # Try to load examination data with fallbacks
    try:
        exam_cols = ['SEQN', 'BMXWT', 'BMXHT', 'BMXBMI', 'BMXWAIST', 'BMXARMC', 'BMXARML']
        exam = pd.read_csv("NHANES dataset/examination.csv", usecols=exam_cols)
        print("  - Loaded examination data with columns:", exam.columns.tolist())
    except Exception as e:
        print(f"  - Error loading examination data: {e}")
        exam = pd.DataFrame(columns=['SEQN'])
    
    # Try to load blood pressure data if available
    has_bp = False
    bp = pd.DataFrame(columns=['SEQN'])
    try:
        bp_cols = ['SEQN'] + [f'BPXSY{i}' for i in range(1, 5)] + [f'BPXDI{i}' for i in range(1, 5)]
        bp = pd.read_csv("NHANES dataset/examination.csv", usecols=bp_cols)
        has_bp = True
        print("  - Loaded blood pressure data")
    except Exception as e:
        print(f"  - Warning: Could not load blood pressure data: {e}")
    
    print("Loading NHANES lab data...")
    # Initialize labs DataFrame with just SEQN
    labs = pd.DataFrame(columns=['SEQN'])
    
    try:
        # First, read just the header to see what columns are available
        with open("NHANES dataset/labs.csv", 'r') as f:
            header = f.readline().strip().replace('"', '').split(',')
        
        print(f"  - Found {len(header)} columns in labs.csv")
        
        # Look for potential columns of interest
        potential_glucose_cols = [col for col in header if 'GLU' in col or 'GLT' in col or 'GLY' in col]
        potential_insulin_cols = [col for col in header if 'IN' in col or 'INS' in col]
        potential_a1c_cols = [col for col in header if 'A1C' in col or 'GH' in col or 'GLYCO' in col]
        
        print(f"  - Potential glucose columns: {potential_glucose_cols}")
        print(f"  - Potential insulin columns: {potential_insulin_cols}")
        print(f"  - Potential A1C columns: {potential_a1c_cols}")
        
        # Always include SEQN, plus any available measurement columns
        lab_cols = ['SEQN']
        col_mapping = {}
            
        if potential_glucose_cols:
            lab_cols.append(potential_glucose_cols[0])
            col_mapping[potential_glucose_cols[0]] = 'GLUCOSE'
            
        if potential_insulin_cols:
            lab_cols.append(potential_insulin_cols[0])
            col_mapping[potential_insulin_cols[0]] = 'INSULIN'
            
        if potential_a1c_cols:
            lab_cols.append(potential_a1c_cols[0])
            col_mapping[potential_a1c_cols[0]] = 'A1C'
        
        # Only try to load if we have columns to load
        if len(lab_cols) > 1:
            print(f"  - Loading lab data with columns: {lab_cols}")
            labs = pd.read_csv("NHANES dataset/labs.csv", usecols=lab_cols)
            
            # Rename columns to standard names
            labs = labs.rename(columns=col_mapping)
            print("  - Successfully loaded lab data")
        else:
            print("  - No relevant lab data columns found")
            
    except Exception as e:
        print(f"  - Error loading lab data: {e}")
    
    print("Loading NHANES questionnaire data...")
    # Look for diabetes-related questions
    try:
        quest = pd.read_csv("NHANES dataset/questionnaire.csv")
        # Look for columns related to diabetes
        diabetes_cols = [col for col in quest.columns if 'DIQ' in col or 'DIAB' in col]
        if diabetes_cols:
            quest = quest[['SEQN'] + diabetes_cols]
            # Rename the first diabetes column to DIABETES if not already named
            if 'DIQ010' in quest.columns:
                quest = quest.rename(columns={'DIQ010': 'DIABETES'})
            elif 'DIABQ' in quest.columns:
                quest = quest.rename(columns={'DIABQ': 'DIABETES'})
        else:
            quest = pd.DataFrame(columns=['SEQN'])
    except Exception as e:
        print(f"Warning: Could not load questionnaire data: {e}")
        quest = pd.DataFrame(columns=['SEQN'])
    
    print("Merging NHANES datasets...")
    # Start with demographic data
    nhanes = demo.copy()
    
    # Merge other datasets if they have data
    nhanes = nhanes.merge(exam, on='SEQN', how='left')
    
    if has_bp:
        nhanes = nhanes.merge(bp, on='SEQN', how='left')
        
        # Calculate average blood pressure if we have the columns
        if all(col in nhanes.columns for col in ['BPXSY1', 'BPXSY2', 'BPXSY3', 'BPXSY4']):
            nhanes['SYS_BP'] = nhanes[['BPXSY1', 'BPXSY2', 'BPXSY3', 'BPXSY4']].mean(axis=1, skipna=True)
        if all(col in nhanes.columns for col in ['BPXDI1', 'BPXDI2', 'BPXDI3', 'BPXDI4']):
            nhanes['DIA_BP'] = nhanes[['BPXDI1', 'BPXDI2', 'BPXDI3', 'BPXDI4']].mean(axis=1, skipna=True)
        
        # Drop individual BP columns to save space
        nhanes = nhanes.drop(columns=[col for col in nhanes.columns if 'BPX' in col], errors='ignore')
    
    # Merge lab data
    if not labs.empty:
        nhanes = nhanes.merge(labs, on='SEQN', how='left')
    
    # Merge questionnaire data
    if not quest.empty and 'DIABETES' in quest.columns:
        nhanes = nhanes.merge(quest[['SEQN', 'DIABETES']], on='SEQN', how='left')
        
        # Standardize diabetes diagnosis if we have the column
        if 'DIABETES' in nhanes.columns:
            nhanes['DIABETES'] = nhanes['DIABETES'].replace({
                1: 1,  # Yes
                2: 0,  # No
                3: 1,  # Borderline -> consider as diabetes
                7: np.nan,  # Refused
                9: np.nan,  # Don't know
                '1': 1,
                '2': 0,
                '3': 1,
                '7': np.nan,
                '9': np.nan,
                'Yes': 1,
                'No': 0,
                'Borderline': 1,
                'Refused': np.nan,
                "Don't know": np.nan
            })
    
    # Add source column
    nhanes['DATA_SOURCE'] = 'NHANES'
    
    return nhanes

def preprocess_combined_data(pima, nhanes):
    """Preprocess and combine the datasets.
    
    Args:
        pima: DataFrame containing PIMA dataset
        nhanes: DataFrame containing NHANES dataset
        
    Returns:
        Combined and preprocessed DataFrame
    """
    pima_clean = pima.copy()
    nhanes_clean = nhanes.copy()
    
    # Standardize column names between PIMA and NHANES
    column_mapping = {
        # PIMA columns to standard names
        'BPXSY1': 'SYS_BP',
        'BPXDI1': 'DIA_BP',
        'LBXGLU': 'GLUCOSE',
        'LBXIN': 'INSULIN',
        'LBXGH': 'A1C',
        'RIDAGEYR': 'AGE',
        'RIAGENDR': 'GENDER',
        'BMXBMI': 'BMI',
        'DIABETES': 'OUTCOME'  # Standardize outcome column name
    }
    
    # Apply column mapping to both datasets
    pima_clean = pima_clean.rename(columns={k: v for k, v in column_mapping.items() 
                                          if k in pima_clean.columns})
    nhanes_clean = nhanes_clean.rename(columns={k: v for k, v in column_mapping.items()
                                              if k in nhanes_clean.columns})
    
    # Ensure all expected columns exist in both datasets
    expected_columns = ['AGE', 'GENDER', 'BMI', 'SYS_BP', 'DIA_BP', 
                       'GLUCOSE', 'INSULIN', 'A1C', 'OUTCOME']
    
    for col in expected_columns:
        if col not in pima_clean.columns:
            pima_clean[col] = np.nan
        if col not in nhanes_clean.columns:
            nhanes_clean[col] = np.nan
    
    # Add source column if not exists
    if 'DATA_SOURCE' not in pima_clean.columns:
        pima_clean['DATA_SOURCE'] = 'PIMA'
    if 'DATA_SOURCE' not in nhanes_clean.columns:
        nhanes_clean['DATA_SOURCE'] = 'NHANES'
    
    # Combine datasets
    combined = pd.concat([pima_clean, nhanes_clean], axis=0, ignore_index=True)
    
    # Clean and convert data types
    numeric_cols = ['AGE', 'BMI', 'SYS_BP', 'DIA_BP', 'GLUCOSE', 'INSULIN', 'A1C']
    for col in numeric_cols:
        if col in combined.columns:
            combined[col] = pd.to_numeric(combined[col], errors='coerce')
    
    # Handle missing values - keep rows with essential measurements
    # We'll keep rows with at least glucose, BMI, and outcome
    required_cols = ['GLUCOSE', 'BMI', 'OUTCOME']
    combined = combined.dropna(subset=[col for col in required_cols if col in combined.columns])
    
    # Ensure OUTCOME is binary (0 or 1)
    if 'OUTCOME' in combined.columns:
        combined['OUTCOME'] = combined['OUTCOME'].replace({
            2: 0,  # No
            3: 1,  # Borderline -> consider as diabetes
            7: np.nan,  # Refused
            9: np.nan,  # Don't know
            'No': 0,
            'Yes': 1,
            'Borderline': 1,
            'Refused': np.nan,
            "Don't know": np.nan
        })
        combined = combined.dropna(subset=['OUTCOME'])
        combined['OUTCOME'] = combined['OUTCOME'].astype(int)
    
    # Add derived features if we have the necessary columns
    if 'AGE' in combined.columns and 'BMI' in combined.columns:
        # Age groups
        bins = [0, 30, 45, 60, 100]
        labels = ['<30', '30-44', '45-59', '60+']
        combined['AGE_GROUP'] = pd.cut(combined['AGE'], bins=bins, labels=labels, right=False)
        
        # BMI categories
        bmi_bins = [0, 18.5, 25, 30, 100]
        bmi_labels = ['Underweight', 'Normal', 'Overweight', 'Obese']
        combined['BMI_CATEGORY'] = pd.cut(combined['BMI'], bins=bmi_bins, labels=bmi_labels, right=False)
    
    return combined

def generate_dataset_description(df):
    """Generate a detailed description of the dataset.
    
    Args:
        df: Combined DataFrame to describe
        
    Returns:
        str: Formatted description of the dataset
    """
    description = "# Combined Diabetes Dataset Description\n\n"
    
    # Basic information
    description += "## Dataset Overview\n"
    description += f"- Total samples: {len(df):,}\n"
    
    # Data sources
    if 'DATA_SOURCE' in df.columns:
        source_counts = df['DATA_SOURCE'].value_counts()
        description += "- Data sources:\n"
        for source, count in source_counts.items():
            description += f"  - {source}: {count:,} samples ({count/len(df):.1%})\n"
    
    # Outcome distribution
    if 'OUTCOME' in df.columns:
        outcome_counts = df['OUTCOME'].value_counts()
        description += f"- Diabetes cases: {outcome_counts.get(1, 0):,} ({outcome_counts.get(1, 0)/len(df):.1%})\n"
        if 'DATA_SOURCE' in df.columns:
            description += "- Diabetes prevalence by source:\n"
            for source in df['DATA_SOURCE'].unique():
                source_df = df[df['DATA_SOURCE'] == source]
                count = source_df['OUTCOME'].sum()
                total = len(source_df)
                description += f"  - {source}: {count:,}/{total:,} ({count/max(1, total):.1%})\n"
    
    # Column information
    description += "\n## Variables\n"
    
    # Define variable categories
    demographics = ['AGE', 'GENDER', 'RACE', 'ETHNICITY']
    measurements = ['HEIGHT', 'WEIGHT', 'BMI', 'WAIST_CIRC', 'HIP_CIRC', 'WAIST_HIP_RATIO']
    vitals = ['SYS_BP', 'DIA_BP', 'HEART_RATE', 'RESP_RATE', 'TEMPERATURE']
    labs = ['GLUCOSE', 'INSULIN', 'A1C', 'CHOLESTEROL', 'HDL', 'LDL', 'TRIGLYCERIDES']
    
    # Categorize columns
    demo_cols = [col for col in df.columns if any(d in col.upper() for d in demographics)]
    measure_cols = [col for col in df.columns if any(m in col.upper() for m in measurements)]
    vital_cols = [col for col in df.columns if any(v in col.upper() for v in vitals)]
    lab_cols = [col for col in df.columns if any(l in col.upper() for l in labs)]
    other_cols = [col for col in df.columns if col not in demo_cols + measure_cols + vital_cols + lab_cols 
                  and col not in ['OUTCOME', 'DATA_SOURCE', 'SEQN']]
    
    # Add column descriptions
    def add_column_section(title, columns):
        if not columns:
            return ""
        section = f"### {title}\n"
        for col in columns:
            dtype = str(df[col].dtype)
            missing = df[col].isna().sum()
            missing_pct = missing / len(df) * 100
            
            section += f"- **{col}** ({dtype})\n"
            if df[col].dtype in ['int64', 'float64']:
                section += f"  - Range: {df[col].min():.2f} to {df[col].max():.2f}\n"
                if len(df[col].unique()) < 20:  # Likely categorical
                    section += f"  - Values: {sorted(df[col].unique().tolist())}\n"
            section += f"  - Missing: {missing:,} ({missing_pct:.1f}%)\n"
            
            if col.upper() == 'GENDER':
                gender_map = {1: 'Male', 2: 'Female'}
                section += f"  - Values: {gender_map}\n"
        return section + "\n"
    
    description += add_column_section("Demographics", demo_cols)
    description += add_column_section("Anthropometric Measurements", measure_cols)
    description += add_column_section("Vital Signs", vital_cols)
    description += add_column_section("Laboratory Tests", lab_cols)
    description += add_column_section("Other Variables", other_cols)
    
    # Add data quality information
    description += "## Data Quality\n"
    missing_values = df.isna().sum().sum()
    total_cells = df.size
    missing_pct = missing_values / total_cells * 100
    
    description += f"- Total missing values: {missing_values:,} ({missing_pct:.1f}% of all cells)\n"
    description += "- Rows with any missing values: {:,} ({:.1f}%)\n".format(
        df.isna().any(axis=1).sum(),
        df.isna().any(axis=1).mean() * 100
    )
    
    # Add summary statistics for numeric columns
    if any(df[col].dtype in ['int64', 'float64'] for col in df.columns):
        description += "\n## Summary Statistics\n"
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        description += df[numeric_cols].describe().round(2).to_markdown()
    
    return description

def main():
    """Main function to run the data merging and preprocessing."""
    print("Loading PIMA dataset...")
    pima = load_pima_data()
    print("\nPIMA dataset preview:")
    print(pima.head())
    print("\nPIMA dataset columns:", pima.columns.tolist())
    
    print("\nLoading NHANES dataset...")
    nhanes = load_nhanes_data()
    print("\nNHANES dataset preview:")
    print(nhanes.head())
    print("\nNHANES dataset columns:", nhanes.columns.tolist())
    
    print("\nCombining and preprocessing datasets...")
    combined = preprocess_combined_data(pima, nhanes)
    
    # Save the combined dataset
    output_file = "combined_diabetes_dataset.csv"
    combined.to_csv(output_file, index=False)
    print(f"\nCombined dataset saved to {output_file}")
    
    # Generate dataset description
    description = generate_dataset_description(combined)
    with open("dataset_description.txt", "w") as f:
        f.write(description)
    print("\nDataset description saved to dataset_description.txt")
    
    # Print dataset summary
    print("\nCombined dataset summary:")
    print(combined.info())
    print("\nFirst 5 rows of combined dataset:")
    print(combined.head())
    
    # Print value counts for categorical variables
    if 'OUTCOME' in combined.columns:
        print("\nOutcome distribution:")
        print(combined['OUTCOME'].value_counts(dropna=False))
        print(f"\nDiabetes prevalence: {combined['OUTCOME'].mean():.1%}")
    
    if 'DATA_SOURCE' in combined.columns:
        print(f"\nPIMA samples: {len(combined[combined['DATA_SOURCE'] == 'PIMA']):,}")
        print(f"NHANES samples: {len(combined[combined['DATA_SOURCE'] == 'NHANES']):,}")
    
    print("\nMissing values per column:")
    print(combined.isnull().sum())
    
    # Save dataset description
    with open('dataset_description.txt', 'w') as f:
        f.write("=== Combined Diabetes Dataset Description ===\n\n")
        f.write(f"Total samples: {len(combined):,}\n")
        if 'DATA_SOURCE' in combined.columns:
            f.write(f"PIMA samples: {len(combined[combined['DATA_SOURCE'] == 'PIMA']):,}\n")
            f.write(f"NHANES samples: {len(combined[combined['DATA_SOURCE'] == 'NHANES']):,}\n")
        if 'OUTCOME' in combined.columns:
            f.write(f"\nDiabetes cases: {combined['OUTCOME'].sum():,} ({combined['OUTCOME'].mean():.1%})\n\n")
        f.write("\n=== Column Descriptions ===\n")
        for col in combined.columns:
            f.write(f"\n{col}:")
            if combined[col].dtype in ['int64', 'float64']:
                f.write(f"\n  Type: {combined[col].dtype}")
                f.write(f"\n  Non-null: {combined[col].count():,} ({(combined[col].count()/len(combined)):.1%})")
                if len(combined[col].unique()) < 20:  # For categorical variables
                    f.write("\n  Value counts:")
                    for val, count in combined[col].value_counts().items():
                        f.write(f"\n    {val}: {count:,} ({(count/len(combined)):.1%})")
                else:  # For continuous variables
                    f.write(f"\n  Mean: {combined[col].mean():.2f}")
                    f.write(f"\n  Std: {combined[col].std():.2f}")
                    f.write(f"\n  Min: {combined[col].min():.2f}")
                    f.write(f"\n  25%: {combined[col].quantile(0.25):.2f}")
                    f.write(f"\n  50%: {combined[col].median():.2f}")
                    f.write(f"\n  75%: {combined[col].quantile(0.75):.2f}")
                    f.write(f"\n  Max: {combined[col].max():.2f}")
    
    print("\nDetailed dataset description saved to 'dataset_description.txt'")

if __name__ == "__main__":
    main()
