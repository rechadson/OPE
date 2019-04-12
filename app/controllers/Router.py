# coding=utf-8
from app import app,db
from flask import render_template, redirect, url_for, flash,session,request,jsonify
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
    
    return render_template('Orcamentoteste.html',produtos = tables.Produtos.getAllProduto())
@app.route("/adicionar/produto/", methods=["GET","POST"])
def AdicionarProduto():
    produtos = tables.Produtos.getAllProduto()
    prod =  str(request.form['prod'])
    
    for produto in produtos:
        if produto.nome == prod:
            print(prod)
            return jsonify({"nome":produto.nome,"preco":produto.preco,"fornecedor":produto.fornecedor_id})
    
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
    
    if form.validate_on_submit():
        formCnpj = int(form.cnpj.data)
        fornecedore=tables.Fornecedor.getFornecedor(formCnpj)
        if fornecedore:
            return render_template('Fornecedor.html',FornecedorForm=form,cadastrar=False,pesquisa=True,fornecedores=tables.Fornecedor.getFornecedor(formCnpj))
        
        else:
            return redirect(url_for('Pesquisar_fornecedor'))
    return render_template('Fornecedor.html',FornecedorForm=form,cadastrar=False,fornecedores=[])
@app.route("/fornecedor/atualizar/<cnpj>", methods=["GET","POST"])
def atualizar_fornecedor(cnpj):
    form = forms.FornecedorForm(request.form)
    if request.method == 'POST':
        formNome= str(request.form['fornecedor'])
        formEmail = str(request.form['email'])
        formCnpj = int(request.form['cnpj'])
        
        if form.validate_on_submit():
            tables.Fornecedor.setFornecedor(formNome,formEmail,formCnpj)
            return redirect(url_for('Pesquisar_fornecedor'))
        else:
            return render_template('Fornecedor.html',FornecedorForm=form,cadastrar=False,pesquisa=True,atualizar=True,fornecedores=tables.Fornecedor.getFornecedor(cnpj))

        
    return render_template('Fornecedor.html',FornecedorForm=form,cadastrar=False,pesquisa=True,atualizar=True,fornecedores=tables.Fornecedor.getFornecedor(cnpj))
@app.route("/orcamento/cadastrar/", methods=["GET","POST"])
def Cadastrar_Orcamento():
    
    if request.method == 'POST':
        formCPF= str(request.form['cpf_cliente'])
        
        print(formCPF)
        produtos = tables.Produtos.getAllProduto()
        return jsonify({"nome":produto.nome,"preco":produto.preco,"fornecedor":produto.fornecedor_id})
        tables.Fornecedor.insertFornecedor(formNome,formEmail,formCnpj)
        
        
        
    return render_template('Fornecedor.html',FornecedorForm=form,cadastrar=True) 