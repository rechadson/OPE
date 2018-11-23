from app import app,db
from flask import render_template
from app.models import forms, tables



@app.route("/<user><inputPassword>", methods=["POST"])
@app.route("/", methods=["GET","POST"],defaults={"user":None,"inputPassword":None})
def index(user,inputPassword):
    
    form = forms.LoginForm()
    if form.validate_on_submit():
        
        
        user = [tables.Usuario.query.filter_by(User = form.username.data).all()]
        All = tables.Usuario.query.all()
        print(user)
        print (All)
        

       
    else:
        print(form.errors)
    
    return render_template('index.html',LoginForm=form)