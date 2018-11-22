from app import app
from flask import render_template
from models import tables

@app.route("/", methods=["GET","POST"])
def index(User,inputPassword):
    
    return render_template('index.html')