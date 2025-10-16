import streamlit as st
import json
import os

DATA_FILE = "garage_records.json"

# Load or create data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# App setup
st.title("🚗 Garage Record System")
data = load_data()

# Input for vehicle number
car_number = st.text_input("Enter Vehicle Number").upper().strip()

if car_number:
    # Show existing records
    if car_number in data:
        st.subheader(f"Service History for {car_number}")
        for i, record in enumerate(data[car_number], 1):
            st.write(f"{i}. {record['date']} - {record['service']} (Cost: {record['cost']})")
    else:
        st.info(f"No records found for {car_number}.")

    # Add new service
    st.subheader("Add New Service")
    with st.form(key="service_form"):
        service = st.text_input("Service Performed")
        date = st.date_input("Date")
        cost = st.text_input("Cost (optional)")
        submit = st.form_submit_button("Add Service")

        if submit:
            if not service:
                st.error("Service field is required!")
            else:
                record = {"service": service, "date": str(date), "cost": cost}
                data.setdefault(car_number, []).append(record)
                save_data(data)
                st.success(f"Added new service for {car_number}!")
                st.experimental_rerun()  # Refresh to show new record

