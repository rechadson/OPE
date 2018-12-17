# coding=utf-8
from app import app,db
from flask import render_template, redirect, url_for, flash
from app.models import forms, tables



@app.route("/<user><inputPassword>", methods=["POST"])
@app.route("/", methods=["GET","POST"],defaults={"user":None,"inputPassword":None})
def login(user,inputPassword):
    
    form = forms.LoginForm()
    if form.validate_on_submit(): 
        print(form.username.data)
        formLogin  = str(form.username.data)
        formSenha = str(form.password.data)
        
        login = tables.Usuario.getUser(formLogin)
        senha = tables.Usuario.getSenha(formSenha)
        if login:
            if senha:
                return redirect(url_for('index'))
            else:
                flash('Senha Inválida!')
                return redirect(url_for('login'))
        else:
            flash('Usuario inválido ou não existe!')
            return redirect(url_for('login'))
        
    return render_template('login.html',LoginForm=form)