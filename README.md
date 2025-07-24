# Intelligent SQL Query Retriever

This project demonstrates a Streamlit web application that leverages the Google Gemini API to convert natural language questions into SQL queries. These generated SQL queries are then executed against a local SQLite database, and the results are displayed in the web interface.

## Features

* **Natural Language to SQL:** Ask questions in plain English about your student database.
* **Gemini API Integration:** Utilizes Google's Gemini model to interpret questions and generate accurate SQL.
* **SQLite Database:** Stores student data locally.
* **Streamlit UI:** Provides an interactive and user-friendly web interface.

## Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.8+**
* **Anaconda or Miniconda** (recommended for environment management)

## Setup

Follow these steps to set up and run the project locally.

### 1. Clone the Repository (if applicable)

If this is part of a larger repository, clone it first:

```bash
git clone <your-repository-url>
cd <your-project-directory>
```

### 2. Create and Activate Conda Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
conda create -n sql_gemini_env python=3.9 -y
conda activate sql_gemini_env
```
*(Note: If you prefer `venv` over Conda, you would use `python -m venv venv` and `source venv/bin/activate` or `venv\Scripts\activate` on Windows.)*

### 3. Install Requirements

Navigate to your project directory and install the necessary Python packages. First, ensure you have a `requirements.txt` file (its content is provided in the next section).

```bash
pip install -r requirements.txt
```

### 4. Set Up Google Gemini API Key

1.  Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and create a new API key.
2.  In your project's root directory, create a file named `.env`.
3.  Add your API key to this `.env` file in the following format:

    ```
    GOOGLE_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
    ```
    **Replace `YOUR_ACTUAL_GEMINI_API_KEY` with the key you obtained from Google AI Studio.**

### 5. Initialize the SQLite Database

The `SQL_PY.py` script creates the `student.db` database and populates it with sample student data. You only need to run this once.

```bash
python SQL_PY.py
```
This will create a `student.db` file in your project directory.

## Running the Application

Once the setup is complete, you can run the Streamlit application:

```bash
streamlit run APP_PY.py
```

This command will open the Streamlit application in your default web browser. If it doesn't open automatically, it will provide a local URL (e.g., `http://localhost:8501`) that you can copy and paste into your browser.

## Usage

1.  **Enter your question:** In the Streamlit web interface, type a question related to the student data (e.g., "What is the average marks of students?", "Show me all students in 10th class?", "Who has the highest marks?").
2.  **Click "Ask Gemini":** The application will send your question to the Gemini model, which will convert it into an SQL query.
3.  **View Results:** The generated SQL query will be executed against your `student.db` database, and the results will be displayed on the page.

## Deployment

*(Once deployed, you can add your live application link here)*

**Deployed Application Link:** [https://dipanshu-03malik-intelligent-sql-query-app-etmwzd.streamlit.app/]

## Troubleshooting

* **`TypeError: Could not create Blob... Got a: <class 'list'>`**: This error indicates that the `prompt` variable in `APP_PY.py` is defined as a list instead of a string. Ensure your `prompt` variable is a plain string.
* **`404 models/gemini-pro is not found`**: This means the specified Gemini model is not available or accessible with your API key in your region.
    * Check your terminal output when running `APP_PY.py` for "Available Gemini Models" list.
    * Update the model name in `get_gemini_response` function in `APP_PY.py` to one of the listed available models (e.g., `gemini-1.5-flash`).
    * Ensure your `GOOGLE_API_KEY` in the `.env` file is correct and has access to Gemini models.
* **`Database error during query execution: near "```sql"`**: This means the Gemini model included markdown formatting (```sql`) or extra words (`undefined`) in the generated SQL. The `APP_PY.py` includes post-processing to remove these, but if it persists, ensure your `APP_PY.py` is updated to the latest version provided.
* **"No data found" or unexpected results**:
    * Verify your `SQL_PY.py` ran successfully and populated `student.db`.
    * Check the "Generated SQL Query" printed in your terminal (where you ran `streamlit run`). Copy and paste this query directly into a SQLite browser to see if it works as expected. This helps determine if the issue is with SQL generation or database retrieval.
