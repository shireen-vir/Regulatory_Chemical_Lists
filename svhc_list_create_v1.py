import pandas as pd

# Define category mappings
CATEGORY_MAPPINGS = {
    "Carcinogenic (Article 57a)": {"full_description": "Carcinogenic (Article 57a)", "code": "CRCG"},
    "Mutagenic (Article 57b)": {"full_description": "Mutagenic (Article 57b)", "code": "MUTG"},
    "Toxic for reproduction (Article 57c)": {"full_description": "Toxic for Reproduction (Article 57c)", "code": "TXRPD"},
    "PBT (Article 57d)": {"full_description": "Persistent, Bioaccumulative and Toxic (Article 57d)", "code": "PBT"},
    "vPvB (Article 57e)": {"full_description": "very Persistent and very Bioaccumulative (Article 57e)", "code": "vPvB"},
    "Endocrine disrupting properties (Article 57(f) - human health)": {"full_description": "Endocrine disrupting properties (Article 57(f) - human health)", "code": "ECHUM"},
    "Endocrine disrupting properties (Article 57(f) - environment)": {"full_description": "Endocrine disrupting properties (Article 57(f) - environment)", "code": "ECENV"},
    "Equivalent level of concern having probable serious effects to human health (Article 57(f) - human health)": {"full_description": "Equivalent level of concern having probable serious effects to human health (Article 57(f) - human health)", "code": "PIHUM"},
    "Equivalent level of concern having probable serious effects to the environment (Article 57(f) - environment)": {"full_description": "Equivalent level of concern having probable serious effects to the environment (Article 57(f) - environment)", "code": "PIENV"},
    "Specific target organ toxicity after repeated exposure (Article 57(f) - human health)": {"full_description": "Specific target organ toxicity after repeated exposure (Article 57(f) - human health)", "code": "TOGHUM"},
    "Respiratory sensitising properties (Article 57(f) - human health)": {"full_description": "Respiratory sensitising properties (Article 57(f) - human health)", "code": "RSPHUM"}
}

# Input and output file paths
input_file = "candidate-list-of-svhc-for-authorisation-export_shireen.xlsx"
output_file = "echa_svhc.xlsx"

# Read the input file
df_file1 = pd.read_excel(input_file)

# Initialize the output dataframe with required columns
columns = [
    "name", "ec_number", "cas_number", "max-concentration-percent", "identifiers",
    "Categories", "Regulations", "inchikey", "iupac_name", "smiles",
    "molecular_formula", "qsar_ready_smiles", "ms_ready_smiles"
]
df_file2 = pd.DataFrame(columns=columns)

# Copy relevant columns
df_file2["name"] = df_file1["Substance name"].astype(str)
df_file2["ec_number"] = df_file1["EC No."].astype(str)
df_file2["cas_number"] = df_file1["CAS No."].astype(str)

# Populate the "Categories" column
def map_categories(reason):
    if pd.isna(reason):
        return ""
    reasons = str(reason).split("#")
    categories = []
    for reason in reasons:
        reason = reason.strip()
        if reason in CATEGORY_MAPPINGS:
            mapping = CATEGORY_MAPPINGS[reason]
            categories.append(f"{mapping['code']}:{mapping['full_description']}")
    return "|".join(categories)

df_file2["Categories"] = df_file1["Reason for inclusion"].apply(map_categories)
df_file2["Regulations"] = "EUR:EUROPE;REACH:Registration, Evaluation, Authorisation and Restriction of Chemicals"

# Write the output file
df_file2.to_excel(output_file, index=False)
print(f"Processed data has been saved to {output_file}")
