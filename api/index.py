import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from datetime import datetime

# CRITICAL: This tells Flask to look "up" one level for the templates folder
app = Flask(__name__, template_folder='../templates')

# Connect to MongoDB using an Environment Variable (Security)
# Ensure you have added "MONGO_URI" in your Vercel Dashboard Settings
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client.vibe_db
collection = db.updates

@app.route('/')
def index():
    try:
        # Get all updates, newest first
        posts = list(collection.find().sort("_id", -1))
    except Exception as e:
        print(f"Database Error: {e}")
        posts = []
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['POST'])
def add():
    skill = request.form.get('skill')
    notes = request.form.get('notes')
    if skill:
        try:
            collection.insert_one({
                "skill": skill,
                "notes": notes,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
        except Exception as e:
            print(f"Insert Error: {e}")
            
    return redirect('/')

# Required for local testing, Vercel uses the 'app' object directly
if __name__ == "__main__":
    app.run()