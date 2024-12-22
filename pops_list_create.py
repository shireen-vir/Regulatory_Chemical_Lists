import pandas as pd

# Input and Output file names
input_excel = "list-of-substances-subject-to-pops-regulation-export.xlsx"
output_excel = "POPs_Regulation_List.xlsx"

# EU-POP Dictionary
eu_pop_dict = {
    "EU-POP_C-1": "Pentachlorophenol esters",
    "EU-POP_C-2": "Perfluorooctane sulfonates (PFOS) C8F17SO2X (X = OH, Metal salt (O-M+), halide, amide, and other derivatives including polymers)",
    "EU-POP_C-3": "Polychlorinated dibenzo-p-dioxins and dibenzofurans (PCDD/PCDF)",
    "EU-POP_C-4": "Endosulfan and its isomers",
    "EU-POP_C-5": "Heptabromodiphenyl ether (Group)",
    "EU-POP_C-6": "Hexabromocyclododecane (HBCDD)",
    "EU-POP_C-7": "Hexabromodiphenyl ether (group)",
    "EU-POP_C-8": "Hexachlorocyclohexanes, including lindane",
    "EU-POP_C-9": "Pentabromodiphenyl ether (group)",
    "EU-POP_C-10": "Pentachlorophenol and its salts and esters",
    "EU-POP_C-11": "Pentachlorophenol salts",
    "EU-POP_C-12": "Perfluorohexane-1-sulphonic acid, its salts and related substances",
    "EU-POP_C-13": "perfluorooctanoic acid (PFOA), its salts and PFOA-related substances",
    "EU-POP_C-14": "Polychlorinated Biphenyls (PCB)",
    "EU-POP_C-15": "Polychlorinated naphthalenes",
    "EU-POP_C-16": "Polycyclic aromatic hydrocarbons (PAHs)",
    "EU-POP_C-17": "Tetrabromodiphenyl ether (group)"
}

# Annex Dictionary
annex_dict = {
    "Annex I, part A": {
        "description": "subject to prohibition (with specific exemptions) on manufacturing, placing on the market and use",
        "abbreviation": "POPs-Annex1_PartA"
    },
    "Annex III, part A": {
        "description": "subject to release reduction provisions",
        "abbreviation": "POPs-Annex3_PartA"
    },
    "Annex IV": {
        "description": "subject to waste management provisions",
        "abbreviation": "POPs-Annex4"
    },
    "Annex III, part B": {
        "description": "subject to release reduction provisions",
        "abbreviation": "POPs-Annex3_PartB"
    }
}

# Read the input Excel file
df_input = pd.read_excel(input_excel)

# Initialize the output dataframe with required columns
columns_output = [
    "name", "ec_number", "cas_number", "max-concentration-percent", "identifiers",
    "Categories", "Regulations", "inchikey", "iupac_name", "smiles",
    "molecular_formula", "qsar_ready_smiles", "ms_ready_smiles"
]
df_output = pd.DataFrame(columns=columns_output)

# Convert all input entries to strings
df_input = df_input.astype(str)

# Processing each row in the input file
for index, row in df_input.iterrows():
    substance_name = row['Substance name']
    ec_number = row['EC / List no']
    cas_number = row['CAS no']
    pops_annex = row['POPs Regulation Annex']

    # Check if the substance name matches any group in the dictionary
    cat_abbr = None
    cat_val = None
    for key, value in eu_pop_dict.items():
        if substance_name == value:
            cat_abbr = key
            cat_val = value
            break

    if cat_abbr:
        # Skip group entries and print debug message
        print(f"Group Found: {cat_abbr} -> {cat_val}. Skipping this entry.")
        category_string = f"{cat_abbr} : {cat_val}"
        continue

    # Parse the regulations string and extract the relevant parts
    regulations = []
    if pops_annex:
        annex_parts = pops_annex.split('#')
        for part in annex_parts:
            part = part.strip()
            if part in annex_dict:
                reg_abbr = annex_dict[part]['abbreviation']
                reg_desc = annex_dict[part]['description']
                regulations.append(f"EUR:EUROPE; {reg_abbr}: {reg_desc}")
            else:
                print(f"Warning: Regulation part '{part}' not found in annex dictionary.")
    regulations_string = "| ".join(regulations)

    # Add the processed data to the output dataframe
    df_output = pd.concat([
        df_output,
        pd.DataFrame({
            "name": [substance_name],
            "ec_number": [ec_number],
            "cas_number": [cas_number],
            "max-concentration-percent": [None],
            "identifiers": [None],
            "Categories": [category_string],
            "Regulations": [regulations_string],
            "inchikey": [None],
            "iupac_name": [None],
            "smiles": [None],
            "molecular_formula": [None],
            "qsar_ready_smiles": [None],
            "ms_ready_smiles": [None]
        })
    ], ignore_index=True)

# Write the output dataframe to an Excel file
df_output.to_excel(output_excel, index=False)
print(f"Processing complete. Output saved to {output_excel}.")
