## Expense Management System
This project is an expense management system that consists of a Streamlit frontend application and a FastAPI server.
### Project Structure
- **frontend**: Contains the Streamlit application code.  
- **backend**: Contains the FastAPI backend server code.  
- **test**: Contains the test cases for both frontend and backend.  
- **requirements**: Contains the dependencies and package requirements for the project.  
- **README.md**: Provides project documentation and usage instructions.  
## Setup Instructions
1. Clone the repository  
   ```bash
    git clone https://github.com/fariarahman93/expense-management-system.git
    cd expense-management-system
2. Install dependencies
   ```commandline
    pip install -r requirements.txt
3. Start the backend server
   ```commandline
    uvicorn backend.main:app --reload
4. Start the frontend
   ```commandline
    streamlit run frontend/app.py
