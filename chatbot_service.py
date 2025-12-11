import re
import random
from datetime import datetime, timedelta

# Rule-based chatbot service for natural language processing

def get_conversational_response(text, uid=None):
    """
    Handle conversational inputs like greetings, questions, and general chat.
    Returns a response action if the input is conversational, None otherwise.
    Uses rule-based responses.
    """
    text_lower = text.lower().strip()
    
    # Greetings (expanded)
    greetings = {
        "hi": ["Hi there! 👋 How can I help you with your expenses today?", "Hello! What would you like to do?", "Hi! Ready to track your finances?"],
        "hello": ["Hello! 👋 How can I assist you today?", "Hi there! What can I do for you?", "Hello! Let's manage your expenses together!"],
        "hey": ["Hey! 👋 What's up? Need help with expenses?", "Hey there! How can I help?", "Hey! Ready to track your spending?"],
        "yo": ["Yo! 👋 What's up? Need help with your expenses?", "Yo! How can I help you today?", "Yo! Ready to track your finances?"],
        "good morning": ["Good morning! ☀️ How can I help you start your day?", "Morning! What would you like to do today?", "Good morning! Ready to manage your finances?"],
        "good afternoon": ["Good afternoon! ☀️ How can I assist you?", "Afternoon! What can I do for you?", "Good afternoon! Let's work on your expenses!"],
        "good evening": ["Good evening! 🌙 How can I help you?", "Evening! What would you like to do?", "Good evening! Ready to track your expenses?"],
        "greetings": ["Greetings! How can I assist you today?", "Hello! What can I do for you?", "Hi! Let's manage your expenses together!"],
        "morning": ["Morning! ☀️ How can I help you today?", "Good morning! What would you like to do?", "Morning! Ready to track your expenses?"],
        "afternoon": ["Afternoon! ☀️ How can I assist you?", "Good afternoon! What can I do for you?", "Afternoon! Let's manage your finances!"],
        "evening": ["Evening! 🌙 How can I help you?", "Good evening! What would you like to do?", "Evening! Ready to track your expenses?"],
    }
    
    # Check for exact greeting matches
    for greeting, responses in greetings.items():
        if text_lower == greeting or text_lower.startswith(greeting + " "):
            return {
                "action": "conversation",
                "message": random.choice(responses)
            }
    
    # Guide command - show detailed help
    if text_lower == "guide" or text_lower == "help":
        guide_message = """<strong>💰 ADD EXPENSES (Keywords: bought, spent, paid, cost)</strong><br><br>
• "bought lunch 60 baht" → Adds food expense<br>
• "spent 200 baht on transport" → Adds transport expense<br>
• "paid 500 baht for shopping yesterday" → Adds shopping expense with date<br>
• "coffee 50 baht" → Quick expense entry<br>
• Categories: food, transport, shopping, entertainment, bills, health, education, other<br><br>

<strong>💵 ADD INCOME (Keywords: earned, got, received, salary, bonus)</strong><br><br>
• "earned 15000 baht salary" → Adds income<br>
• "got 5000 baht bonus" → Adds bonus income<br>
• "received 2000 baht" → Adds income<br><br>

<strong>📊 GET SUMMARY & ANALYSIS (Keywords: summary, analyze, balance, total, spending)</strong><br><br>
• "show me summary" → Full expense analysis<br>
• "analyze my expenses" → Detailed spending analysis<br>
• "what's my balance?" → Shows income, expenses, and balance<br>
• "how much did I spend this month?" → Monthly spending<br>
• "how much did I spend today?" → Today's spending<br>
• "how much did I spend yesterday?" → Yesterday's spending<br>
• "total spending" → All-time spending<br>
• "show me my income" → Total income<br><br>

<strong>🍔 CATEGORY SPENDING (Keywords: how much + category name)</strong><br><br>
• "how much did I spend on food?" → Food category total<br>
• "what did I spend on transport?" → Transport category total<br>
• "food spending this month" → Monthly food expenses<br>
• "shopping expenses" → Shopping category total<br>
• Works with: food, transport, shopping, entertainment, bills, health, education<br><br>

<strong>📈 ADVANCED ANALYSIS (Keywords: average, trend, weekday, category growth, predict, forecast)</strong><br><br>
• "what's my average spending?" → Average daily/monthly spending<br>
• "show me spending trends" → Spending trend analysis<br>
• "predict my spending" → Predicts next month's spending<br>
• "forecast my expenses" → Forecasts future expenses<br>
• "what will my spending be next month?" → Next month prediction<br>
• "weekday analysis" → Spending by day of week<br>
• "category growth" → Which categories are growing<br>
• "fastest growing category" → Category growth analysis<br><br>

<strong>🏷️ ADD CUSTOM CATEGORIES (Keywords: add + category name + category)</strong><br><br>
• "add shopping category" → Creates new category<br>
• "add travel category" → Creates travel category<br>
• "add gym category" → Creates gym category"""
        return {
            "action": "conversation",
            "message": guide_message
        }
    
    # Questions about capabilities (expanded patterns)
    capability_patterns = [
        (r"what can you do|what can i do|how can you help|what do you do|what are you|what's your purpose|what is your purpose", 
         ["I can help you track expenses and income! You can:\n• Add expenses like 'bought lunch 60 baht'\n• Add income like 'got salary 15000'\n• Ask for analysis like 'show me summary' or 'analyze my spending'\n• Ask about category spending like 'how much did I spend on food'\n• Add custom categories like 'add shopping category'\n\nJust type naturally and I'll understand!"],
        ),
        (r"how does this work|how do i use|how to use|instructions|help me|can you help|how to|tutorial",
         ["I'm here to help! Here's how to use me:\n\n📝 **Add Expenses**: Just type naturally like 'bought coffee 50 baht' or 'lunch 80 baht yesterday'\n\n💰 **Add Income**: Say things like 'got salary 15000' or 'received bonus 5000'\n\n📊 **Get Analysis**: Ask 'show me summary' or 'analyze my expenses' to see your spending patterns\n\n💵 **Category Spending**: Ask 'how much did I spend on food' or 'what did I spend on transport'\n\n🏷️ **Add Categories**: Type 'add [category name] category' to create custom categories\n\nTry it out!"],
        ),
        (r"who are you|what are you|tell me about yourself|introduce yourself|what is your name",
         ["I'm PIGGY's smart expense assistant! 🐷 I help you track your income and expenses by understanding natural language. Just tell me what you spent or earned, and I'll organize it for you. I can also analyze your spending patterns, answer questions about your expenses, and give you insights!"],
        ),
    ]
    
    for pattern, responses in capability_patterns:
        if re.search(pattern, text_lower):
            return {
                "action": "conversation",
                "message": random.choice(responses)
            }
    
    # Thank you responses
    if re.search(r"thank|thanks|thx|appreciate", text_lower):
        responses = [
            "You're welcome! 😊 Is there anything else I can help you with?",
            "Happy to help! Let me know if you need anything else!",
            "You're welcome! Feel free to ask me anything about your expenses!",
            "Anytime! What else can I do for you?",
        ]
        return {
            "action": "conversation",
            "message": random.choice(responses)
        }
    
    # Goodbye responses
    if re.search(r"bye|goodbye|see you|farewell|later", text_lower):
        responses = [
            "Goodbye! 👋 Take care and keep tracking your expenses!",
            "See you later! Don't forget to log your expenses!",
            "Bye! Have a great day! 🐷",
            "Goodbye! Come back anytime you need help with your finances!",
        ]
        return {
            "action": "conversation",
            "message": random.choice(responses)
        }
    
    # How are you / How's it going
    if re.search(r"how are you|how's it going|how is it going|how do you feel", text_lower):
        responses = [
            "I'm doing great! Ready to help you manage your expenses! How can I assist you today?",
            "I'm fantastic! Always happy to help with your finances. What would you like to do?",
            "I'm doing well, thanks for asking! What can I help you with today?",
        ]
        return {
            "action": "conversation",
            "message": random.choice(responses)
        }
    
    # Compliments
    if re.search(r"good job|well done|nice|awesome|great|excellent|amazing|love you", text_lower):
        responses = [
            "Aww, thank you! 😊 I'm here to make expense tracking easy for you!",
            "Thanks! I'm glad I can help! What else can I do?",
            "You're too kind! 😊 Let me know if you need anything else!",
        ]
        return {
            "action": "conversation",
            "message": random.choice(responses)
        }
    
    # Confusion / Don't understand
    if re.search(r"what|huh|i don't understand|confused|what does that mean|explain", text_lower) and not re.search(r"what can|what do|what are", text_lower):
        responses = [
            "I'm here to help! You can add expenses, add income, ask for analysis, or add categories. Try saying something like 'bought lunch 60 baht' or 'show me summary'!",
            "No worries! I can help you track expenses and income. Just type naturally like 'got salary 15000' or 'bought coffee 50 baht'. I'll understand!",
            "Let me help! You can:\n• Add expenses: 'bought lunch 60 baht'\n• Add income: 'got salary 15000'\n• Get analysis: 'show me summary'\n• Add categories: 'add shopping category'",
        ]
        return {
            "action": "conversation",
            "message": random.choice(responses)
        }
    
    # Examples / Show me how
    if re.search(r"example|show me|demonstrate|how do i add|how to add", text_lower):
        responses = [
            "Sure! Here are some examples:\n\n💰 **Add Expense**: 'bought lunch 60 baht yesterday'\n💰 **Add Income**: 'got salary 15000'\n📊 **Get Summary**: 'show me summary' or 'analyze my expenses'\n🏷️ **Add Category**: 'add shopping category'\n\nJust type naturally and I'll understand!",
            "Here are examples of what you can say:\n\n• 'bought coffee 50 baht' - adds an expense\n• 'got salary 20000' - adds income\n• 'show me summary' - analyzes your spending\n• 'add travel category' - creates a new category\n\nTry one!",
        ]
        return {
            "action": "conversation",
            "message": random.choice(responses)
        }
    
    # Status / How am I doing
    if re.search(r"how am i doing|how's my spending|am i doing well|my status", text_lower):
        return {
            "action": "analyze",
            "query": text
        }
    
    # General positive responses
    if re.search(r"ok|okay|sure|alright|fine|yes|yeah|yep", text_lower) and len(text_lower.split()) <= 3:
        responses = [
            "Great! What would you like to do?",
            "Awesome! How can I help you?",
            "Perfect! What's next?",
        ]
        return {
            "action": "conversation",
            "message": random.choice(responses)
        }
    
    # Questions about features
    if re.search(r"can i|is it possible|do you support|does this support", text_lower):
        responses = [
            "Yes! I can help you add expenses, add income, analyze your spending, and create custom categories. Just type naturally and I'll understand!",
            "Absolutely! I support adding expenses, income, spending analysis, and custom categories. What would you like to try?",
        ]
        return {
            "action": "conversation",
            "message": random.choice(responses)
        }
    
    # Check for category spending queries FIRST (before total queries)
    # This ensures "how much did I spend on food" goes to category handler, not total handler
    category_query_response = handle_category_spending_query(text, uid)
    if category_query_response:
        return category_query_response
    
    # Check for total spending/balance queries (only if not a category query)
    total_query_response = handle_total_spending_query(text, uid)
    if total_query_response:
        return total_query_response
    
    # Return None if no conversational match found
    return None

def handle_total_spending_query(text, uid=None):
    """
    Handle queries about total spending, balance, income, etc.
    Examples: "how much did I spend", "what's my balance", "total expenses"
    """
    if not uid:
        return None
    
    text_lower = text.lower().strip()
    
    # Check if this is a category-specific query - if so, don't handle it here
    # Look for patterns like "spend on food", "spending on transport", etc.
    if re.search(r'(?:spend|spent|spending|expense|expenses)\s+(?:on|for)\s+', text_lower):
        # This looks like a category query, let handle_category_spending_query handle it
        return None
    
    # Patterns for total spending/balance queries
    total_patterns = [
        r'how much (?:did|do|have) (?:i|you|we) (?:spend|spent|spending) (?:in total|total|all|altogether|overall)?$',
        r'how much (?:did|do|have) (?:i|you|we) (?:spend|spent|spending)$',
        r'what (?:is|was) (?:my|the) (?:total )?(?:spending|spent|expense|expenses)$',
        r'what (?:is|was) (?:my|the) (?:total )?(?:balance|remaining|left)',
        r'how much (?:is|was) (?:my|the) (?:total )?(?:income|earned|earnings)',
        r'show (?:me )?(?:my )?(?:total )?(?:spending|expenses|balance)$',
        r'total (?:spending|spent|expense|expenses)$',
        r'how much (?:do|did) (?:i|you|we) (?:have|had) (?:left|remaining)',
        r'what (?:is|was) (?:my|the) (?:current )?(?:balance|remaining)',
    ]
    
    is_total_query = False
    query_type = None  # 'spending', 'balance', 'income', 'all'
    
    for pattern in total_patterns:
        if re.search(pattern, text_lower):
            is_total_query = True
            if 'balance' in text_lower or 'remaining' in text_lower or 'left' in text_lower:
                query_type = 'balance'
            elif 'income' in text_lower or 'earned' in text_lower or 'earnings' in text_lower:
                query_type = 'income'
            elif 'spend' in text_lower or 'expense' in text_lower:
                query_type = 'spending'
            else:
                query_type = 'all'
            break
    
    # Also check for simple queries
    if not is_total_query:
        if re.search(r'\b(total|balance|spending|expenses|income)\b', text_lower) and len(text_lower.split()) <= 5:
            is_total_query = True
            if 'balance' in text_lower:
                query_type = 'balance'
            elif 'income' in text_lower:
                query_type = 'income'
            elif 'spend' in text_lower or 'expense' in text_lower:
                query_type = 'spending'
            else:
                query_type = 'all'
    
    if is_total_query:
        try:
            from database_service import get_expenses
            expenses = get_expenses(uid)
            
            # Determine time period
            now = datetime.now()
            time_period = None
            period_text = ""
            
            if re.search(r'\b(today|this day)\b', text_lower):
                time_period = "today"
                period_text = "today"
            elif re.search(r'\b(yesterday)\b', text_lower):
                time_period = "yesterday"
                period_text = "yesterday"
            elif re.search(r'\b(this month|current month)\b', text_lower):
                time_period = "this_month"
                period_text = "this month"
            elif re.search(r'\b(last month|previous month)\b', text_lower):
                time_period = "last_month"
                period_text = "last month"
            elif re.search(r'\b(this week|current week)\b', text_lower):
                time_period = "this_week"
                period_text = "this week"
            
            # Use rule-based response
            total_income = 0
            total_expense = 0
            
            today_start = None
            if time_period == "today":
                today_start = datetime(now.year, now.month, now.day)
            elif time_period == "yesterday":
                yesterday = now - timedelta(days=1)
                today_start = datetime(yesterday.year, yesterday.month, yesterday.day)
            elif time_period == "this_month":
                today_start = datetime(now.year, now.month, 1)
            elif time_period == "last_month":
                if now.month == 1:
                    today_start = datetime(now.year - 1, 12, 1)
                else:
                    today_start = datetime(now.year, now.month - 1, 1)
            elif time_period == "this_week":
                days_since_monday = now.weekday()
                today_start = now - timedelta(days=days_since_monday)
                today_start = datetime(today_start.year, today_start.month, today_start.day)
            
            for expense in expenses:
                amount = float(expense.get("amount", 0))
                
                # Check time period if specified
                if today_start:
                    try:
                        expense_date_str = expense.get("datetime") or expense.get("date", "")
                        if expense_date_str:
                            if " " in expense_date_str:
                                expense_date = datetime.strptime(expense_date_str.split()[0], "%Y-%m-%d")
                            else:
                                expense_date = datetime.strptime(expense_date_str, "%Y-%m-%d")
                            
                            if expense_date >= today_start:
                                if amount >= 0:
                                    total_income += amount
                                else:
                                    total_expense += abs(amount)
                    except:
                        # If date parsing fails, include it anyway
                        if amount >= 0:
                            total_income += amount
                        else:
                            total_expense += abs(amount)
                else:
                    # All time
                    if amount >= 0:
                        total_income += amount
                    else:
                        total_expense += abs(amount)
            
            balance = total_income - total_expense
            
            # Format response based on query type
            if query_type == 'balance':
                if time_period:
                    message = f"💰 Your balance {period_text} is {balance:,.2f} ฿ (Income: {total_income:,.2f} ฿, Expenses: {total_expense:,.2f} ฿)"
                else:
                    message = f"💰 Your total balance is {balance:,.2f} ฿ (Income: {total_income:,.2f} ฿, Expenses: {total_expense:,.2f} ฿)"
            elif query_type == 'income':
                if time_period:
                    message = f"💰 Your total income {period_text} is {total_income:,.2f} ฿"
                else:
                    message = f"💰 Your total income is {total_income:,.2f} ฿"
            elif query_type == 'spending':
                if time_period:
                    message = f"💰 You've spent {total_expense:,.2f} ฿ {period_text}"
                else:
                    message = f"💰 You've spent {total_expense:,.2f} ฿ in total"
            else:
                if time_period:
                    message = f"📊 Summary {period_text}:\n💰 Income: {total_income:,.2f} ฿\n💸 Expenses: {total_expense:,.2f} ฿\n💵 Balance: {balance:,.2f} ฿"
                else:
                    message = f"📊 Total Summary:\n💰 Income: {total_income:,.2f} ฿\n💸 Expenses: {total_expense:,.2f} ฿\n💵 Balance: {balance:,.2f} ฿"
            
            return {
                "action": "conversation",
                "message": message
            }
        except Exception as e:
            return None
    
    return None

def handle_pandas_analysis_query(text, uid=None):
    """
    Handle pandas/scikit-learn analysis queries:
    - Average spending queries
    - Trend/prediction queries
    - Day of week analysis
    - Category growth analysis
    """
    if not uid:
        return None
    
    text_lower = text.lower().strip()
    
    # Quick check if text contains analysis keywords before doing expensive operations
    analysis_keywords = ['average', 'mean', 'avg', 'trend', 'predict', 'forecast', 'weekday', 'day of week', 
                        'category growth', 'growing', 'increasing', 'decreasing']
    if not any(keyword in text_lower for keyword in analysis_keywords):
        return None
    
    try:
        from database_service import get_expenses
        from analysis_service import get_average_spending, get_spending_trends, get_weekday_analysis, get_category_growth
        expenses = get_expenses(uid)
        
        if not expenses or len(expenses) == 0:
            # Return helpful message instead of None
            if 'average' in text_lower or 'mean' in text_lower or 'avg' in text_lower:
                return {
                    "action": "conversation",
                    "message": "📊 No spending data available to calculate averages. Add some expenses first!"
                }
            return None
        
        # Average spending queries (expanded patterns)
        avg_patterns = [
            r'average (?:spending|spent|expense|expenses)',
            r'mean (?:spending|spent|expense|expenses)',
            r'avg (?:spending|spent|expense|expenses)',
            r'what (?:is|was) (?:my|the) (?:average|mean|avg) (?:spending|spent)',
            r'how much (?:do|did) (?:i|you) (?:spend|spent) (?:on average|per day|per transaction)',
            r'show (?:me )?(?:my )?(?:average|mean|avg) (?:spending|spent)',
            r'tell (?:me )?(?:my|about) (?:average|mean|avg) (?:spending|spent)',
            r'(?:average|mean|avg) (?:daily|per day|per transaction) (?:spending|spent)',
        ]
        
        for pattern in avg_patterns:
            if re.search(pattern, text_lower):
                # Check for category
                category = None
                category_keywords = {
                    "food": ["food", "lunch", "dinner", "breakfast", "meal", "restaurant"],
                    "transport": ["transport", "gas", "fuel", "taxi", "uber", "grab", "bus", "train"],
                    "shopping": ["shopping", "mall", "store", "buy", "purchase"],
                    "entertainment": ["entertainment", "movie", "cinema", "game", "concert"],
                    "bills": ["bill", "bills", "electricity", "water", "internet", "phone"],
                    "health": ["health", "hospital", "clinic", "doctor", "medicine"],
                    "education": ["education", "school", "book", "course", "tuition"],
                }
                
                for cat, keywords in category_keywords.items():
                    if any(kw in text_lower for kw in keywords):
                        category = cat
                        break
                
                # Check for time period
                time_period = None
                if re.search(r'\b(this month|current month)\b', text_lower):
                    time_period = "this_month"
                elif re.search(r'\b(last month|previous month)\b', text_lower):
                    time_period = "last_month"
                
                result = get_average_spending(expenses, category, time_period)
                if result:
                    if category:
                        cat_text = category.capitalize()
                        message = f"📊 Average {cat_text} Spending:\n"
                    else:
                        message = f"📊 Average Spending:\n"
                    
                    if time_period:
                        period_text = "this month" if time_period == "this_month" else "last month"
                        message += f"• Per transaction: {result['avg_per_transaction']:,.2f} ฿ ({period_text})\n"
                        message += f"• Per day: {result['avg_daily']:,.2f} ฿ ({period_text})\n"
                    else:
                        message += f"• Per transaction: {result['avg_per_transaction']:,.2f} ฿\n"
                        message += f"• Per day: {result['avg_daily']:,.2f} ฿\n"
                    message += f"• Total transactions: {result['total_transactions']}"
                    
                    return {
                        "action": "conversation",
                        "message": message
                    }
                else:
                    # No data available
                    if category:
                        cat_text = category.capitalize()
                        period_text = f" {time_period.replace('_', ' ')}" if time_period else ""
                        return {
                            "action": "conversation",
                            "message": f"📊 No {cat_text} spending data available{period_text} to calculate averages."
                        }
                    else:
                        return {
                            "action": "conversation",
                            "message": "📊 No spending data available to calculate averages."
                        }
        
        # Trend/prediction queries (expanded patterns)
        trend_patterns = [
            r'(?:spending|spent) (?:trend|trends|pattern|patterns)',
            r'(?:is|are) (?:my|the) (?:spending|expenses) (?:increasing|decreasing|going up|going down)',
            r'predict (?:my|the) (?:spending|expenses)',
            r'forecast (?:my|the) (?:spending|expenses)',
            r'what (?:will|is) (?:my|the) (?:spending|expenses) (?:be|next month)',
            r'how (?:is|are) (?:my|the) (?:spending|expenses) (?:trending|changing)',
            r'show (?:me )?(?:my|the) (?:spending|expense) (?:trend|trends)',
            r'tell (?:me )?(?:about|my) (?:spending|expense) (?:trend|trends)',
            r'(?:spending|expense) (?:prediction|forecast|projection)',
            r'will (?:i|my) (?:spend|spending) (?:more|less)',
        ]
        
        for pattern in trend_patterns:
            if re.search(pattern, text_lower):
                result = get_spending_trends(expenses)
                if result:
                    message = f"📈 Spending Trends:\n"
                    message += f"• Current trend: {result['trend'].capitalize()}\n"
                    message += f"• Monthly change: {abs(result['slope']):,.2f} ฿ per month\n"
                    message += f"• Current month: {result['current_month']:,.2f} ฿\n"
                    message += f"• Predicted next month: {result['predicted_next_month']:,.2f} ฿"
                    
                    return {
                        "action": "conversation",
                        "message": message
                    }
                else:
                    return {
                        "action": "conversation",
                        "message": "📈 Not enough data to analyze spending trends. Need at least 2 months of data."
                    }
        
        # Day of week analysis (expanded patterns)
        weekday_patterns = [
            r'(?:day of week|weekday|day) (?:spending|spent|expenses)',
            r'which (?:day|days) (?:do|did) (?:i|you) (?:spend|spent) (?:the most|most)',
            r'spending (?:by|on) (?:day|days)',
            r'weekday (?:analysis|pattern)',
            r'show (?:me )?(?:spending|expenses) (?:by|on) (?:day|days)',
            r'tell (?:me )?(?:which|what) (?:day|days) (?:i|you) (?:spend|spent)',
            r'(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday) (?:spending|spent)',
        ]
        
        for pattern in weekday_patterns:
            if re.search(pattern, text_lower):
                result = get_weekday_analysis(expenses)
                if result and result.get('weekday_avg') and len(result['weekday_avg']) > 0:
                    message = f"📅 Spending by Day of Week:\n\n"
                    for day, avg in result['weekday_avg'].items():
                        message += f"• {day}: {avg:,.2f} ฿ (avg)\n"
                    
                    if result.get('highest_day'):
                        message += f"\n💰 Highest spending day: {result['highest_day']}\n"
                    if result.get('lowest_day'):
                        message += f"💸 Lowest spending day: {result['lowest_day']}"
                    
                    return {
                        "action": "conversation",
                        "message": message
                    }
                else:
                    return {
                        "action": "conversation",
                        "message": "📅 No spending data available to analyze by day of week."
                    }
        
        # Category growth analysis (expanded patterns)
        growth_patterns = [
            r'(?:category|categories) (?:growth|growing|increasing|decreasing)',
            r'which (?:category|categories) (?:is|are) (?:growing|increasing|decreasing)',
            r'fastest (?:growing|increasing|declining|decreasing) (?:category|categories)',
            r'(?:spending|expenses) (?:growth|trend) (?:by|for) (?:category|categories)',
            r'show (?:me )?(?:category|categories) (?:growth|growing)',
            r'tell (?:me )?(?:which|what) (?:category|categories) (?:is|are) (?:growing|increasing)',
            r'(?:category|categories) (?:trend|trends)',
        ]
        
        for pattern in growth_patterns:
            if re.search(pattern, text_lower):
                result = get_category_growth(expenses)
                if result:
                    message = f"📊 Category Growth Analysis (Last 30 days vs Previous 30 days):\n\n"
                    
                    if result.get('fastest_growing'):
                        fg = result['fastest_growing']
                        message += f"📈 Fastest Growing: {fg['category'].capitalize()} (+{fg['growth_percent']:.1f}%)\n"
                    
                    if result.get('fastest_declining'):
                        fd = result['fastest_declining']
                        message += f"📉 Fastest Declining: {fd['category'].capitalize()} ({fd['decline_percent']:.1f}%)\n"
                    
                    if result.get('category_growth'):
                        message += f"\nAll Categories:\n"
                        for cat, growth in sorted(result['category_growth'].items(), key=lambda x: x[1], reverse=True):
                            symbol = "📈" if growth > 0 else "📉"
                            message += f"{symbol} {cat.capitalize()}: {growth:+.1f}%\n"
                    
                    return {
                        "action": "conversation",
                        "message": message
                    }
                else:
                    return {
                        "action": "conversation",
                        "message": "📊 Not enough historical data to analyze category growth. Need at least 60 days of data."
                    }
        
    except Exception as e:
        print(f"Error in handle_pandas_analysis_query: {e}")
        import traceback
        traceback.print_exc()
        # Return a helpful error message instead of None
        return {
            "action": "conversation",
            "message": f"Sorry, I encountered an error processing your analysis query. Please try again or ask a different question."
        }
    
    return None


def handle_category_spending_query(text, uid=None):
    """
    Handle queries about spending in specific categories.
    Examples: "how much did I spend on food", "what did I spend on transport"
    Returns a response action if it's a category query, None otherwise.
    Uses rule-based pattern matching to process queries.
    """
    if not uid:
        return None
    
    text_lower = text.lower().strip()
    
    # Expanded category keywords with many variations
    category_keywords = {
        "food": ["food", "lunch", "dinner", "breakfast", "meal", "meals", "restaurant", "restaurants", 
                 "eat", "eating", "cafe", "coffee", "snack", "snacks", "groceries", "grocery", 
                 "takeout", "delivery", "pizza", "burger", "sushi", "thai food", "chinese food",
                 "fast food", "dining", "canteen", "buffet", "catering"],
        "transport": ["transport", "transportation", "gas", "fuel", "petrol", "diesel", "taxi", "taxis",
                     "uber", "grab", "bus", "buses", "train", "trains", "bts", "mrt", "car", "cars",
                     "parking", "toll", "tolls", "metro", "subway", "flight", "flights", "airplane",
                     "airport", "taxi fare", "bus fare", "train fare", "commute", "commuting"],
        "shopping": ["shopping", "mall", "malls", "store", "stores", "buy", "bought", "purchase", "purchases",
                    "clothes", "clothing", "shirt", "shirts", "dress", "dresses", "shoes", "bag", "bags",
                    "electronics", "gadget", "gadgets", "phone", "laptop", "computer", "online shopping",
                    "amazon", "ebay", "market", "supermarket", "department store"],
        "entertainment": ["entertainment", "movie", "movies", "cinema", "cinemas", "theater", "theatre",
                        "game", "games", "gaming", "concert", "concerts", "music", "netflix", "spotify",
                        "youtube", "streaming", "subscription", "subscriptions", "hobby", "hobbies",
                        "sports", "gym", "fitness", "party", "parties", "event", "events"],
        "bills": ["bill", "bills", "electricity", "water", "internet", "wifi", "phone", "mobile", "cell",
                 "utility", "utilities", "rent", "rental", "mortgage", "insurance", "subscription fee",
                 "electric bill", "water bill", "phone bill", "internet bill", "utility bill"],
        "health": ["health", "hospital", "hospitals", "clinic", "clinics", "doctor", "doctors", "medicine",
                  "medicines", "pharmacy", "drug", "drugs", "medical", "treatment", "checkup", "check-up",
                  "dental", "dentist", "vitamin", "vitamins", "supplement", "supplements", "therapy"],
        "education": ["education", "school", "schools", "book", "books", "course", "courses", "tuition",
                     "study", "studying", "university", "college", "textbook", "textbooks", "stationery",
                     "stationary", "learning", "training", "workshop", "workshops", "seminar", "seminars"],
        "salary": ["salary", "wage", "wages", "paycheck", "pay", "payment", "income", "earnings"],
        "bonus": ["bonus", "bonuses", "reward", "rewards", "incentive", "incentives"],
        "other": ["other", "misc", "miscellaneous", "various", "others"]
    }
    
    # Patterns for category spending queries
    spending_patterns = [
        r'how much (?:did|do|have) (?:i|you|we) (?:spend|spent|spending) (?:on|for) (.+)',
        r'what (?:did|do|have) (?:i|you|we) (?:spend|spent|spending) (?:on|for) (.+)',
        r'how much (?:is|was) (?:my|the) (.+) (?:spending|spent|expense|expenses)',
        r'(.+) (?:spending|spent|expense|expenses|cost|costs)',
        r'show (?:me )?(?:my )?(?:spending|expenses) (?:on|for) (.+)',
        r'total (?:spending|spent|expense|expenses) (?:on|for) (.+)',
        r'(.+) (?:total|amount|sum)',
        r'how much (?:for|on) (.+)',
    ]
    
    # Try to match spending query patterns
    matched_category = None
    for pattern in spending_patterns:
        match = re.search(pattern, text_lower)
        if match:
            # Extract the category mention
            category_mention = match.group(1).strip()
            
            # Find which category it matches
            for category, keywords in category_keywords.items():
                if any(keyword in category_mention for keyword in keywords):
                    matched_category = category
                    break
            
            # Also check if category mention directly matches a category name
            if not matched_category:
                for category in category_keywords.keys():
                    if category in category_mention:
                        matched_category = category
                        break
            
            if matched_category:
                break
    
    # If no pattern matched, try direct category mentions with spending keywords
    if not matched_category:
        spending_keywords = ["spend", "spent", "spending", "expense", "expenses", "cost", "costs", "paid"]
        if any(keyword in text_lower for keyword in spending_keywords):
            # Check if any category keyword appears in the text
            for category, keywords in category_keywords.items():
                if any(keyword in text_lower for keyword in keywords):
                    matched_category = category
                    break
    
    # If we found a category, get the spending data
    if matched_category:
        try:
            from database_service import get_expenses
            expenses = get_expenses(uid)
            
            # Determine time period
            now = datetime.now()
            time_period = None
            period_text = ""
            
            if re.search(r'\b(today|this day)\b', text_lower):
                time_period = "today"
                period_text = "today"
            elif re.search(r'\b(yesterday)\b', text_lower):
                time_period = "yesterday"
                period_text = "yesterday"
            elif re.search(r'\b(this month|current month|this month)\b', text_lower):
                time_period = "this_month"
                period_text = "this month"
            elif re.search(r'\b(last month|previous month)\b', text_lower):
                time_period = "last_month"
                period_text = "last month"
            elif re.search(r'\b(this week|current week)\b', text_lower):
                time_period = "this_week"
                period_text = "this week"
            elif re.search(r'\b(last week|previous week)\b', text_lower):
                time_period = "last_week"
                period_text = "last week"
            
            # Use rule-based response
            category_spending = 0
            category_count = 0
            
            # Calculate spending for the category
            today_start = None
            if time_period == "today":
                today_start = datetime(now.year, now.month, now.day)
            elif time_period == "yesterday":
                yesterday = now - timedelta(days=1)
                today_start = datetime(yesterday.year, yesterday.month, yesterday.day)
            elif time_period == "this_month":
                today_start = datetime(now.year, now.month, 1)
            elif time_period == "last_month":
                if now.month == 1:
                    today_start = datetime(now.year - 1, 12, 1)
                else:
                    today_start = datetime(now.year, now.month - 1, 1)
            elif time_period == "this_week":
                days_since_monday = now.weekday()
                today_start = now - timedelta(days=days_since_monday)
                today_start = datetime(today_start.year, today_start.month, today_start.day)
            elif time_period == "last_week":
                days_since_monday = now.weekday()
                last_week_start = now - timedelta(days=days_since_monday + 7)
                today_start = datetime(last_week_start.year, last_week_start.month, last_week_start.day)
            
            for expense in expenses:
                amount = float(expense.get("amount", 0))
                category = expense.get("category", "other")
                
                # Only count expenses (negative amounts or expenses)
                if amount < 0 and category == matched_category:
                    # Check time period if specified
                    if today_start:
                        try:
                            expense_date_str = expense.get("datetime") or expense.get("date", "")
                            if expense_date_str:
                                if " " in expense_date_str:
                                    expense_date = datetime.strptime(expense_date_str.split()[0], "%Y-%m-%d")
                                else:
                                    expense_date = datetime.strptime(expense_date_str, "%Y-%m-%d")
                                
                                if expense_date >= today_start:
                                    category_spending += abs(amount)
                                    category_count += 1
                        except:
                            # If date parsing fails, include it anyway
                            category_spending += abs(amount)
                            category_count += 1
                    else:
                        # All time
                        category_spending += abs(amount)
                        category_count += 1
            
            # Format response
            category_name = matched_category.capitalize()
            if category_spending > 0:
                if time_period:
                    message = f"💰 You've spent {category_spending:,.2f} ฿ on {category_name} {period_text} ({category_count} transaction{'s' if category_count != 1 else ''})"
                else:
                    message = f"💰 You've spent {category_spending:,.2f} ฿ on {category_name} in total ({category_count} transaction{'s' if category_count != 1 else ''})"
            else:
                if time_period:
                    message = f"📊 You haven't spent anything on {category_name} {period_text} yet."
                else:
                    message = f"📊 You haven't spent anything on {category_name} yet."
            
            return {
                "action": "conversation",
                "message": message
            }
        except Exception as e:
            # If there's an error, return None to fall back to other handlers
            return None
    
    return None

def parse_natural_language(text, uid=None):
    """
    Parse natural language input and extract expense/income information.
    Returns JSON object with type, amount, category, date, and note.
    """
    text_lower = text.lower().strip()
    
    # Check for pandas/scikit-learn analysis queries FIRST (before conversational)
    # These are specific analysis queries that need to be handled before general conversation
    pandas_analysis_response = handle_pandas_analysis_query(text, uid)
    if pandas_analysis_response:
        return pandas_analysis_response
    
    # ALWAYS check for conversational responses
    # This ensures greetings and questions are handled properly
    conversation_response = get_conversational_response(text, uid)
    if conversation_response:
        return conversation_response
    
    # Check if input looks like a transaction (has numbers that could be amounts)
    looks_like_transaction = False
    numbers = re.findall(r'\d+(?:\.\d+)?', text)
    if numbers:
        # Check if any number could be an amount (reasonable range: 1 to 1,000,000)
        for num_str in numbers:
            try:
                num = float(num_str)
                if 1 <= num <= 1000000:  # Reasonable amount range
                    looks_like_transaction = True
                    break
            except:
                pass
    
    # Also check for transaction keywords (expanded)
    transaction_keywords = [
        "bought", "buy", "purchase", "purchased", "spent", "spend", "spending",
        "got", "get", "received", "receive", "paid", "pay", "payment", "paying",
        "cost", "costs", "costed", "lunch", "dinner", "breakfast", "food", "meal",
        "salary", "wage", "income", "earnings", "expense", "expenses", "transaction",
        "add", "record", "logged", "log", "enter", "input", "save", "saved"
    ]
    if any(keyword in text_lower for keyword in transaction_keywords):
        looks_like_transaction = True
    
    # Check for analysis/summary requests (expanded keywords)
    analysis_keywords = [
        "summary", "summarize", "summaries", "analyze", "analysis", "analyses", 
        "how much", "how many", "spent", "spending", "budget", "budgets", 
        "report", "reports", "statistics", "stats", "stat", "insight", "insights",
        "overview", "breakdown", "break down", "total", "totals", "balance",
        "financial", "finance", "expense report", "spending report", "summary report",
        "show me", "tell me", "what is", "what's", "give me", "display", "view"
    ]
    
    # Check if it's a general analysis request (not category-specific)
    is_general_analysis = any(keyword in text_lower for keyword in analysis_keywords)
    
    # Make sure it's not a category-specific query (those are handled in get_conversational_response)
    category_keywords_in_text = ["food", "transport", "shopping", "entertainment", "bills", 
                                 "health", "education", "salary", "bonus", "other"]
    is_category_specific = any(cat in text_lower for cat in category_keywords_in_text)
    
    if is_general_analysis and not is_category_specific:
        return {
            "action": "analyze",
            "query": text
        }
    
    # Initialize result
    result = {
        "type": "expense",
        "amount": 0,
        "category": "other",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),  # Include current time
        "note": text[:50]  # Limit note to 50 chars
    }
    
    # Check for add category command
    if "add" in text_lower and "category" in text_lower:
        # Extract category name
        match = re.search(r'add\s+(\w+)\s+category', text_lower)
        if match:
            category_name = match.group(1)
            return {
                "action": "add_category",
                "category": category_name.lower()
            }
        return {
            "action": "add_category",
            "category": None,
            "error": "Could not extract category name"
        }
    
    # Determine type (income or expense) - expanded keywords
    income_keywords = [
        "salary", "salaries", "wage", "wages", "got", "get", "received", "receive", 
        "earned", "earn", "earning", "income", "incomes", "bonus", "bonuses", 
        "paycheck", "paychecks", "paid", "payment received", "payments received",
        "revenue", "profit", "gains", "refund", "refunds", "return", "returns"
    ]
    expense_keywords = [
        "bought", "buy", "purchase", "purchased", "spent", "spend", "spending",
        "paid", "pay", "payment", "paying", "expense", "expenses", "cost", "costs",
        "gas", "fuel", "lunch", "dinner", "breakfast", "food", "meal", "meals",
        "bill", "bills", "fee", "fees", "charge", "charges", "debit", "debits"
    ]
    
    is_income = any(keyword in text_lower for keyword in income_keywords)
    is_expense = any(keyword in text_lower for keyword in expense_keywords)
    
    # If both or neither, check for specific patterns
    if not is_income and not is_expense:
        # Check for "got" or "received" patterns
        if re.search(r'\b(got|received|earned)\b', text_lower):
            is_income = True
        else:
            is_expense = True  # Default to expense
    
    result["type"] = "income" if is_income else "expense"
    
    # Extract amount
    # Look for numbers (including Thai baht symbol or "bath", "baht")
    amount_patterns = [
        r'(\d+(?:\.\d+)?)\s*(?:bath|baht|฿|บาท)',  # "60 baht" or "60 bath"
        r'(?:bath|baht|฿|บาท)\s*(\d+(?:\.\d+)?)',  # "baht 60"
    ]
    
    amount = None
    # First try patterns with baht/bath keywords (case insensitive)
    for pattern in amount_patterns:
        match = re.search(pattern, text_lower)
        if match:
            try:
                # Get the number from the match (could be group 1 or 2)
                amount_str = None
                if match.lastindex >= 1:
                    amount_str = match.group(1)
                if not amount_str and match.lastindex >= 2:
                    amount_str = match.group(2)
                
                if amount_str:
                    amount = float(amount_str)
                    if amount > 0:
                        break
            except (ValueError, IndexError):
                continue
    
    # If no amount found with baht keyword, look for standalone numbers
    if amount is None or amount <= 0:
        # Find all numbers in the text
        numbers = re.findall(r'\d+(?:\.\d+)?', text)
        if numbers:
            # Try each number, prefer larger numbers (likely to be amounts)
            potential_amounts = []
            for num_str in numbers:
                try:
                    num = float(num_str)
                    # Accept any positive number (even small ones like 5, 10, etc.)
                    if num > 0:
                        potential_amounts.append(num)
                except:
                    pass
    
            if potential_amounts:
                # Use the largest number (most likely to be the amount)
                # But if there's only one reasonable number, use it
                if len(potential_amounts) == 1:
                    amount = potential_amounts[0]
                else:
                    # Filter out very small numbers that might be dates/times (1-9)
                    large_amounts = [n for n in potential_amounts if n >= 10]
                    if large_amounts:
                        amount = max(large_amounts)
                    else:
                        # If all numbers are small, use the largest one
                        amount = max(potential_amounts)
    
    # Set amount in result
    if amount and amount > 0:
        result["amount"] = amount
    else:
        # If no valid amount found, set to 0 so frontend shows error
        result["amount"] = 0
    
    # Extract date and time
    today = datetime.now()
    date_found = False
    time_found = False
    
    # Extract time patterns (HH:MM, HH:MM:SS, or "at 3pm", "at 15:30", etc.)
    # Try hour-only with am/pm first (e.g., "3pm", "3 PM")
    hour_only_match = re.search(r'\b(\d{1,2})\s*(am|pm|AM|PM)\b', text_lower)
    if hour_only_match:
        try:
            hour = int(hour_only_match.group(1))
            am_pm = hour_only_match.group(2).lower()
            if am_pm == 'pm' and hour != 12:
                hour += 12
            elif am_pm == 'am' and hour == 12:
                hour = 0
            if 0 <= hour <= 23:
                result["time"] = f"{hour:02d}:00:00"
                time_found = True
        except:
            pass
    
    # Try time with minutes (HH:MM or HH:MM:SS)
    if not time_found:
        time_patterns = [
            r'\bat\s+(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(am|pm|AM|PM)?\b',  # at 3:30, at 15:30, at 3:30pm
            r'\b(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(am|pm|AM|PM)?\b',  # 3:30, 15:30, 3:30:45, 3:30pm
        ]
        
        for pattern in time_patterns:
            time_match = re.search(pattern, text_lower)
            if time_match:
                try:
                    hour = int(time_match.group(1))
                    minute = int(time_match.group(2))
                    second = int(time_match.group(3)) if time_match.lastindex >= 3 and time_match.group(3) else 0
                    
                    # Check for am/pm in the match
                    if time_match.lastindex >= 4 and time_match.group(4):
                        am_pm = time_match.group(4).lower()
                        if am_pm == 'pm' and hour != 12:
                            hour += 12
                        elif am_pm == 'am' and hour == 12:
                            hour = 0
                    
                    # Validate time
                    if 0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59:
                        result["time"] = f"{hour:02d}:{minute:02d}:{second:02d}"
                        time_found = True
                        break
                except:
                    continue
    
    # Check for relative dates
    if "yesterday" in text_lower:
        result["date"] = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        date_found = True
    elif "tomorrow" in text_lower:
        result["date"] = (today + timedelta(days=1)).strftime("%Y-%m-%d")
        date_found = True
    elif "today" in text_lower:
        result["date"] = today.strftime("%Y-%m-%d")
        date_found = True
    
    # Check for specific date patterns (YYYY-MM-DD, MM/DD/YYYY, etc.)
    if not date_found:
        date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', text)
        if date_match:
            result["date"] = date_match.group(0)
            date_found = True
        else:
            date_match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', text)
            if date_match:
                month, day, year = date_match.groups()
                result["date"] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                date_found = True
    
    # If no date found, use today (already set as default)
    # If no time found, use current time (already set as default)
    
    # Extract category (expanded keywords)
    category_keywords = {
        "food": ["food", "lunch", "dinner", "breakfast", "meal", "meals", "restaurant", "restaurants", 
                 "eat", "eating", "cafe", "coffee", "snack", "snacks", "groceries", "grocery", 
                 "takeout", "delivery", "pizza", "burger", "sushi", "thai food", "chinese food",
                 "fast food", "dining", "canteen", "buffet", "catering", "brunch", "supper"],
        "transport": ["transport", "transportation", "gas", "fuel", "petrol", "diesel", "taxi", "taxis",
                     "uber", "grab", "bus", "buses", "train", "trains", "bts", "mrt", "car", "cars",
                     "parking", "toll", "tolls", "metro", "subway", "flight", "flights", "airplane",
                     "airport", "taxi fare", "bus fare", "train fare", "commute", "commuting", "ride"],
        "shopping": ["shopping", "mall", "malls", "store", "stores", "buy", "bought", "purchase", "purchases",
                    "clothes", "clothing", "shirt", "shirts", "dress", "dresses", "shoes", "bag", "bags",
                    "electronics", "gadget", "gadgets", "phone", "laptop", "computer", "online shopping",
                    "amazon", "ebay", "market", "supermarket", "department store", "retail"],
        "entertainment": ["entertainment", "movie", "movies", "cinema", "cinemas", "theater", "theatre",
                        "game", "games", "gaming", "concert", "concerts", "music", "netflix", "spotify",
                        "youtube", "streaming", "subscription", "subscriptions", "hobby", "hobbies",
                        "sports", "gym", "fitness", "party", "parties", "event", "events", "show", "shows"],
        "bills": ["bill", "bills", "electricity", "water", "internet", "wifi", "phone", "mobile", "cell",
                 "utility", "utilities", "rent", "rental", "mortgage", "insurance", "subscription fee",
                 "electric bill", "water bill", "phone bill", "internet bill", "utility bill"],
        "health": ["health", "hospital", "hospitals", "clinic", "clinics", "doctor", "doctors", "medicine",
                  "medicines", "pharmacy", "drug", "drugs", "medical", "treatment", "checkup", "check-up",
                  "dental", "dentist", "vitamin", "vitamins", "supplement", "supplements", "therapy"],
        "education": ["education", "school", "schools", "book", "books", "course", "courses", "tuition",
                     "study", "studying", "university", "college", "textbook", "textbooks", "stationery",
                     "stationary", "learning", "training", "workshop", "workshops", "seminar", "seminars"],
        "salary": ["salary", "wage", "wages", "paycheck", "pay", "payment", "income", "earnings"],
        "bonus": ["bonus", "bonuses", "reward", "rewards", "incentive", "incentives"],
    }
    
    # Find matching category
    category_found = False
    for category, keywords in category_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            result["category"] = category
            category_found = True
            break
    
    # If no category found, try to infer from context
    if not category_found:
        if result["type"] == "income":
            result["category"] = "salary"  # Default income category
        else:
            result["category"] = "other"  # Default expense category
    
    # Extract note (simplified version of input)
    note = text.strip()
    # Remove amount and date from note if present
    note = re.sub(r'\d+(?:\.\d+)?\s*(?:bath|baht|฿|บาท)', '', note, flags=re.IGNORECASE)
    note = re.sub(r'\b(today|yesterday|tomorrow)\b', '', note, flags=re.IGNORECASE)
    note = re.sub(r'\s+', ' ', note).strip()
    if note:
        result["note"] = note[:50]
    
    # Ensure result has all required fields
    if not result.get("type"):
        result["type"] = "expense"
    if not result.get("amount"):
        result["amount"] = 0
    if not result.get("category"):
        result["category"] = "other"
    if not result.get("date"):
        result["date"] = datetime.now().strftime("%Y-%m-%d")
    if not result.get("time"):
        result["time"] = datetime.now().strftime("%H:%M:%S")
    
    return result

