import pandas as pd
import os

# Define the mapping for categories
CATEGORY_MAPPING = {
    "cancer": "cancer_categ", # c
    "developmental": "dev_categ",
    "developmental male": "dev_male_categ",
    "developmental female": "dev_female_categ",
    "male": "male_categ",
    "female": "female_categ",
}

# Input and output file names
REFERENCE_EXCEL = "prp_65.xlsx"
OUTPUT_EXCEL = "cal_prop_65.xlsx"

# Define the header for the new Excel
NEW_EXCEL_COLUMNS = [
    "name",
    "ec_number",
    "cas_number",
    "max-concentration-percent",
    "identifiers",
    "Categories",
    "Regulations",
    "inchikey",
    "iupac_name",
    "smiles",
    "molecular_formula",
    "qsar_ready_smiles",
    "ms_ready_smiles",
]

def process_categories(category_cell):
    """
    Process the Type of Toxicity column to map and construct the Categories field.
    """
    if pd.isna(category_cell):
        return ""

    categories = []
    not_found = []

    for entry in str(category_cell).split(','):
        entry_clean = entry.strip()  # Remove leading and trailing spaces
        if entry_clean in CATEGORY_MAPPING:
            categories.append(f"{CATEGORY_MAPPING[entry_clean]}:{entry_clean}")
        else:
            not_found.append(entry_clean)

    # Log the entries not found in the mapping
    if not_found:
        print(f"Unmapped categories: {', '.join(not_found)}")

    return " | ".join(categories)

def main():
    if not os.path.exists(REFERENCE_EXCEL):
        print(f"Error: File '{REFERENCE_EXCEL}' not found.")
        return

    # Read the reference Excel
    ref_df = pd.read_excel(REFERENCE_EXCEL)

    # Prepare the new DataFrame
    new_data = {col: [] for col in NEW_EXCEL_COLUMNS}

    for _, row in ref_df.iterrows():
        # Skip rows where Chemical is blank
        if pd.isna(row.get("Chemical")):
            continue

        # Map the columns from reference Excel to the new Excel format
        new_data["name"].append(str(row.get("Chemical", "")))
        new_data["cas_number"].append(str(row.get("CAS No.", "")))
        new_data["Categories"].append(process_categories(row.get("Type of Toxicity", "")))

        # Fill other columns with empty strings
        for col in new_data:
            if len(new_data[col]) < len(new_data["name"]):
                new_data[col].append("")

    # Create a DataFrame for the new Excel
    new_df = pd.DataFrame(new_data)

    # Write the new DataFrame to Excel
    new_df.to_excel(OUTPUT_EXCEL, index=False)
    print(f"New Excel file '{OUTPUT_EXCEL}' has been created.")

if __name__ == "__main__":
    main()
