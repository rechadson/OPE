# coding=utf-8
from app import app,db
from flask import render_template, redirect, url_for, flash,session
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
                session['Login'] = "valid"
                print(formLogin)
                return redirect(url_for('index',user=formLogin))
            else:
                flash('Senha Inválida!')
                return redirect(url_for('login'))
        else:
            flash('Usuario inválido ou não existe!')
            return redirect(url_for('login'))
        
    return render_template('login.html',LoginForm=form)

@app.route("/home/<user>", methods=["GET", "POST"])
def index(user):
    valid = tables.Usuario.getUser(user)
    if valid:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))
@app.route("/orcamento/", methods=["GET","POST"])
def Orcamento():
    
    return render_template('Orcamento.html',produtos = tables.Produtos.getAllProduto()) 

@app.route("/fornecedor/cadastrar/", methods=["GET","POST"])
def Cadastrar_fornecedor():
    form = forms.FornecedorForm()
    if form.validate_on_submit():
        formNome= str(form.fornecedor.data)
        formEmail = str(form.email.data)
        formCnpj = int(form.cnpj.data)
        tables.Fornecedor.insertFornecedor(formNome,formEmail,formCnpj)
        return redirect(url_for('Cadastrar_fornecedor'))
        
        
    return render_template('Fornecedor.html',FornecedorForm=form,cadastrar=True) 
@app.route("/fornecedor/", methods=["GET","POST"])
def Pesquisar_fornecedor():
    form = forms.FornecedorForm()
    return render_template('Fornecedor.html',FornecedorForm=form,cadastrar=False,fornecedores=tables.Fornecedor.getAllFornecedor())