import streamlit as st
import pandas as pd
import openai
from io import BytesIO
import os

# Initialize session state
if 'files' not in st.session_state:
    st.session_state.files = {}
if 'history' not in st.session_state:
    st.session_state.history = []
if 'feedback' not in st.session_state:
    st.session_state.feedback = []

# Set up OpenAI API key
api_key = st.text_input("Enter OpenAI API Key:", type="password")
if api_key:
    openai.api_key = api_key

# File uploader
st.header("AI-Powered Data Analysis App")
uploaded_files = st.file_uploader("Upload CSV/XLS files", accept_multiple_files=True, type=['csv', 'xls', 'xlsx'])

# Process uploaded files
for uploaded_file in uploaded_files:
    if uploaded_file.name not in st.session_state.files:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.session_state.files[uploaded_file.name] = df
            st.success(f"Successfully uploaded {uploaded_file.name}")
        except Exception as e:
            st.error(f"Error reading {uploaded_file.name}: {str(e)}")

# Display available files
if st.session_state.files:
    st.subheader("Available Files")
    for filename, df in st.session_state.files.items():
        st.write(f"- {filename} ({len(df)} rows, {len(df.columns)} columns)")

# Display top N rows
st.subheader("Display Top N Rows")
file_options = list(st.session_state.files.keys())
selected_file = st.selectbox("Select a file to view:", file_options if file_options else ["No files uploaded"])
if selected_file in st.session_state.files:
    n_rows = st.number_input("Enter number of rows (N):", min_value=1, max_value=len(st.session_state.files[selected_file]), value=5)
    if st.button("Show Top N Rows"):
        st.dataframe(st.session_state.files[selected_file].head(n_rows))

# Ask questions about the data using a form to avoid duplicate buttons
st.subheader("Ask Questions About Your Data")
file_options = list(st.session_state.files.keys())
selected_file_for_query = st.selectbox("Select file for query:", file_options if file_options else ["No files uploaded"])
prompt = st.text_area("Enter your question/prompt:")

with st.form(key="query_form"):
    submit_button = st.form_submit_button(label="Get Answer")
    if submit_button and prompt and selected_file_for_query in st.session_state.files and api_key:
        df = st.session_state.files[selected_file_for_query]
        csv_string = df.to_csv(index=False)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful data analyst. Analyze the provided CSV data and answer the user's question accurately."},
                    {"role": "user", "content": f"CSV Data:\n{csv_string}\n\nQuestion: {prompt}"}
                ],
                max_tokens=500,
                temperature=0.3
            )
            answer = response.choices[0].message.content
            st.session_state.history.append({
                "prompt": prompt,
                "file": selected_file_for_query,
                "answer": answer,
                "timestamp": pd.Timestamp.now()
            })
            st.success("Answer generated!")
            st.write("**Answer:**")
            st.write(answer)
        except Exception as e:
            st.error(f"Error generating answer: {str(e)}")
    elif submit_button:
        st.warning("Please upload a file, select a file for query, enter a prompt, and provide an API key.")

# Prompt History
st.subheader("Prompt History")
if st.session_state.history:
    for i, item in enumerate(st.session_state.history):
        with st.expander(f"Prompt: {item['prompt'][:50]}... (File: {item['file']})"):
            st.write(f"**Question:** {item['prompt']}")
            st.write(f"**Answer:** {item['answer']}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Useful", key=f"useful_{i}"):
                    st.session_state.feedback.append({"index": i, "feedback": "Useful"})
                    st.success("Thank you for your feedback!")
            with col2:
                if st.button("👎 Not Useful", key=f"not_useful_{i}"):
                    st.session_state.feedback.append({"index": i, "feedback": "Not Useful"})
                    st.success("Thank you for your feedback!")
else:
    st.info("No prompts yet. Ask a question above to start!")

# Feedback Summary
st.subheader("Feedback Summary")
if st.session_state.feedback:
    useful_count = sum(1 for f in st.session_state.feedback if f["feedback"] == "Useful")
    not_useful_count = sum(1 for f in st.session_state.feedback if f["feedback"] == "Not Useful")
    total_feedback = useful_count + not_useful_count
    if total_feedback > 0:
        useful_percentage = (useful_count / total_feedback) * 100
        not_useful_percentage = (not_useful_count / total_feedback) * 100
        st.write(f"**Useful Answers:** {useful_count} ({useful_percentage:.1f}%)")
        st.write(f"**Not Useful Answers:** {not_useful_count} ({not_useful_percentage:.1f}%)")
    else:
        st.write("No feedback provided yet.")
else:
    st.write("No feedback provided yet.")

# Clear history button
if st.button("Clear History"):
    st.session_state.history = []
    st.session_state.feedback = []
    st.rerun()

# Instructions sidebar
with st.sidebar:
    st.header("Instructions")
    st.write("""
    1. Enter your OpenAI API key (keep it secret!)
    2. Upload CSV or Excel files (e.g., Titanic dataset)
    3. Use "Display Top N Rows" to preview data
    4. Select a file and ask questions about it
    5. View history and provide feedback
    """)
    st.write("**Security Note:** Never commit API keys to Git. Use environment variables in production.")
