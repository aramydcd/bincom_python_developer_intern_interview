# Election Results Management System

A multi-tab web application designed to visualize and manage election results from a relational database. This project was developed as part of a technical assessment to demonstrate proficiency in **SQL aggregation**, **database migration**, and **full-stack Python development**.

## 🚀 Features
* **Task 1: Polling Unit Viewer** – Instant retrieval of party scores for any specific polling unit.
* **Task 2: LGA Aggregator** – Real-time calculation of total scores across all polling units in a selected Local Government Area using SQL `SUM` and `JOIN`.
* **Task 3: Data Entry & Audit** – A secure form to input new results with an automated audit trail to track database activity.
* **Automated Migration** – Custom script to clean MySQL syntax and initialize a local SQLite database.

## 🛠️ Setup Instructions

### 1. Initialize the Database
Before running the app, you must convert the raw SQL dump into a SQLite database:
Bash
python init_db.py

This will create election_results.db in your folder.

### 2. Install Dependencies
Ensure you have Python installed, then run:

Bash
uv sync

### 3. Launch the Application
Start the Streamlit server:

Bash
streamlit run app.py

📂 File Structure
app.py: The Streamlit frontend (User Interface).

model.py: The data access layer containing all Raw SQL queries.

init_db.py: Migration script to clean and import bincom_test.sql.

bincom_test.sql: The source data file (MySQL format).

election_results.db: The generated SQLite database (created after running init).

💡 Technical Highlights
SQL Injection Prevention: Uses parameterized queries (?) for all user inputs.

Performance: Aggregations (SUM/GROUP BY) are handled at the database level for speed.

Architecture: Follows a clean separation of concerns between the UI (app.py) and the logic (model.py).
