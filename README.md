# Text-to-SQL RAG Chatbot

A natural-language-to-SQL chatbot that allows users to ask questions about a MySQL database using plain English. The system uses an LLM with database schema context to generate SQL queries and evaluates the generated responses using Ragas.

##  Project Overview

The project converts natural-language questions into SQL queries and executes them against a MySQL database.

For example:

> "What are the names of all products in the products table?"

The system provides the database schema to the LLM, which generates the corresponding SQL query.

##  Architecture

```text
User Question
      ↓
Database Schema
      ↓
LangChain Prompt
      ↓
Gemini LLM
      ↓
SQL Query
      ↓
MySQL Database
      ↓
Query Result
      ↓
Ragas Evaluation
```
##  Technologies Used
- Python
- LangChain
- Google Gemini
- MySQL
- Ragas
- Groq
- Hugging Face Embeddings
- Jupyter Notebook

##  Features

- Natural-language-to-SQL query generation
- MySQL database integration
- Database schema-aware SQL generation
- LangChain-based LLM pipeline
- SQL query execution
- Ragas-based evaluation
- Context precision evaluation
- Response helpfulness evaluation

##  Dataset

The project uses a relational sales and business dataset stored in MySQL.

The database contains the following tables:

- `customers`
- `products`
- `sales_order`
- `regions`
- `state_regions`
- `2017_budgets`

The dataset is included in this repository for demonstration and reproducibility.

##  Project Workflow

1. Connect to the MySQL database.
2. Retrieve the database schema.
3. Provide the schema and user question to the LLM.
4. Generate the SQL query.
5. Execute the SQL query against MySQL.
6. Collect generated responses.
7. Evaluate the responses using Ragas.

##  Evaluation Results

The system was evaluated using a 5-question evaluation dataset.

| Metric | Result |
|---|---:|
| Context Precision | 1.0000 |
| Helpfulness | 4.0000 / 5 |

##  Project Notebooks

### `gemini chatbot.ipynb`

Contains the main Text-to-SQL chatbot implementation using LangChain, Gemini and MySQL.

### `gemini chatbot rag.ipynb`

Contains the Ragas evaluation workflow used to evaluate the generated responses.

##  Future Improvements

- Add a web-based chatbot interface
- Add SQL validation before execution
- Handle SQL generation errors automatically
- Add more evaluation questions
- Add additional Ragas evaluation metrics
- Improve handling of complex multi-table queries
