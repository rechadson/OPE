from app import app,db
from flask import render_template
from app.models import forms, tables



@app.route("/<user><inputPassword>", methods=["POST"])
@app.route("/", methods=["GET","POST"],defaults={"user":None,"inputPassword":None})
def index(user,inputPassword):
    
    form = forms.LoginForm()
    if form.validate_on_submit(): 
        print(form.username.data)
        formLogin  = str(form.username.data)
        formSenha = str(form.password.data)
        
        try:
            login = tables.Usuario.getUser(formLogin)
            senha = tables.Usuario.getSenha(formSenha)
        except errors as errors:
            return print("erro")       
        print (login,senha)
        
        
        

       
    else:
        print(form.errors)
    
    return render_template('index.html',LoginForm=form)