## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/todo_app.git
   cd todo_app

2. Install the dependencies required for the project:
pip install fastapi uvicorn pydantic sqlite3

## Execution

1.  Set Up the Database
python -c "from db import setup_database; setup_database()"

2. Running the Application
uvicorn todo_app.main:app --reload

## TO access

1. Open your browser and navigate to:
http://127.0.0.1:8000/docs




