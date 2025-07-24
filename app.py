import streamlit as st
import os
import sqlite3
import google.generativeai as genai
from google.api_core.exceptions import NotFound
import tempfile # For handling temporary uploaded files
import pandas as pd # Import pandas for DataFrame creation

# Load environment variables from .env file (for GOOGLE_API_KEY)
from dotenv import load_dotenv
load_dotenv()

# Configure our Google Gemini API KEY
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Helper function to list available Gemini models (for debugging model 404) ---
# This function is helpful for debugging if you encounter model not found errors.
def list_gemini_models():
    """Lists available Gemini models that support generateContent."""
    st.sidebar.subheader("Available AI Models (generateContent):") # Changed from Gemini Models
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

# Call this function to display available models in the sidebar for debugging
list_gemini_models()
# --- End of helper function ---

# Function to get database schema (table names and column info)
def get_database_schema(db_path):
    """
    Connects to a SQLite database and retrieves its schema (table names and columns).
    Returns a string formatted for the AI prompt.
    """
    conn = None
    schema_info = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table_name_tuple in tables:
            table_name = table_name_tuple[0]
            schema_info.append(f"Table: {table_name}")
            schema_info.append("Columns:")
            
            # Get column info for each table
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                schema_info.append(f"  - {col_name} ({col_type})")
            schema_info.append("") # Add a blank line for readability

    except sqlite3.Error as e:
        st.error(f"Error reading database schema: {e}")
        return ""
    finally:
        if conn:
            conn.close()
    
    return "\n".join(schema_info)

# Function to load Google AI model and get SQL query response
def get_gemini_response(question, db_schema): # Function name remains get_gemini_response for consistency with genai lib
    """
    Sends the user's question and database schema to AI to get a SQL query.
    """
    # Define the prompt for the AI model dynamically
    prompt_text = f"""
    You are an expert in converting English questions to SQL queries.
    The SQL database schema is provided below:

    {db_schema}

    For example:
    - If the user asks "How many entries of records are present in the STUDENT table?", the SQL command should be: SELECT COUNT(*) FROM STUDENT;
    - If the user asks "Tell me all the students studying in Data Science class from the STUDENT table?", the SQL command should be: SELECT * FROM STUDENT WHERE CLASS="Data Science";
    - If the user asks "What are the names of all employees in the Employees table?", the SQL command should be: SELECT name FROM Employees;

    Please provide only the SQL query as the response, without any additional text, markdown formatting (like ```sql), or keywords like 'undefined'.
    Ensure the SQL query is valid for SQLite.
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash') # Model name remains 'gemini-1.5-flash' as it's the actual API model ID
        response = model.generate_content([prompt_text, question])
        generated_text = response.text.strip()

        # --- CRUCIAL ADDITION: Clean the generated SQL query ---
        # Remove markdown code block delimiters and any leading/trailing whitespace
        if generated_text.startswith("```sql"):
            generated_text = generated_text[len("```sql"):].strip()
        if generated_text.endswith("```"):
            generated_text = generated_text[:-len("```")].strip()
        
        # Remove the "undefined" keyword if it appears at the end
        if generated_text.lower().endswith("undefined"):
            generated_text = generated_text[:-len("undefined")].strip()
        # --- End of cleaning ---

        return generated_text
    except NotFound as e:
        st.error(f"Model Not Found Error: {e}. Please check if the model name is correct and available in your region.")
        st.error("You can use the 'Available AI Models' section in the sidebar to find valid model names.") # Changed from Gemini Models
        return "" # Return empty string on error
    except Exception as e:
        st.error(f"An unexpected error occurred with AI API: {e}") # Changed from Gemini API
        return "" # Return empty string on other errors

# Function to retrieve query from SQL database
def read_sql_query(sql, db_path):
    """
    Connects to the specified SQLite database and executes the given SQL query.
    Returns the fetched rows.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        # For SELECT queries, commit is not strictly necessary but harmless.
        # For INSERT/UPDATE/DELETE, it's crucial.
        conn.commit() 
        return rows
    except sqlite3.Error as e:
        st.error(f"Database error during query execution: {e}. This likely means the generated SQL is malformed or invalid for your database schema.")
        st.code(f"Problematic SQL: {sql}", language="sql") # Show the problematic SQL for debugging
        return []
    finally:
        if conn:
            conn.close()

# Streamlit UI
st.set_page_config(page_title="Intelligent SQL Query Retriever", layout="centered", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
    .main-header {
        font-size: 3em;
        font-weight: bold;
        color: #4CAF50; /* Green color */
        text-align: center;
        margin-bottom: 0.5em;
    }
    .subheader {
        font-size: 1.5em;
        color: #333333;
        text-align: center;
        margin-bottom: 1.5em;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        font-size: 1.2em;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.3);
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #cccccc;
        padding: 10px;
        font-size: 1.1em;
    }
    .stFileUploader>div>div>button {
        background-color: #2196F3; /* Blue color */
        color: white;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        font-size: 1.1em;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    .stFileUploader>div>div>button:hover {
        background-color: #0b7dda;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.3);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='main-header'>✨ AI-Powered SQL Query App ✨</h1>", unsafe_allow_html=True) # Changed from Gemini-Powered
st.markdown("<p class='subheader'>Upload your SQLite database file (.db) and ask questions about its data using natural language.</p>", unsafe_allow_html=True)

st.divider() # Visual separator

# File uploader for the database
uploaded_file = st.file_uploader("📂 Upload your SQLite Database (.db file)", type=["db"])

db_path = None
if uploaded_file is not None:
    # Create a temporary file to store the uploaded database
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        db_path = tmp_file.name
    st.success(f"✅ Database '{uploaded_file.name}' uploaded successfully!")

    # Display the schema of the uploaded database in an expander
    with st.expander("🔍 View Uploaded Database Schema"):
        schema_display = get_database_schema(db_path)
        if schema_display:
            st.code(schema_display, language="text") # Use st.code for schema display
        else:
            st.warning("⚠️ Could not retrieve schema for the uploaded database. Please ensure it's a valid SQLite .db file.")
            db_path = None # Invalidate db_path if schema retrieval failed

st.divider() # Visual separator

if db_path:
    st.subheader("❓ Ask a Question About Your Data")
    question = st.text_input("Enter your question (e.g., 'Show me all students in 10th grade', 'What is the average marks in section A?'):", key="input_question")
    
    # Center the button
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        submit = st.button("🚀 Ask AI") # Changed from Ask Gemini

    if submit and question:
        with st.spinner("🧠 Generating SQL query and fetching data..."):
            # Get the database schema for the prompt
            current_db_schema = get_database_schema(db_path)
            
            # Get the SQL query from AI
            generated_sql_query = get_gemini_response(question, current_db_schema) # Function call remains get_gemini_response

            if generated_sql_query:
                st.subheader("📝 Generated SQL Query:")
                st.code(generated_sql_query, language="sql")
                
                # Execute the SQL query on your database
                data_from_db = read_sql_query(generated_sql_query, db_path)

                st.subheader("📊 Results from the Database:")
                if data_from_db:
                    # Display results using Pandas DataFrame for proper column naming
                    conn_temp = sqlite3.connect(db_path)
                    cur_temp = conn_temp.cursor()
                    try:
                        cur_temp.execute(generated_sql_query)
                        col_names = [description[0] for description in cur_temp.description]
                        df = pd.DataFrame(data_from_db, columns=col_names)
                        st.dataframe(df) # Pass the DataFrame directly
                    except sqlite3.Error as e:
                        st.error(f"❌ Error displaying results: {e}")
                        st.write("Raw data (if available):")
                        for row in data_from_db: 
                            st.write(row)
                    finally:
                        conn_temp.close()
                else:
                    st.write("🤷 No data found for your query or an error occurred during SQL execution. Please review the generated SQL and any error messages above.")
            else:
                st.warning("🤔 AI could not generate a valid SQL query. Please try rephrasing your question or check the API key/model configuration.") # Changed from Gemini
    elif submit and not question:
        st.warning("Please enter a question.")
else:
    st.info("⬆️ Please upload a SQLite database file to proceed.")

st.markdown("---")
st.markdown("Developed with ❤️ using Streamlit and Google AI API.") 
