import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# === Initialize Firebase App ===
firebase_config = st.secrets["firebase"]
cred = credentials.Certificate(dict(firebase_config))
firebase_admin.initialize_app(cred)

# === Load Excel file with all sheets ===
excel_path = "Death Claims_upto  March 2022_website.xlsx"  # Replace with your Excel file path
sheets = pd.read_excel(excel_path, sheet_name=None, header=None)  # No header

for sheet_name, df in sheets.items():
    print(f"\n📄 Processing sheet: {sheet_name}")
    
    # Find header row (where column A is 'Life Insurer')
    header_row_index = None
    for i, row in df.iterrows():
        if str(row[0]).strip().lower() == 'life insurer':
            header_row_index = i
            break

    if header_row_index is None:
        print(f"⚠️ 'Life Insurer' header not found in {sheet_name}, skipping.")
        continue

    # Reload sheet using detected header
    df = pd.read_excel(excel_path, sheet_name=sheet_name, header=header_row_index)

    for idx, row in df.iterrows():
        try:
            insurer_name = str(row.iloc[0]).strip()  # Column A
            claim_ratio = row.iloc[18]  # Column S (0-based index 18)

            if pd.isna(insurer_name) or pd.isna(claim_ratio):
                continue

            # Firestore lookup
            users_ref = db.collection("USERS")
            matches = users_ref.where("username", "==", insurer_name).get()

            if matches:
                for doc in matches:
                    users_ref.document(doc.id).update({
                        "claim_settlement_ratio": claim_ratio
                    })
                    print(f"✅ Updated: {insurer_name} → {claim_ratio}")
            else:
                print(f"⚠️ No match found in Firestore for: {insurer_name}")

        except Exception as e:
            print(f"❌ Error at row {idx}: {e}")
