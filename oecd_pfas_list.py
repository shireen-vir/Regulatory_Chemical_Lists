import pandas as pd

# Load the input file
input_file = "global-database-of-per-and-polyfluoroalkyl-substances_26Jun2024_shireen.xlsx"
output_file = "oecd_pfas_v1.xlsx"

# Regulation mapping as specified
regulation_mapping = [
    {"regulation_name": "Australian AICS", "regulatory_region": "AUSTRALIA", "legend": "AICS"},
    {"regulation_name": "Australian IMAP Tier 2", "regulatory_region": "AUSTRALIA", "legend": "IMAP2"},
    {"regulation_name": "Canada PCTSR 2012", "regulatory_region": "CANADA", "legend": "PCTSR"},
    {"regulation_name": "Canadian DSL", "regulatory_region": "CANADA", "legend": "DSL"},
    {"regulation_name": "China IECSC", "regulatory_region": "CHINA", "legend": "IECSC"},
    {"regulation_name": "EU REACH Pre-registered", "regulatory_region": "EUROPE", "legend": "REACH-P"},
    {"regulation_name": "EU REACH Registered", "regulatory_region": "EUROPE", "legend": "REACH-R"},
    {"regulation_name": "Japan ENCS", "regulatory_region": "JAPAN", "legend": "ENCS"},
    {"regulation_name": "Japan Examples of PFOA Stockholm Convention", "regulatory_region": "JAPAN", "legend": "STCON"},
    {"regulation_name": "SPIN", "regulatory_region": "EUROPE", "legend": "SPIN"},
    {"regulation_name": "US EPA CDR 2012", "regulatory_region": "USA", "legend": "CDR12"},
    {"regulation_name": "US EPA CDR 2016", "regulatory_region": "USA", "legend": "CDR16"},
    {"regulation_name": "US EPA IUR 1986-2002", "regulatory_region": "USA", "legend": "IUR02"},
    {"regulation_name": "US EPA IUR 2006", "regulatory_region": "USA", "legend": "IUR06"},
    {"regulation_name": "US EPA TSCA 12b", "regulatory_region": "USA", "legend": "TSCA12b"},
    {"regulation_name": "US EPA TSCA Inventory", "regulatory_region": "USA", "legend": "TSCA"},
    {"regulation_name": "US FDA FCS", "regulatory_region": "USA", "legend": "FCS"},
]

# Load input data
df_input = pd.read_excel(input_file)

# Prepare the output dataframe
columns = [
    "name", "ec_number", "cas_number", "max-concentration-percent", "identifiers",
    "Categories", "Regulations", "inchikey", "iupac_name", "smiles",
    "molecular_formula", "qsar_ready_smiles", "ms_ready_smiles"
]
df_output = pd.DataFrame(columns=columns)

# Populate output data
df_output["cas_number"] = df_input["CAS Number"].astype(str)
df_output["name"] = df_input["Chemical Name"].astype(str)

# Process identifiers
def process_identifiers(row):
    synonyms = str(row.get("Synonyms", "")).replace(";", "|")
    prev_cas = str(row.get("Previously used CAS Number", "")).replace(",", "|")
    return f"{synonyms} | {prev_cas}"

df_output["identifiers"] = df_input.apply(process_identifiers, axis=1)

# Process categories
def process_categories(row):
    category = str(row.get("Structure Category", ""))
    category_name = str(row.get("Structure Category Name", "")).replace(":", "")
    return f"{category} : {category_name}"

df_output["Categories"] = df_input.apply(process_categories, axis=1)

# Copy columns directly
df_output["molecular_formula"] = df_input["Molecular Formula"]
df_output["smiles"] = df_input["SMILES"]

# Process regulations
def process_regulations(row):
    regulations = []
    for mapping in regulation_mapping:
        column = mapping["regulation_name"]
        if row.get(column, 0) == 1:
            regulations.append(
                f"{mapping['regulatory_region']}:{mapping['regulatory_region']};{mapping['legend']}:{mapping['regulation_name']}"
            )
    return " | ".join(regulations)

df_output["Regulations"] = df_input.apply(process_regulations, axis=1)

# Save the output file
df_output.to_excel(output_file, index=False)

print(f"Processed data has been saved to {output_file}.")
