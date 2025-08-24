
import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger("db_helper")


# -------------------- DB Connection Helper --------------------

@contextmanager
def get_db_cursor(commit=False):
    """
    Context manager to get a DB cursor with optional commit.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",          # 🔹 change if your DB password is different
        database="expense_manager"
    )
    cursor = connection.cursor(dictionary=True)
    try:
        yield cursor
        if commit:
            connection.commit()
    finally:
        cursor.close()
        connection.close()


# -------------------- Expense Functions --------------------

def insert_expenses_for_date(expense_date, amount, category, notes=None):
    """
    Insert a new expense record into the DB.
    """
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            INSERT INTO expenses (expense_date, amount, category, notes)
            VALUES (%s, %s, %s, %s)
            """,
            (expense_date, amount, category, notes)
        )
    logger.info(f"Inserted expense on {expense_date}: {amount} - {category}")


def fetch_expenses_for_date(expense_date):
    """
    Fetch all expenses for a given date.
    """
    with get_db_cursor() as cursor:
        cursor.execute(
            """
            SELECT id, expense_date, amount, category, notes
            FROM expenses
            WHERE expense_date = %s
            ORDER BY id
            """,
            (expense_date,)
        )
        rows = cursor.fetchall()
    return rows


def delete_expenses_for_date(expense_date):
    """
    Delete all expenses for a given date.
    """
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            DELETE FROM expenses
            WHERE expense_date = %s
            """,
            (expense_date,)
        )
    logger.info(f"Deleted all expenses for {expense_date}")


def fetch_expense_summary(start_date, end_date):
    """
    Fetch expense totals grouped by category between two dates.
    Returns: [{"category": "Food", "total": 200}, ...]
    """
    with get_db_cursor() as cursor:
        cursor.execute(
            """
            SELECT category, SUM(amount) AS total
            FROM expenses
            WHERE expense_date BETWEEN %s AND %s
            GROUP BY category
            ORDER BY total DESC
            """,
            (start_date, end_date)
        )
        rows = cursor.fetchall()
    return rows


# -------------------- Monthly Expenses Function --------------------

def get_monthly_expenses_range(start_date, end_date):
    """
    Fetch total expenses grouped by month between two dates.
    Returns: {"2024-08": 1200.0, "2024-09": 950.0}
    """
    with get_db_cursor() as cursor:
        cursor.execute(
            """
            SELECT DATE_FORMAT(expense_date, '%Y-%m') AS month,
                   SUM(amount) AS total_amount
            FROM expenses
            WHERE expense_date BETWEEN %s AND %s
            GROUP BY month
            ORDER BY month
            """,
            (start_date, end_date)
        )
        rows = cursor.fetchall()

    # Convert result to dictionary
    return {row["month"]: float(row["total_amount"]) for row in rows}
