import re
from urllib.parse import quote_plus

import streamlit as st

from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI


# ---------------------------------------------------------
# Streamlit Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Text-to-SQL RAG Chatbot",
    page_icon="🤖",
    layout="centered"
)


# ---------------------------------------------------------
# Database Connection
# ---------------------------------------------------------

@st.cache_resource
def get_database():

    host = st.secrets["DB_HOST"]
    port = int(st.secrets["DB_PORT"])
    username = st.secrets["DB_USER"]
    password = st.secrets["DB_PASSWORD"]
    database_name = st.secrets["DB_NAME"]

    # Encode password in case it contains special characters
    password_encoded = quote_plus(password)

    mysql_uri = (
        f"mysql+pymysql://"
        f"{username}:{password_encoded}"
        f"@{host}:{port}/{database_name}"
    )

    db = SQLDatabase.from_uri(
        mysql_uri,
        sample_rows_in_table_info=2
    )

    return db


# ---------------------------------------------------------
# Gemini LLM
# ---------------------------------------------------------

@st.cache_resource
def get_llm():

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        api_key=st.secrets["GOOGLE_API_KEY"]
    )

    return llm


# ---------------------------------------------------------
# SQL Prompt
# ---------------------------------------------------------

template = """
Based on the table schema below, write a SQL query that would answer
the user's question.

Rules:
- Only provide the SQL query.
- Do not provide explanations.
- Do not use markdown code fences.
- Return the SQL query in a single line.
- Only generate SELECT queries.
- Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE,
  TRUNCATE, or other data-modifying queries.

Table Schema:
{schema}

Question:
{question}

SQL Query:
"""


prompt = ChatPromptTemplate.from_template(template)


# ---------------------------------------------------------
# Get Database Schema
# ---------------------------------------------------------

def get_schema(db):

    return db.get_table_info()


# ---------------------------------------------------------
# Create SQL Generation Chain
# ---------------------------------------------------------

def get_sql_chain(db, llm):

    sql_chain = (
        RunnablePassthrough.assign(
            schema=lambda _: get_schema(db)
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return sql_chain


# ---------------------------------------------------------
# Clean Generated SQL
# ---------------------------------------------------------

def clean_sql(sql):

    sql = re.sub(
        r"```sql|```",
        "",
        sql,
        flags=re.IGNORECASE
    )

    sql = sql.strip()

    # Remove accidental "SQL Query:" prefix
    sql = re.sub(
        r"^SQL\s*Query\s*:\s*",
        "",
        sql,
        flags=re.IGNORECASE
    )

    return sql.strip()


# ---------------------------------------------------------
# Validate SQL
# ---------------------------------------------------------

def validate_sql(sql):

    sql_upper = sql.strip().upper()

    if not sql_upper.startswith("SELECT"):
        raise ValueError(
            "Only SELECT queries are allowed."
        )

    forbidden_keywords = [
        "INSERT ",
        "UPDATE ",
        "DELETE ",
        "DROP ",
        "ALTER ",
        "CREATE ",
        "TRUNCATE ",
        "REPLACE ",
        "GRANT ",
        "REVOKE "
    ]

    for keyword in forbidden_keywords:

        if keyword in sql_upper:
            raise ValueError(
                "Unsafe SQL query detected."
            )


# ---------------------------------------------------------
# Ask Database
# ---------------------------------------------------------

def ask_database(question):

    db = get_database()
    llm = get_llm()

    sql_chain = get_sql_chain(
        db,
        llm
    )

    sql_query = sql_chain.invoke(
        {
            "question": question
        }
    )

    sql_query = clean_sql(sql_query)

    validate_sql(sql_query)

    result = db.run(sql_query)

    return sql_query, result


# ---------------------------------------------------------
# Main Application
# ---------------------------------------------------------

st.title("🤖 Text-to-SQL RAG Chatbot")

st.write(
    "Ask questions about the sales database using natural language."
)

st.info(
    "Ask a question in plain English. "
    "Gemini will generate SQL and execute it against the MySQL database."
)


# ---------------------------------------------------------
# User Input
# ---------------------------------------------------------

question = st.text_input(
    "Ask a question",
    placeholder="Example: What was the budget of Product 12?"
)


# ---------------------------------------------------------
# Process Question
# ---------------------------------------------------------

if question:

    with st.spinner(
        "Generating SQL and querying the database..."
    ):

        try:

            sql_query, result = ask_database(
                question
            )

            st.subheader("Generated SQL")

            st.code(
                sql_query,
                language="sql"
            )

            st.subheader("Database Result")

            st.write(result)

        except Exception as e:

            st.error(
                "Something went wrong while connecting to the database "
                "or generating the SQL query."
            )

            st.exception(e)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("About")

    st.write(
        "This application converts natural-language questions "
        "into SQL queries using Google Gemini and LangChain."
    )

    st.write("### Technologies")

    st.write(
        """
        - Python
        - Streamlit
        - LangChain
        - Google Gemini
        - MySQL
        - Ragas
        """
    )

    st.write("### Database Tables")

    st.write(
        """
        - customers
        - products
        - sales_order
        - regions
        - state_regions
        - 2017_budgets
        """
    )