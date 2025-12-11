from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def analyze_expenses(expenses, uid=None):
    """
    Analyze expenses and provide insights.
    Returns a dictionary with analysis results.
    """
    if not expenses:
        return {
            "error": "No expenses found",
            "total_spent": 0,
            "total_income": 0,
            "balance": 0,
            "categories": {},
            "percentages": {},
            "most_spent_category": {
                "name": None,
                "amount": 0,
                "percentage": 0
            },
            "suggestions": [],
            "monthly_stats": {
                "days_passed": 0,
                "days_remaining": 0,
                "monthly_spent": 0,
                "avg_daily_spending": 0,
                "remaining_budget": 0,
                "max_daily_spending": 0,
                "projected_monthly_spending": 0,
                "projected_end_balance": 0
            }
        }
    
    # Calculate totals
    total_income = 0
    total_expense = 0
    category_totals = defaultdict(float)
    category_counts = defaultdict(int)
    
    # Get current month
    now = datetime.now()
    current_month_start = datetime(now.year, now.month, 1)
    current_month_expenses = []
    
    for expense in expenses:
        amount = float(expense.get("amount", 0))
        category = expense.get("category", "other")
        date_str = expense.get("date", "")
        
        # Parse date
        try:
            expense_date = datetime.strptime(date_str, "%Y-%m-%d")
            if expense_date >= current_month_start:
                current_month_expenses.append(expense)
        except:
            pass
        
        if amount >= 0:
            total_income += amount
        else:
            total_expense += abs(amount)
            category_totals[category] += abs(amount)
            category_counts[category] += 1
    
    total_spent = total_expense
    balance = total_income - total_expense
    
    # Calculate percentages
    percentages = {}
    if total_spent > 0:
        for category, amount in category_totals.items():
            percentages[category] = (amount / total_spent) * 100
    
    # Find most spent category
    most_spent_category_name = None
    most_spent_amount = 0
    if category_totals:
        most_spent_category = max(category_totals.items(), key=lambda x: x[1])
        if most_spent_category:
            most_spent_category_name = most_spent_category[0]
            most_spent_amount = most_spent_category[1]
    
    # Calculate monthly spending rate
    try:
        # Get last day of current month
        if now.month == 12:
            next_month = datetime(now.year + 1, 1, 1)
        else:
            next_month = datetime(now.year, now.month + 1, 1)
        days_in_month = (next_month - timedelta(days=1)).day
    except:
        days_in_month = 30  # Fallback
    
    days_passed = now.day
    days_remaining = max(0, days_in_month - days_passed)
    
    # Calculate average daily spending this month
    monthly_spent = sum(abs(float(e.get("amount", 0))) for e in current_month_expenses if float(e.get("amount", 0)) < 0)
    avg_daily_spending = monthly_spent / days_passed if days_passed > 0 else 0
    
    # Project end of month spending
    projected_monthly_spending = avg_daily_spending * days_in_month
    projected_remaining_spending = avg_daily_spending * days_remaining
    
    # Calculate remaining budget (assuming income is monthly)
    # Get monthly income from current month
    monthly_income = sum(float(e.get("amount", 0)) for e in current_month_expenses if float(e.get("amount", 0)) >= 0)
    if monthly_income == 0:
        # If no income this month, use total income as fallback
        monthly_income = total_income
    
    remaining_budget = monthly_income - monthly_spent
    max_daily_spending = remaining_budget / days_remaining if days_remaining > 0 else 0
    
    # Projected end balance
    projected_end_balance = monthly_income - projected_monthly_spending
    
    # Generate suggestions
    suggestions = []
    
    # Suggest category to reduce spending
    if category_totals:
        # Find categories that are taking up too much percentage
        high_spending_categories = [(cat, amt, pct) for cat, amt, pct in 
                                   [(cat, category_totals[cat], percentages.get(cat, 0)) 
                                    for cat in category_totals.keys()]
                                   if pct > 30]  # More than 30% of spending
        
        if high_spending_categories:
            high_spending_categories.sort(key=lambda x: x[2], reverse=True)
            top_category = high_spending_categories[0]
            suggestions.append({
                "type": "reduce_spending",
                "category": top_category[0],
                "percentage": round(top_category[2], 1),
                "message": f"Consider reducing spending on {top_category[0].capitalize()} (currently {round(top_category[2], 1)}% of total expenses)"
            })
    
    # Budget warnings
    if remaining_budget < 0:
        suggestions.append({
            "type": "over_budget",
            "message": f"⚠️ You've exceeded your monthly budget by {abs(remaining_budget):.2f} ฿"
        })
    elif remaining_budget < (monthly_income * 0.1):
        suggestions.append({
            "type": "low_budget",
            "message": f"⚠️ You have only {remaining_budget:.2f} ฿ left this month ({round((remaining_budget/monthly_income)*100, 1)}% of income)"
        })
    
    # Spending rate warning
    if projected_end_balance < 0:
        suggestions.append({
            "type": "projected_negative",
            "message": f"⚠️ At current spending rate, you'll have a deficit of {abs(projected_end_balance):.2f} ฿ by month end"
        })
    
    # Use pandas for enhanced analysis
    df = None
    pandas_analysis = {}
    
    try:
        # Convert expenses to DataFrame
        df = pd.DataFrame(expenses)
        
        # Convert date column
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['datetime'] = pd.to_datetime(df.get('datetime', df['date']), errors='coerce')
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        # Remove rows with invalid dates or amounts
        df = df.dropna(subset=['date', 'amount'])
        
        if len(df) > 0:
            # Use pandas GROUPBY for category analysis
            expenses_df = df[df['amount'] < 0].copy()
            expenses_df['amount'] = expenses_df['amount'].abs()
            
            # GROUPBY category - sum, mean, count
            category_grouped = expenses_df.groupby('category')
            pandas_analysis['category_totals'] = category_grouped['amount'].sum().to_dict()
            pandas_analysis['category_avg'] = category_grouped['amount'].mean().to_dict()
            pandas_analysis['category_counts'] = category_grouped.size().to_dict()
            
            # GROUPBY month
            df['month'] = df['date'].dt.to_period('M')
            monthly_grouped = expenses_df.groupby(expenses_df['date'].dt.to_period('M'))
            pandas_analysis['monthly_totals'] = {str(k): v for k, v in monthly_grouped['amount'].sum().to_dict().items()}
            pandas_analysis['monthly_avg'] = {str(k): v for k, v in monthly_grouped['amount'].mean().to_dict().items()}
            
            # GROUPBY day of week
            df['day_of_week'] = df['date'].dt.day_name()
            weekday_grouped = expenses_df.groupby(expenses_df['date'].dt.day_name())
            pandas_analysis['weekday_avg'] = weekday_grouped['amount'].mean().to_dict()
            
            # GROUPBY category and month (multi-level)
            category_monthly = expenses_df.groupby(['category', expenses_df['date'].dt.to_period('M')])['amount'].sum()
            pandas_analysis['category_monthly'] = {f"{cat}_{str(month)}": amt for (cat, month), amt in category_monthly.to_dict().items()}
            
            # Calculate trends using linear regression
            if len(monthly_grouped) >= 2:
                monthly_data = monthly_grouped['amount'].sum().sort_index()
                X = np.array(range(len(monthly_data))).reshape(-1, 1)
                y = monthly_data.values
                
                model = LinearRegression()
                model.fit(X, y)
                
                # Predict next month
                next_month_pred = model.predict([[len(monthly_data)]])[0]
                pandas_analysis['predicted_next_month'] = max(0, round(next_month_pred, 2))
                pandas_analysis['spending_trend'] = "increasing" if model.coef_[0] > 0 else "decreasing"
                pandas_analysis['trend_slope'] = round(model.coef_[0], 2)
            
            # Rolling averages
            expenses_sorted = expenses_df.sort_values('date')
            expenses_sorted['7day_rolling'] = expenses_sorted['amount'].rolling(window=7, min_periods=1).mean()
            expenses_sorted['30day_rolling'] = expenses_sorted['amount'].rolling(window=30, min_periods=1).mean()
            pandas_analysis['current_7day_avg'] = round(expenses_sorted['7day_rolling'].iloc[-1] if len(expenses_sorted) > 0 else 0, 2)
            pandas_analysis['current_30day_avg'] = round(expenses_sorted['30day_rolling'].iloc[-1] if len(expenses_sorted) > 0 else 0, 2)
            
            # Category growth analysis
            recent_30_days = expenses_df[expenses_df['date'] >= (expenses_df['date'].max() - pd.Timedelta(days=30))]
            older_30_days = expenses_df[(expenses_df['date'] < (expenses_df['date'].max() - pd.Timedelta(days=30))) & 
                                        (expenses_df['date'] >= (expenses_df['date'].max() - pd.Timedelta(days=60)))]
            
            if len(older_30_days) > 0:
                recent_by_cat = recent_30_days.groupby('category')['amount'].mean()
                older_by_cat = older_30_days.groupby('category')['amount'].mean()
                
                category_growth = {}
                for cat in recent_by_cat.index:
                    if cat in older_by_cat.index and older_by_cat[cat] > 0:
                        growth = ((recent_by_cat[cat] - older_by_cat[cat]) / older_by_cat[cat]) * 100
                        category_growth[cat] = round(growth, 2)
                
                pandas_analysis['category_growth'] = category_growth
                if category_growth:
                    fastest_growing = max(category_growth.items(), key=lambda x: x[1])
                    pandas_analysis['fastest_growing_category'] = {
                        'name': fastest_growing[0],
                        'growth_percent': fastest_growing[1]
                    }
    except Exception as e:
        print(f"Error in pandas analysis: {e}")
        import traceback
        traceback.print_exc()
        pandas_analysis = {}
    
    return {
        "total_spent": round(total_spent, 2),
        "total_income": round(total_income, 2),
        "balance": round(balance, 2),
        "categories": {k: round(v, 2) for k, v in category_totals.items()},
        "percentages": {k: round(v, 1) for k, v in percentages.items()},
        "most_spent_category": {
            "name": most_spent_category_name,
            "amount": round(most_spent_amount, 2),
            "percentage": round(percentages.get(most_spent_category_name, 0), 1) if most_spent_category_name else 0
        },
        "suggestions": suggestions,
        "monthly_stats": {
            "days_passed": days_passed,
            "days_remaining": days_remaining,
            "monthly_spent": round(monthly_spent, 2),
            "avg_daily_spending": round(avg_daily_spending, 2),
            "remaining_budget": round(remaining_budget, 2),
            "max_daily_spending": round(max_daily_spending, 2),
            "projected_monthly_spending": round(projected_monthly_spending, 2),
            "projected_end_balance": round(projected_end_balance, 2)
        },
        "pandas_analysis": pandas_analysis
    }

def get_average_spending(expenses, category=None, time_period=None):
    """Get average spending using pandas mean operations"""
    try:
        df = pd.DataFrame(expenses)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        df = df.dropna(subset=['date', 'amount'])
        
        expenses_df = df[df['amount'] < 0].copy()
        expenses_df['amount'] = expenses_df['amount'].abs()
        
        if category:
            expenses_df = expenses_df[expenses_df['category'] == category]
        
        if time_period == "this_month":
            now = datetime.now()
            expenses_df = expenses_df[expenses_df['date'].dt.month == now.month]
            expenses_df = expenses_df[expenses_df['date'].dt.year == now.year]
        elif time_period == "last_month":
            now = datetime.now()
            last_month = now.month - 1 if now.month > 1 else 12
            last_year = now.year if now.month > 1 else now.year - 1
            expenses_df = expenses_df[expenses_df['date'].dt.month == last_month]
            expenses_df = expenses_df[expenses_df['date'].dt.year == last_year]
        
        if len(expenses_df) == 0:
            return None
        
        avg_per_transaction = expenses_df['amount'].mean()
        avg_daily = expenses_df.groupby(expenses_df['date'].dt.date)['amount'].sum().mean()
        
        return {
            'avg_per_transaction': round(avg_per_transaction, 2),
            'avg_daily': round(avg_daily, 2),
            'total_transactions': len(expenses_df)
        }
    except Exception as e:
        print(f"Error in get_average_spending: {e}")
        return None

def get_spending_trends(expenses):
    """Get spending trends using linear regression"""
    try:
        df = pd.DataFrame(expenses)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        df = df.dropna(subset=['date', 'amount'])
        
        expenses_df = df[df['amount'] < 0].copy()
        expenses_df['amount'] = expenses_df['amount'].abs()
        
        monthly_grouped = expenses_df.groupby(expenses_df['date'].dt.to_period('M'))
        monthly_totals = monthly_grouped['amount'].sum().sort_index()
        
        if len(monthly_totals) < 2:
            return None
        
        X = np.array(range(len(monthly_totals))).reshape(-1, 1)
        y = monthly_totals.values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict next month
        next_month_pred = model.predict([[len(monthly_totals)]])[0]
        
        return {
            'trend': "increasing" if model.coef_[0] > 0 else "decreasing",
            'slope': round(model.coef_[0], 2),
            'predicted_next_month': max(0, round(next_month_pred, 2)),
            'current_month': round(monthly_totals.iloc[-1], 2) if len(monthly_totals) > 0 else 0
        }
    except Exception as e:
        print(f"Error in get_spending_trends: {e}")
        return None

def get_weekday_analysis(expenses):
    """Get spending by day of week using pandas GROUPBY"""
    try:
        df = pd.DataFrame(expenses)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        df = df.dropna(subset=['date', 'amount'])
        
        expenses_df = df[df['amount'] < 0].copy()
        
        if len(expenses_df) == 0:
            return None
        
        expenses_df['amount'] = expenses_df['amount'].abs()
        
        weekday_grouped = expenses_df.groupby(expenses_df['date'].dt.day_name())
        weekday_avg = weekday_grouped['amount'].mean()
        weekday_totals = weekday_grouped['amount'].sum()
        
        if len(weekday_avg) == 0:
            return None
        
        # Order by day of week
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_avg = weekday_avg.reindex([d for d in day_order if d in weekday_avg.index])
        weekday_totals = weekday_totals.reindex([d for d in day_order if d in weekday_totals.index])
        
        return {
            'weekday_avg': {k: round(v, 2) for k, v in weekday_avg.to_dict().items()},
            'weekday_totals': {k: round(v, 2) for k, v in weekday_totals.to_dict().items()},
            'highest_day': weekday_avg.idxmax() if len(weekday_avg) > 0 else None,
            'lowest_day': weekday_avg.idxmin() if len(weekday_avg) > 0 else None
        }
    except Exception as e:
        print(f"Error in get_weekday_analysis: {e}")
        return None

def get_category_growth(expenses):
    """Get category growth analysis using pandas GROUPBY"""
    try:
        df = pd.DataFrame(expenses)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        df = df.dropna(subset=['date', 'amount'])
        
        expenses_df = df[df['amount'] < 0].copy()
        expenses_df['amount'] = expenses_df['amount'].abs()
        
        recent_30_days = expenses_df[expenses_df['date'] >= (expenses_df['date'].max() - pd.Timedelta(days=30))]
        older_30_days = expenses_df[(expenses_df['date'] < (expenses_df['date'].max() - pd.Timedelta(days=30))) & 
                                    (expenses_df['date'] >= (expenses_df['date'].max() - pd.Timedelta(days=60)))]
        
        if len(older_30_days) == 0:
            return None
        
        recent_by_cat = recent_30_days.groupby('category')['amount'].mean()
        older_by_cat = older_30_days.groupby('category')['amount'].mean()
        
        category_growth = {}
        for cat in recent_by_cat.index:
            if cat in older_by_cat.index and older_by_cat[cat] > 0:
                growth = ((recent_by_cat[cat] - older_by_cat[cat]) / older_by_cat[cat]) * 100
                category_growth[cat] = round(growth, 2)
        
        if not category_growth:
            return None
        
        fastest_growing = max(category_growth.items(), key=lambda x: x[1])
        fastest_declining = min(category_growth.items(), key=lambda x: x[1])
        
        return {
            'category_growth': category_growth,
            'fastest_growing': {
                'category': fastest_growing[0],
                'growth_percent': fastest_growing[1]
            },
            'fastest_declining': {
                'category': fastest_declining[0],
                'decline_percent': fastest_declining[1]
            }
        }
    except Exception as e:
        print(f"Error in get_category_growth: {e}")
        return None

