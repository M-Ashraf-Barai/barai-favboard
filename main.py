


import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os
from dotenv import load_dotenv 

load_dotenv()

st.set_page_config(page_title="FavBoard 💖", layout="centered")

st.title("💖 FavBoard")
st.write("Share your favorite things and explore others' favorites!")
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;} /* Hide hamburger menu */
    header {visibility: hidden;}    /* Hide Streamlit header */
    footer {visibility: hidden;}    /* Hide default footer */

    /* Custom sticky footer */
    .custom-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: gray;
        border-top: 1px solid #ddd;
        z-index: 9999;
    }
    </style>

    <div class="custom-footer">
        © 2025 Barai –  Built by <b>M-Ashraf-Barai</b>
    </div>
    """,
    unsafe_allow_html=True
)
# Google Sheet setup
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
WORKSHEET_NAME = os.getenv("GOOGLE_SHEET_WORKSHEET_NAME")

creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
client = gspread.authorize(creds)

sheet = client.open_by_key(SHEET_ID)
worksheet = sheet.worksheet(WORKSHEET_NAME)

# Ensure headers exist
expected_headers = [
    "Name", "Favorite Dish", "Favorite Fruit", "Favorite Drink", "Favorite Hobby",
    "Favorite Color", "Favorite Flower", "Favorite Type of People", "Favorite Perfume",
    "Favorite Time of Day", "Favorite Season", "Favorite Movie Genre",
    "Favorite Sports", "Favorite Sportman", "Favorite Country/Region to Visit"
]
existing_headers = worksheet.row_values(1)
if not existing_headers or existing_headers != expected_headers:
    worksheet.clear()
    worksheet.append_row(expected_headers)

# --- FORM SECTION ---
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

if not st.session_state.form_submitted:
    with st.form("MY_FAVOURITES"):
        name = st.text_input("Your Name")
        dish = st.text_input("Favorite Dish")
        fruit = st.text_input("Favorite Fruit")
        drink = st.text_input("Favorite Drink")
        hobby = st.text_input("Favorite Hobby")
        color = st.text_input("Favorite Color")
        flower = st.text_input("Favorite Flower")
        people = st.text_input("Favorite Type of People")
        perfume = st.text_input("Favorite Perfume")
        time = st.text_input("Favorite Time of Day")
        season = st.text_input("Favorite Season")
        movie = st.text_input("Favorite Movie Genre")
        sports = st.text_input("Favorite Sports")
        sportman = st.text_input("Favorite Sportman")
        place = st.text_input("Favorite Country/region to visit")
        submitted = st.form_submit_button("Submit")

        if submitted:
            if any([name, dish, fruit, drink, hobby, color, flower, people, perfume, time, season, movie, sportman, sports, place]) and name:
                worksheet.append_row([
                    name or "None", dish or "None", fruit or "None", drink or "None", hobby or "None",
                    color or "None", flower or "None", people or "None", perfume or "None",
                    time or "None", season or "None", movie or "None", sportman or "None", sports or "None", place or "None"
                ]) 
                st.session_state.form_submitted = True  # mark as done
                st.rerun()  # reload page cleanly (without form)
            else:
                st.error("⚠️ Please fill at least one field before submitting.")
else:
    st.success("🎉 Thank you! You’ve shared your favorites.")
    st.subheader("🌍 Everyone's Favorites")

    data = worksheet.get_all_records(expected_headers=expected_headers)
    if data:
        df = pd.DataFrame(data)
        df_transposed = df.set_index("Name").T
        st.dataframe(df_transposed)
    else:
        st.info("No data yet. Be the first to add your favorites!")
