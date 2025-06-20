import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
from fuzzywuzzy import process


# === Initialize Firestore ===
cred = credentials.Certificate("firebase_key.json")  # Replace with your actual path
firebase_admin.initialize_app(cred)
db = firestore.client()

# === URL of MouthShut Page ===
MOUTHSHUT_URL = "https://www.mouthshut.com/companies/top-10-health-insurance-companies-in-india-tpg-120"

response = requests.get(MOUTHSHUT_URL)
print(response.status_code)
print(response.text[:1000])  # print first 1000 chars of the page content


def fetch_mouthshut_data():
    response = requests.get(MOUTHSHUT_URL)
    soup = BeautifulSoup(response.content, "html.parser")

    company_data = {}

    # Each company's block contains h3 and rating info
    for block in soup.find_all("div", class_="col-12 col-lg-8 col-md-8 pl-4 pr-4"):
        title_tag = block.find("h3")
        if not title_tag:
            continue
        
        username = title_tag.get_text(strip=True).lower()

        rating_block = block.find_next("div", class_="rating-sec")
        if not rating_block:
            continue
        
        try:
            vote_percent = rating_block.find("span", string=lambda x: "%" in x).get_text(strip=True)
            rating = rating_block.find("span", class_="orange-text").get_text(strip=True)
            votes_text = rating_block.find_all("span")[-1].get_text(strip=True)
            votes = votes_text.replace(",", "").split()[0]

            company_data[username] = {
                "vote_percent": vote_percent,
                "rating": float(rating),
                "votes": int(votes)
            }
        except Exception as e:
            print(f"Skipping {username} due to error: {e}")
    
    return company_data

def update_firestore_with_scraped_data():
    scraped_data = fetch_mouthshut_data()
    users_ref = db.collection("USERS").stream()

    scraped_keys = list(scraped_data.keys())
    print(f"Scraped {len(scraped_keys)} companies:", scraped_keys)

    for user_doc in users_ref:
        user_data = user_doc.to_dict()
        username = user_data.get("username")

        if not username:
            continue

        result = process.extractOne(username.lower(), scraped_keys)

        if result is not None:
            match, score = result
            if score >= 60:
                data = scraped_data[match]
                db.collection("USERS").document(user_doc.id).update({
                    "mouthshut_rating": data["rating"],
                    "mouthshut_votes": data["votes"],
                    "mouthshut_vote_percent": data["vote_percent"],
                    "matched_company_name": match
                })
                print(f"✅ Matched: {username} → {match} (score: {score})")
            else:
                print(f"❌ No close match for: {username} (best score: {score})")
        else:
            print(f"❌ No match found at all for: {username}")


# === Run the script ===
if __name__ == "__main__":
    update_firestore_with_scraped_data()
