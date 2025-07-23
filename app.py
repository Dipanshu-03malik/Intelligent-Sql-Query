from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
import google.generativeai as genai
from google.api_core.exceptions import NotFound 

# Configure our Google Gemini API KEY
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def list_gemini_models():
    """Lists available Gemini models that support generateContent."""
    st.sidebar.subheader("Available Gemini Models:")
    found_models = False
    try:
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                st.sidebar.write(f"- {m.name} ({m.display_name})")
                found_models = True
    except Exception as e:
        st.sidebar.error(f"Error listing models: {e}")
    if not found_models:
        st.sidebar.write("No models found that support 'generateContent' with your current API key and region.")
    st.sidebar.markdown("---")
list_gemini_models()


# Function to load Google Gemini model and get SQL query response
def get_gemini_response(question, prompt_text):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash') 
        response = model.generate_content([prompt_text, question])
        return response.text
    except NotFound as e:
        st.error(f"Model Not Found Error: {e}. Please check if the model name is correct and available in your region.")
        st.error("You can use the 'Available Gemini Models' section in the sidebar to find valid model names.")
        return "" 
    except Exception as e:
        st.error(f"An unexpected error occurred with Gemini API: {e}")
        return ""


# Function to retrieve query from SQL database
def read_sql_query(sql, db):
    conn = None 
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        return rows
    except sqlite3.Error as e:
        st.error(f"Database error during query execution: {e}. Please check the generated SQL query.")
        st.code(f"Generated SQL: {sql}", language="sql")
        return [] 
    finally:
        if conn: 
            conn.close()


# DEFINE THE PROMPT for the Gemini model
prompt = """
    You are an expert in converting English questions to SQL query! The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION and MARKS.
    For example:
    Example 1 - How many entries of records are present?, the SQL command will be something like this: SELECT COUNT(*) FROM STUDENT;
    Example 2 - Tell me all the students studying in Data Science class?, the SQL command will be something like this: SELECT * FROM STUDENT WHERE CLASS="Data Science";
    The SQL code should NOT have ``` (backticks) in the beginning or end, and should NOT include the word 'sql' in the output.
"""

# Streamlit UI
st.set_page_config(page_title="Intelligent SQL Query Retriever")
st.header("Gemini App to Retrieve Data from SQL Database")

question = st.text_input("Enter your question about the student data:", key="input_question")
submit = st.button("Ask Gemini")

if submit:
    # Get the SQL query from Gemini
    generated_sql_query = get_gemini_response(question, prompt)

    if generated_sql_query: 
        print(f"Generated SQL Query: {generated_sql_query}") # P
        # Execute the SQL query on your database
        # Ensure the database file name matches what you used in SQL_PY.py for connection
        data_from_db = read_sql_query(generated_sql_query, "student.db")

        st.subheader("Results from the Database:")
        if data_from_db:
            for row in data_from_db:
                st.write(row)
        else:
            st.write("No data found for your query or an error occurred during SQL execution.")
    else:
        st.write("Gemini could not generate a valid SQL query. Please try rephrasing your question or check the API key/model.")