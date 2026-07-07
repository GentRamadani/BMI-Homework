import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# -----------------------------
# MongoDB Connection
# -----------------------------

uri = st.secrets["MONGO_URI"]

client = MongoClient(uri, server_api=ServerApi("1"))

try:
    client.admin.command("ping")
    st.success("Connected to MongoDB!")
except Exception as e:
    st.error(f"MongoDB connection failed: {e}")

# Database and Collection

db = client["BMI_Database"]
collection = db["Users"]

# -----------------------------
# Streamlit App
# -----------------------------

st.title("BMI Calculator")

st.write("Enter your information below.")

# User Inputs

first_name = st.text_input("First Name")

last_name = st.text_input("Last Name")

height = st.number_input(
    "Height (meters)",
    min_value=0.50,
    max_value=2.50,
    step=0.01
)

weight = st.number_input(
    "Weight (kg)",
    min_value=1.0,
    max_value=300.0,
    step=0.1
)

# -----------------------------
# BMI Calculation
# -----------------------------

if st.button("Calculate BMI"):

    st.write("Height:", height)
    st.write("Weight:", weight)     


    if first_name == "" or last_name == "":
        st.warning("Please enter your first and last name.")

    else:

        bmi = weight / (height ** 2)

        st.subheader(f"Your BMI is: {bmi:.2f}")

        # BMI Category

        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal weight"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        st.write(f"**Category:** {category}")

        # Save data to MongoDB

        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "height": height,
            "weight": weight,
            "BMI": round(bmi, 2),
            "category": category
        }

        collection.insert_one(user_data)

        st.success("Your data has been saved successfully!")