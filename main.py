import streamlit as st
import requests
import base64
import json
import datetime
import re

# Function to extract the sheet name from the URL
def extract_sheet_name(sheet_url):
    # Extract the sheet name from the URL using regex
    match = re.search(r'/([^/]+)$', sheet_url)
    if match:
        return match.group(1)
    else:
        return None

# Function to send data to Sheety API
def send_to_sheety(auth_token, sheet_url, data):
    sheet_name = extract_sheet_name(sheet_url)
    if not sheet_name:
        st.error("Invalid Sheety URL. Could not extract sheet name.")
        return None
    
    headers = {
        'Authorization': f'Basic {auth_token}',
        'Content-Type': 'application/json'
    }

    # Constructing the correct body structure
    body = {
        sheet_name: {
            "date": datetime.datetime.now().strftime("%Y%m%d"),
            "data": json.dumps(data)  # Wrap the data as a string in the "data" field
        }
    }
    
    response = requests.post(sheet_url, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to send data to Sheety. Status code: {response.status_code}")
        return None

# Function to retrieve data from Sheety API
def get_from_sheety(auth_token, sheet_url):
    headers = {
        'Authorization': f'Basic {auth_token}'
    }
    response = requests.get(sheet_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to retrieve data from Sheety. Status code: {response.status_code}")
        return None

# Function to send data to Pixela API
def send_to_pixela(auth_token, pixela_url, data):
    headers = {
        'X-USER-TOKEN': auth_token,
        'Content-Type': 'application/json'
    }
    response = requests.post(pixela_url, headers=headers, json={
        "date": datetime.datetime.now().strftime("%Y%m%d"),
        "quantity": str(data)
    })
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to send data to Pixela. Status code: {response.status_code}")
        return None

# Function to retrieve data from Pixela API
def get_from_pixela(auth_token, pixela_url):
    svg_content = pixela_url
    return svg_content


# Streamlit app starts here
st.set_page_config(page_title="Data Submission & Retrieval App", page_icon="📝", layout="wide")

# Header with an image
st.image("https://via.placeholder.com/800x200.png?text=Data+Submission+App", use_column_width=True)
st.title("Data Submission & Retrieval App")

# Sheety Section
st.header("Sheety API Integration")
sheety_auth = st.text_input("Enter your Sheety API Basic Authorization string:", type="password")
sheety_url = st.text_input("Enter Sheety API URL:", value="https://api.sheety.co/YOUR_URL_HERE")
sheety_data_input = st.text_area("Enter the JSON data to send to Sheety:", height=200)

if st.button("Send Data to Sheety"):
    if sheety_auth and sheety_data_input:
        try:
            sheety_data = json.loads(sheety_data_input)  # Converting string input to dictionary
            response = send_to_sheety(sheety_auth, sheety_url, sheety_data)
            if response:
                st.success("Data successfully sent to Sheety!")
                st.json(response)
        except Exception as e:
            st.error(f"Error parsing JSON input: {e}")
    else:
        st.error("Please enter both the Authorization string and JSON data.")

if st.button("Retrieve Data from Sheety"):
    if sheety_auth and sheety_url:
        response = get_from_sheety(sheety_auth, sheety_url)
        if response:
            st.success("Data successfully retrieved from Sheety!")
            st.json(response)
    else:
        st.error("Please enter both the Authorization string and the Sheety API URL.")

# Separator
st.markdown("---")

# Pixela Section
st.header("Pixela Task Tracker Integration")
pixela_token = st.text_input("Enter your Pixela API token:", type="password")
pixela_url = st.text_input("Enter Pixela API URL:", value="https://pixe.la/v1/users/YOUR_USERNAME/graphs/YOUR_GRAPH_ID")
pixela_data_input = st.text_area("Enter the JSON data to send to Pixela:", height=200)

if st.button("Send Data to Pixela"):
    if pixela_token and pixela_data_input:
        try:
            pixela_data = json.loads(pixela_data_input)  # Converting string input to dictionary
            response = send_to_pixela(pixela_token, pixela_url, pixela_data)
            if response:
                st.success("Data successfully sent to Pixela!")
                st.json(response)
        except Exception as e:
            st.error(f"Error parsing JSON input: {e}")
    else:
        st.error("Please enter both the Pixela API token and JSON data.")

if st.button("Retrieve Data from Pixela"):
    if pixela_token and pixela_url:
        svg_content = get_from_pixela(pixela_token, pixela_url)
        if svg_content:
            st.success("Data successfully retrieved from Pixela!")
            # Display SVG content
            st.markdown(svg_content, unsafe_allow_html=True)
    else:
        st.error("Please enter both the Pixela API token and the Pixela API URL.")
