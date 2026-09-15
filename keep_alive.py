from flask import Flask
from threading import Thread
import os

app = Flask(__name__) # <--- এই লাইনটাই আসল সমস্যা ছিল

@app.route('/')
def home():
    return "Auto Reaction Bot is Alive and Running!"

def run():
    # Render থেকে আসা নির্দিষ্ট পোর্ট অথবা ডিফল্ট 8080 ব্যবহার করবে
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
