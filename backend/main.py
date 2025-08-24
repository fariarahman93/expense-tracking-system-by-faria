
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from db_helper import (
    insert_expenses_for_date,
    fetch_expenses_for_date,
    delete_expenses_for_date,
    fetch_expense_summary,
    get_monthly_expenses_range,  # <-- NEW NAME
)

app = FastAPI()

class Expense(BaseModel):
    expense_date: str
    amount: float
    category: str
    notes: str | None = None

class AnalyticsRequest(BaseModel):
    start_date: str
    end_date: str

@app.post("/expenses/")
def add_expense(expense: Expense):
    insert_expenses_for_date(expense.expense_date, expense.amount, expense.category, expense.notes)
    return {"message": "Expense added successfully"}

@app.get("/expenses/{expense_date}")
def get_expenses(expense_date: str):
    return fetch_expenses_for_date(expense_date)

@app.delete("/expenses/{expense_date}")
def delete_expenses(expense_date: str):
    delete_expenses_for_date(expense_date)
    return {"message": f"Expenses for {expense_date} deleted successfully"}

@app.post("/analytics/")
def analytics(request: AnalyticsRequest) -> Dict[str, Any]:
    data = fetch_expense_summary(request.start_date, request.end_date)
    total_sum = sum(item["total"] for item in data)
    return {
        item["category"]: {
            "total": float(item["total"]),
            "percentage": round((item["total"] / total_sum) * 100, 2) if total_sum > 0 else 0
        }
        for item in data
    }

@app.post("/monthly_expenses")
def monthly_expenses(request: AnalyticsRequest):
    try:
        return get_monthly_expenses_range(request.start_date, request.end_date)
    except TypeError as e:
        # If you still have an old 0-arg function being imported, this will catch it.
        raise HTTPException(status_code=500, detail=f"db_helper.get_monthly_expenses_range must accept (start_date, end_date): {e}")
