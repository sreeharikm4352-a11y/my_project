import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Connect to MongoDB using an Environment Variable (Security)
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.vibe_db
collection = db.updates

@app.route('/')
def index():
    # Get all updates, newest first
    posts = list(collection.find().sort("_id", -1))
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['POST'])
def add():
    skill = request.form.get('skill')
    notes = request.form.get('notes')
    if skill:
        collection.insert_one({
            "skill": skill,
            "notes": notes,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
    return redirect('/')

# This is required for Vercel
if __name__ == '__main__':
    app.run()