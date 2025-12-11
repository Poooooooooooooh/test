import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, request, jsonify, render_template
from auth_service import register_user, login_user, verify_token
from database_service import add_expense, get_expenses, add_category, get_categories, delete_expense, search_transactions
from chatbot_service import parse_natural_language
from analysis_service import analyze_expenses

# Load environment variables
try:
    from dotenv import load_dotenv
    # Change to the directory where app.py is located
    app_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(app_dir)
    # Load .env from the current directory
    env_path = os.path.join(app_dir, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path, override=True)
        print(f"Loading .env from: {env_path}")
    else:
        print(f".env file not found at: {env_path}")
except ImportError:
    print("python-dotenv not installed. Environment variables must be set manually.")
except Exception as e:
    print(f"Error loading .env: {e}")
    import traceback
    traceback.print_exc()

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Error handler to ensure JSON responses
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400

@app.route("/", methods=["GET"])
def index():
    """Homepage"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PIGGY - Expense Tracking</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700;800&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Nunito', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #b7e4f4 0%, #3abeed 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                text-align: center;
                color: #333;
                background: white;
                padding: 60px 40px;
                border-radius: 25px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.15);
                border: 4px solid white;
                max-width: 600px;
            }
             .logo-container {
                 margin-bottom: 15px;
                 display: flex;
                 flex-direction: column;
                 align-items: center;
                 justify-content: center;
             }
             .logo-container img {
                 height: 169px;
                 width: auto;
                 max-width: 100%;
                 margin-bottom: 10px;
                 display: block;
                 margin-left: auto;
                 margin-right: auto;
                 object-fit: contain;
                 aspect-ratio: auto;
             }
             .brand-title {
                 display: flex;
                 flex-direction: column;
                 align-items: center;
                 line-height: 1.1;
                 margin-bottom: 20px;
             }
             .brand-line {
                 display: block;
                 color: #ffd1d1;
                 font-size: 2.5em;
                 font-weight: 800;
                 letter-spacing: 0.05em;
                 text-shadow: 
                     -3px -3px 0 white,
                     3px -3px 0 white,
                     -3px 3px 0 white,
                     3px 3px 0 white,
                     0 0 15px rgba(255, 255, 255, 0.8);
                 text-transform: uppercase;
             }
            .subtitle {
                font-size: 1.3em;
                color: #666;
                margin-bottom: 40px;
            }
            .buttons {
                margin-top: 40px;
                display: flex;
                gap: 20px;
                justify-content: center;
                flex-wrap: wrap;
            }
            .btn {
                display: inline-block;
                padding: 15px 40px;
                background: linear-gradient(to bottom, #ffd1d1 0%, #ff6767 100%);
                color: white;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                font-size: 1.2em;
                transition: all 0.3s;
                border: 3px solid white;
                box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            }
            .btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 15px rgba(0,0,0,0.2);
            }
            @media (max-width: 768px) {
                body {
                    padding: 10px;
                }
                .container {
                    padding: 30px 20px;
                    max-width: 100%;
                    border-radius: 20px;
                }
                .logo-container img {
                    height: auto;
                    max-height: 25vh; /* 25% of viewport height */
                    max-width: 80vw; /* 80% of viewport width */
                    width: auto;
                }
                .brand-line {
                    font-size: 1.8em;
                }
                .subtitle {
                    font-size: 1.1em;
                    margin-bottom: 30px;
                }
                .buttons {
                    flex-direction: column;
                    gap: 15px;
                    margin-top: 30px;
                }
                .btn {
                    width: 100%;
                    padding: 12px 30px;
                    font-size: 1.1em;
                }
            }
            @media (max-width: 480px) {
                .container {
                    padding: 25px 15px;
                }
                .logo-container img {
                    height: auto;
                    max-height: 20vh; /* 20% of viewport height for smaller screens */
                    max-width: 75vw; /* 75% of viewport width */
                    width: auto;
                }
                .brand-line {
                    font-size: 1.5em;
                }
                .subtitle {
                    font-size: 1em;
                }
            }
        </style>
    </head>
    <body>
         <div class="container">
             <div class="logo-container">
                 <img src="/static/logo.png" alt="PIGGY Logo" style="height: 169px; width: auto; max-width: 100%; margin-bottom: 10px; display: block; margin-left: auto; margin-right: auto;" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                 <h1 style="display: none; background: linear-gradient(to bottom, #ffd1d1 0%, #ff6767 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 3em; font-weight: 800; margin-bottom: 20px; letter-spacing: -0.02em;">PIGGY</h1>
             </div>
             <div class="brand-title">
                 <span class="brand-line">SMART EXPENSE</span>
                 <span class="brand-line">ANALYZER</span>
             </div>
            <div class="buttons">
                <a href="/login" class="btn">Login</a>
                <a href="/signup" class="btn">Sign Up</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.route("/signup", methods=["GET"])
def signup_page():
    """Signup Page"""
    return render_template("signup.html")

@app.route("/login", methods=["GET"])
def login_page():
    """Login Page"""
    return render_template("login.html")

@app.route("/dashboard", methods=["GET"])
def dashboard():
    """Dashboard Page"""
    return render_template("dashboard.html")

@app.route("/test", methods=["GET"])
def test():
    """Simple test endpoint to verify connectivity"""
    return jsonify({
        "status": "success",
        "message": "Flask app is running and accessible!",
        "server_ip": request.remote_addr,
        "host": request.host
    })


@app.route("/api", methods=["GET"])
def api_docs():
    """JSON API documentation"""
    return jsonify({
        "message": "Expense Tracking API",
        "version": "1.0",
        "endpoints": {
            "POST /register": "Register a new user",
            "POST /login": "Login with Firebase ID token",
            "POST /add_expense": "Add a new expense (requires Authorization header)",
            "GET /expenses": "Get all expenses for the authenticated user (requires Authorization header)",
            "GET /search_transactions": "Search transactions by query (requires Authorization header, query parameter: q)"
        },
        "usage": {
            "register": {
                "method": "POST",
                "url": "/register",
                "body": {
                    "email": "user@example.com",
                    "password": "password123"
                }
            },
            "login": {
                "method": "POST",
                "url": "/login",
                "body": {
                    "id_token": "firebase_id_token_here"
                }
            },
            "add_expense": {
                "method": "POST",
                "url": "/add_expense",
                "headers": {
                    "Authorization": "firebase_id_token",
                    "Content-Type": "application/json"
                },
                "body": {
                    "category": "food",
                    "amount": 100,
                    "date": "2024-01-15",
                    "description": "Lunch"
                }
            },
            "get_expenses": {
                "method": "GET",
                "url": "/expenses",
                "headers": {
                    "Authorization": "firebase_id_token"
                }
            },
            "search_transactions": {
                "method": "GET",
                "url": "/search_transactions?q=search_query",
                "headers": {
                    "Authorization": "firebase_id_token"
                },
                "query_parameters": {
                    "q": "Search query (searches in category, description, and amount)"
                }
            }
        }
    })

@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.json
        if not data or "email" not in data or "password" not in data:
            return jsonify({"success": False, "error": "Missing email or password"}), 400
        
        result = register_user(data["email"], data["password"])
        
        # Save user data to Firestore for login
        if result.get("success"):
            try:
                from firebase_config import db
                db.collection("users").document(result["uid"]).set({
                    "email": data["email"],
                    "uid": result["uid"]
                })
            except Exception as e:
                # If Firestore error, log but still return success because user was created
                print(f"Warning: Could not save user to Firestore: {e}")
                # Still return success because user was created in Firebase Auth
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "error": "Missing request data"}), 400
        
        # Support both email/password and id_token
        if "email" in data and "password" in data:
            try:
                # Find user from email in Firestore
                from firebase_config import db
                users_ref = db.collection("users")
                # Use where with positional arguments
                query = users_ref.where("email", "==", data["email"]).limit(1).stream()
                
                user_doc = None
                for doc in query:
                    user_doc = doc
                    break
                
                if user_doc:
                    # For demo - in production should verify password
                    return jsonify({
                        "success": True,
                        "uid": user_doc.id,
                        "token": user_doc.id  # Use uid as temporary token
                    })
                else:
                    return jsonify({"success": False, "error": "Invalid email or password"}), 401
            except Exception as e:
                error_msg = str(e)
                # If Firestore API error, show friendly message
                if "SERVICE_DISABLED" in error_msg or "PermissionDenied" in error_msg:
                    return jsonify({
                        "success": False, 
                        "error": "Firestore API is not enabled. Please enable it in Google Cloud Console.",
                        "help_url": "https://console.developers.google.com/apis/api/firestore.googleapis.com/overview"
                    }), 503
                return jsonify({"success": False, "error": f"Login failed: {error_msg}"}), 500
        elif "id_token" in data:
            # For API that sends id_token
            result = login_user(data["id_token"])
            return jsonify(result)
        else:
            return jsonify({"success": False, "error": "Missing email/password or id_token"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500

@app.route("/add_expense", methods=["POST"])
def add_expense_route():
    token = request.headers.get("Authorization")
    # If token is uid, use it directly, otherwise verify
    if token:
        # Check if token is uid
        from firebase_config import db
        user_doc = db.collection("users").document(token).get()
        if user_doc.exists:
            uid = token
        else:
            uid = verify_token(token)
    else:
        uid = None
    
    if not uid:
        return jsonify({"error": "Invalid token"}), 401

    data = request.json
    add_expense(
        uid,
        data["category"],
        data["amount"],
        data["date"],
        data.get("description", ""),
        data.get("time", None)  # Accept optional time parameter
    )
    return jsonify({"success": True})

@app.route("/expenses", methods=["GET"])
def expenses():
    token = request.headers.get("Authorization")
    # If token is uid, use it directly, otherwise verify
    if token:
        from firebase_config import db
        user_doc = db.collection("users").document(token).get()
        if user_doc.exists:
            uid = token
        else:
            uid = verify_token(token)
    else:
        uid = None
    
    if not uid:
        return jsonify({"error": "Invalid token"}), 401

    result = get_expenses(uid)
    return jsonify(result)

@app.route("/search_transactions", methods=["GET"])
def search_transactions_route():
    """Search transactions by query string"""
    token = request.headers.get("Authorization")
    # If token is uid, use it directly, otherwise verify
    if token:
        from firebase_config import db
        user_doc = db.collection("users").document(token).get()
        if user_doc.exists:
            uid = token
        else:
            uid = verify_token(token)
    else:
        uid = None
    
    if not uid:
        return jsonify({"error": "Invalid token"}), 401
    
    # Get search query from query parameters
    query = request.args.get("q", "").strip()
    
    if not query:
        return jsonify({"error": "Search query required"}), 400
    
    result = search_transactions(uid, query)
    return jsonify(result)

@app.route("/delete_expense", methods=["POST"])
def delete_expense_route():
    """Delete an expense"""
    token = request.headers.get("Authorization")
    if token:
        from firebase_config import db
        user_doc = db.collection("users").document(token).get()
        if user_doc.exists:
            uid = token
        else:
            uid = verify_token(token)
    else:
        uid = None
    
    if not uid:
        return jsonify({"error": "Invalid token"}), 401
    
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    expense_id = data.get("expense_id")
    
    if not expense_id:
        return jsonify({"error": "Expense ID required"}), 400
    
    result = delete_expense(uid, expense_id)
    if result.get("success"):
        return jsonify({"success": True, "message": "Expense deleted successfully"})
    else:
        return jsonify({"error": result.get("error", "Failed to delete expense")}), 400

@app.route("/chatbot", methods=["POST"])
def chatbot():
    """Parse natural language input and return structured data"""
    try:
        token = request.headers.get("Authorization")
        if token:
            from firebase_config import db
            user_doc = db.collection("users").document(token).get()
            if user_doc.exists:
                uid = token
            else:
                uid = verify_token(token)
        else:
            uid = None
        
        if not uid:
            return jsonify({"error": "Invalid token"}), 401
        
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        user_input = data.get("text", "").strip()
        
        if not user_input:
            return jsonify({"error": "No input provided"}), 400
        
        # Parse the natural language
        try:
            result = parse_natural_language(user_input, uid)
            print(f"DEBUG: Parsed result for '{user_input}': {result}")
        except Exception as parse_error:
            print(f"DEBUG: Error parsing input: {parse_error}")
            import traceback
            traceback.print_exc()
            return jsonify({"error": f"Error parsing input: {str(parse_error)}"}), 500
        
        # Check if it's a conversational response
        if result.get("action") == "conversation":
            return jsonify({
                "action": "conversation",
                "message": result.get("message", "Hello! How can I help you?")
            })
        
        # Check if it's an add category action
        if result.get("action") == "add_category":
            if result.get("category"):
                category_result = add_category(uid, result["category"])
                return jsonify({
                    "success": True,
                    "action": "category_added",
                    "category": category_result["category"],
                    "message": f"Category '{category_result['category']}' added successfully"
                })
            else:
                return jsonify({"error": result.get("error", "Could not extract category name")}), 400
        
        # Check if it's an analysis request
        if result.get("action") == "analyze":
            # Get all expenses for analysis
            expenses = get_expenses(uid)
            analysis = analyze_expenses(expenses, uid)
            return jsonify({
                "action": "analysis",
                "analysis": analysis
            })
        
        # Return the parsed result (for adding transactions)
        return jsonify(result)
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in chatbot endpoint: {error_trace}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/add_category", methods=["POST"])
def add_category_route():
    """Add a custom category"""
    token = request.headers.get("Authorization")
    if token:
        from firebase_config import db
        user_doc = db.collection("users").document(token).get()
        if user_doc.exists:
            uid = token
        else:
            uid = verify_token(token)
    else:
        uid = None
    
    if not uid:
        return jsonify({"error": "Invalid token"}), 401
    
    data = request.json
    category_name = data.get("category", "").strip().lower()
    
    if not category_name:
        return jsonify({"error": "Category name required"}), 400
    
    result = add_category(uid, category_name)
    return jsonify(result)

@app.route("/categories", methods=["GET"])
def categories():
    """Get all categories for the user"""
    token = request.headers.get("Authorization")
    if token:
        from firebase_config import db
        user_doc = db.collection("users").document(token).get()
        if user_doc.exists:
            uid = token
        else:
            uid = verify_token(token)
    else:
        uid = None
    
    if not uid:
        return jsonify({"error": "Invalid token"}), 401
    
    categories_list = get_categories(uid)
    return jsonify({"categories": categories_list})

@app.route("/analyze", methods=["GET"])
def analyze():
    """Get expense analysis"""
    token = request.headers.get("Authorization")
    if token:
        from firebase_config import db
        user_doc = db.collection("users").document(token).get()
        if user_doc.exists:
            uid = token
        else:
            uid = verify_token(token)
    else:
        uid = None
    
    if not uid:
        return jsonify({"error": "Invalid token"}), 401
    
    expenses = get_expenses(uid)
    analysis = analyze_expenses(expenses, uid)
    return jsonify(analysis)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
