import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'cpe101finalproject'))
from firebase_config import db
from datetime import datetime

def add_expense(uid, category, amount, date, description="", time=None):
    # If time is provided, combine date and time into datetime string
    # Format: "YYYY-MM-DD HH:MM:SS" or "YYYY-MM-DDTHH:MM:SS"
    if time:
        # Handle both "HH:MM" and "HH:MM:SS" formats
        if len(time.split(':')) == 2:
            time = time + ":00"  # Add seconds if not present
        datetime_str = f"{date} {time}"
    else:
        # If no time provided, use current time
        now = datetime.now()
        datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    expense = {
        "uid": uid,
        "category": category,
        "amount": amount,
        "date": date,  # Keep date for backward compatibility
        "datetime": datetime_str,  # Store full datetime for sorting
        "description": description,
    }
    db.collection("expenses").add(expense)

def get_expenses(uid):
    docs = db.collection("expenses") \
             .where("uid", "==", uid) \
             .stream()

    expenses = []
    for doc in docs:
        expense_data = doc.to_dict()
        expense_data['id'] = doc.id  # Include document ID
        expenses.append(expense_data)
    return expenses

def delete_expense(uid, expense_id):
    """Delete an expense by document ID"""
    expense_ref = db.collection("expenses").document(expense_id)
    expense_doc = expense_ref.get()
    
    if not expense_doc.exists:
        return {"success": False, "error": "Expense not found"}
    
    expense_data = expense_doc.to_dict()
    if expense_data.get("uid") != uid:
        return {"success": False, "error": "Unauthorized"}
    
    expense_ref.delete()
    return {"success": True}

def add_category(uid, category_name):
    """Add a custom category for a user"""
    category_doc = db.collection("user_categories").document(uid).get()
    if category_doc.exists:
        categories = category_doc.to_dict().get("categories", [])
        if category_name.lower() not in [c.lower() for c in categories]:
            categories.append(category_name)
            db.collection("user_categories").document(uid).update({"categories": categories})
    else:
        db.collection("user_categories").document(uid).set({"categories": [category_name]})
    return {"success": True, "category": category_name}

def get_categories(uid):
    """Get all categories (default + custom) for a user"""
    default_categories = ["food", "transport", "shopping", "entertainment", "bills", "health", "education", "salary", "bonus", "other"]
    
    category_doc = db.collection("user_categories").document(uid).get()
    if category_doc.exists:
        custom_categories = category_doc.to_dict().get("categories", [])
        # Combine and remove duplicates
        all_categories = list(set(default_categories + custom_categories))
        return all_categories
    return default_categories

def search_transactions(uid, query):
    """Search transactions by category, description, or amount"""
    # Get all expenses for the user
    all_expenses = get_expenses(uid)
    
    if not query or not query.strip():
        return all_expenses
    
    query_lower = query.strip().lower()
    results = []
    
    for expense in all_expenses:
        # Search in category
        category = str(expense.get("category", "")).lower()
        # Search in description
        description = str(expense.get("description", "")).lower()
        # Search in amount (convert to string)
        amount = str(expense.get("amount", ""))
        
        # Check if query matches any field
        if (query_lower in category or 
            query_lower in description or 
            query_lower in amount):
            results.append(expense)
    
    return results