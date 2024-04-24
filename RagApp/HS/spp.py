import streamlit as st
import requests
import json
# Create a Streamlit app
st.title("LLM App")

from django.views.decorators.csrf import csrf_exempt 

session = requests.Session()
response = session.get("http://localhost:8000/HS/file_interaction")
csrf_token = response.cookies.get("csrftoken")

headers = {"X-CSRFToken": csrf_token}


# Create a form with a file uploader and text input
with st.form("upload_form"):
    file_uploader = st.file_uploader("Upload a file")
    submit_button = st.form_submit_button("Upload")

# When the user submits the form, send a POST request to the Django app's API endpoint

if submit_button:
    file_data = file_uploader.getvalue()
    response = session.post("http://localhost:8000/HS/file_interaction", files={"file": file_data}, headers=headers)
    if response.status_code == 200:
        document_id = response.json()["document_id"]
        llm = response.json()["llm"]
    else:
        st.error(f"Error: {response.status_code} - {response.reason}")

    # Create a new form for the user to ask a question
    with st.form("query_form"):
        query_input = st.text_input("Ask a question")
        submit_button = st.form_submit_button("Ask")

    # When the user submits the query form, send a POST request to the Django app's API endpoint
    if submit_button:
        query_data = query_input
        response = session.post("http://locahost:8000/HS/query_view", data={"document_id": document_id, "query": query_data}, headers=headers)
        answer = response.json()["answer"]
        st.write("Answer:", answer)