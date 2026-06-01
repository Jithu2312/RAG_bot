import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/rag"

st.set_page_config(page_title="RepoLens", page_icon="🔍", layout="wide")

st.title("🔍 RepoLens")
st.caption("AI-powered Repository Understanding Assistant")

# ------------------
# Session ID
# ------------------

session_id = st.text_input("Session ID", value="user_1")

# ------------------
# Repo Ingestion
# ------------------

st.subheader("Repository Ingestion")

repo_url = st.text_input("GitHub Repository URL")

if st.button("Index Repository"):

    payload = {"repo_url": repo_url}

    response = requests.post(f"{API_URL}/ingest-repo", json=payload)

    if response.status_code == 200:
        st.success("Repository indexed successfully")
        st.json(response.json())
    else:
        st.error(response.text)

# ------------------
# Query Section
# ------------------

st.subheader("Ask Questions")

question = st.text_area("Question", height=120)

if st.button("Ask RepoLens"):

    payload = {"question": question, "session_id": session_id}

    response = requests.post(f"{API_URL}/query-repo", json=payload)

    if response.status_code == 200:

        answer = response.json()["answer"]

        st.markdown("### Answer")

        st.write(answer)

    else:
        st.error(response.text)
