import pandas as pd

# Input and output file paths
file1 = "Starting Point for CN PFAS.xlsx"
file2 = "global-database-of-per-and-polyfluoroalkyl-substances_26Jun2024_shireen.xlsx"
file3 = "Canadian_PFAS_v2.xlsx"

# Columns for the output file
columns = [
    "name",
    "cas_number",
    "ec_number",
    "max-concentration-percent",
    "Categories",
    "Regulations",
    "identifiers",
    "inchikey",
    "iupac_name",
    "smiles",
    "molecular_formula",
    "qsar_ready_smiles",
    "ms_ready_smiles",
]

# Load the Excel files
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

# Create the output DataFrame
output_df = pd.DataFrame(columns=columns)

# Extract the relevant columns from the input files
substance_identifier_col = "Substance identifier"
substance_name_col = "Substance Name"
cas_number_col = "CAS Number"
previously_used_cas_col = "Previously used CAS Number"
structure_category_col = "Structure Category"
structure_category_name_col = "Structure Category Name"
synonyms_col = "Synonyms"
smiles_col = "SMILES"
molecular_formula_col = "Molecular Formula"

# Iterate over each row in file1
for _, row1 in df1.iterrows():
    substance_identifier = row1[substance_identifier_col]
    substance_name = row1.get(substance_name_col, "")

    # Search in file2
    match = df2[(df2[cas_number_col] == substance_identifier) |
                (df2[previously_used_cas_col] == substance_identifier)]

    if not match.empty:
        # Found a match
        match_row = match.iloc[0]

        # Extract categories
        structure_category = match_row.get(structure_category_col, "")
        structure_category_name = match_row.get(structure_category_name_col, "")
        categories = f"{structure_category}: {structure_category_name}" if structure_category or structure_category_name else ""

        # Extract identifiers
        synonyms = str(match_row.get(synonyms_col, "")).replace(";", "|")
        previously_used_cas = str(match_row.get(previously_used_cas_col, "")).replace(",", "|")
        identifiers = synonyms
        if previously_used_cas:
            identifiers += f"| {previously_used_cas}"

        # Extract smiles
        smiles = str(match_row.get(smiles_col, ""))

        # Extract molecular formula 
        molecular_formula = str(match_row.get(molecular_formula_col, ""))

        # Append to output DataFrame
        output_df = pd.concat([
            output_df,
            pd.DataFrame({
                "name": [substance_name],
                "cas_number": [substance_identifier],
                "Categories": [categories],
                "identifiers": [identifiers],
                "smiles": [smiles],
                "molecular_formula": [molecular_formula]
            })
        ], ignore_index=True)

        # Print match case
        if substance_identifier == match_row[cas_number_col]:
            print(f"{substance_identifier} from file1 got matched in file2 (CAS Number)")
        elif substance_identifier == match_row[previously_used_cas_col]:
            print(f"{substance_identifier} from file1 got matched in file2 (Previously used CAS Number)")

    else:
        # No match found
        output_df = pd.concat([
            output_df,
            pd.DataFrame({
                "name": [substance_name],
                "cas_number": [substance_identifier],
            })
        ], ignore_index=True)

        # Print no match case
        print(f"{substance_identifier} from file1 has no match in file2")

# Save the output DataFrame to Excel
output_df.to_excel(file3, index=False)
print(f"Data has been saved to {file3}")
