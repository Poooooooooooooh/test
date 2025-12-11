# Expense Tracking Chatbot 💰

A complete expense tracking chatbot application with Flask frontend, Firebase backend, rule-based classification, and Pandas analytics.

## Features

- 🤖 **Smart Classification**: Automatically classifies expenses using rule-based keyword matching
- 📱 **Flask UI**: Beautiful and intuitive web interface
- 🔥 **Firebase Backend**: Secure cloud storage with Firestore
- 📊 **Analytics**: Real-time expense summaries by category using Pandas

## Project Structure

```
cpe101finalproject/
│
├── app.py                   # Flask app UI
├── firebase_config.py       # Firebase initialization
├── chatbot_service.py       # Rule-based chatbot service
├── database_service.py      # Firestore CRUD operations
├── analysis_service.py      # Pandas analytics functions
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or use an existing one
3. Go to Project Settings > Service Accounts
4. Click "Generate new private key" to download `serviceAccount.json`
5. Place `serviceAccount.json` in the project root directory

### 3. Environment Variables

Create a `.env` file in the project root with the following:

```env
GOOGLE_APPLICATION_CREDENTIALS=serviceAccount.json
```

**Note**: The app uses rule-based classification with keyword matching. No external API keys are required!

### 4. Run the Application

```bash
python app.py
```

The app will open in your browser at `http://localhost:5000`

## Usage

### Recording Expenses

Simply type your expense in the text input box. Examples:

- `กินข้าว 100` - Records 100 THB as food expense
- `รถไฟฟ้า 50` - Records 50 THB as transport expense
- `ซื้อเสื้อ 500` - Records 500 THB as shopping expense

### Asking Questions

Ask questions about your expenses:

- `เดือนนี้ใช้ค่าอาหารเท่าไหร่` - How much did you spend on food this month?
- `ใช้ค่าอาหารทั้งหมดเท่าไหร่` - Total food expenses?
- `เดือนนี้ใช้จ่ายเท่าไหร่` - Total expenses this month?

## How It Works

1. **User Input**: User enters a message like "กินข้าว 100"
2. **Rule-Based Classification**: The system classifies the message using keyword-based pattern matching
3. **Data Storage**: Classified expense is saved to Firebase Firestore
4. **Analytics**: Pandas processes the data to show:
   - Total expenses by category
   - Monthly summaries
   - Recent transactions
   - Spending trends and predictions

## Categories Supported

- 🍔 **Food** (อาหาร) - meals, restaurants, snacks
- 🚗 **Transport** (เดินทาง) - taxis, BTS, MRT, buses
- 🛒 **Shopping** (ช้อปปิ้ง) - malls, convenience stores
- 🎬 **Entertainment** (บันเทิง) - movies, concerts, games
- 📄 **Bills** (บิล) - utilities, phone, internet
- 🏥 **Health** (สุขภาพ) - medicine, hospitals, clinics
- 📚 **Education** (การศึกษา) - books, courses, school supplies
- 📝 **Other** (อื่นๆ) - miscellaneous expenses

## Troubleshooting

### Firebase Connection Issues

- Ensure `serviceAccount.json` is in the correct location
- Check that `GOOGLE_APPLICATION_CREDENTIALS` in `.env` points to the correct file
- Verify your Firebase project has Firestore enabled


### Import Errors

- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using Python 3.8 or higher

## Technology Stack

- **Frontend**: Flask
- **Backend**: Firebase Firestore
- **Chatbot**: Rule-based natural language processing
- **Analytics**: Pandas, Scikit-learn
- **Language**: Python 3.8+

## License

This project is created for educational purposes.

## Support

For issues or questions, please check:
1. Firebase documentation: https://firebase.google.com/docs
2. Flask documentation: https://flask.palletsprojects.com/
3. Pandas documentation: https://pandas.pydata.org/

