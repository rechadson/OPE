# coding=utf-8
from app import app,db
from flask import render_template, redirect, url_for, flash,session,request,jsonify
from app.models import forms, tables
import sqlite3


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
    
    return render_template('orcamento.html',produtos = tables.Produtos.getAllProduto())
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

@app.route("/cliente/cadastrar/", methods=["GET","POST"])
def Cadastrar_cliente():
    form = forms.ClienteForm()
    if form.validate_on_submit():
        formNome= str(form.nome.data)
        formCpf = str(form.cpf.data)
        formTelefone = str(form.telefone.data)
        formEndereco = str(form.endereco.data)
        tables.Cliente.insertCliente(formNome,formCpf,formTelefone,formEndereco)
        return redirect(url_for('Cadastrar_cliente'))

    return render_template("cliente.html", ClienteForm=form, cadastrar=True )


@app.route("/produto/cadastrar/", methods=["GET","POST"])
def Cadastrar_produto():
    form = forms.ProdutoForm()
    if form.validate_on_submit():
        formNome= str(form.nome.data)
        formPreco = str(form.preco.data)
        formFornecedor = str(form.fornecedor.data)
        tables.Produtos.insertProduto(formNome,formPreco,formFornecedor)
        return redirect(url_for('Cadastrar_produto'))

    return render_template("produto.html", ProdutoForm=form, cadastrar=True )

@app.route("/produto/", methods=["GET","POST"])
def Pesquisar_produto():
    form = forms.ProdutoForm()
    
    if form.validate_on_submit():
        formNome = str(form.nome.data)
        produt=tables.Produtos.getProduto(formNome)
        if produt:
            return render_template('produto.html',ProdutoForm=form,cadastrar=False,pesquisa=True,produtos=tables.Produtos.getProduto(formNome))
        
        else:
            return redirect(url_for('Pesquisar_produto'))
    return render_template('produto.html',ProdutoForm=form,cadastrar=False,produtos=tables.Produtos.getAllProduto())



@app.route("/cliente/", methods=["GET","POST"])
def Pesquisar_cliente():
    form = forms.ClienteForm()
    
    if form.validate_on_submit():
        formCpf = str(form.cpf.data)
        client=tables.Cliente.getCliente(formCpf)
        if client:
            return render_template('cliente.html',ClienteForm=form,cadastrar=False,pesquisa=True,clientes=tables.Cliente.getCliente(formCpf))
        
        else:
            return redirect(url_for('Pesquisar_cliente'))
    return render_template('cliente.html',ClienteForm=form,cadastrar=False,clientes=tables.Cliente.getAllCliente())

@app.route("/cliente/atualizar/<cpf>", methods=["GET","POST"])
def atualizar_cliente(cpf):
    form = forms.ClienteForm(request.form)
    if request.method == 'POST':
        formNome= str(request.form['nome'])
        formCpf = str(request.form['cpf'])
        formTelefone = str(request.form["telefone"])
        formEndereco = str(request.form['endereco'])
        
        if form.validate_on_submit():
            tables.Cliente.setCliente(formNome,formCpf,formTelefone,formEndereco)
            return redirect(url_for('Pesquisar_cliente'))
        else:
            return render_template('cliente.html',ClienteForm=form,cadastrar=False,pesquisa=True,atualizar=True,clientes=tables.Cliente.getCliente(cpf))

        
    return render_template('cliente.html',ClienteForm=form,cadastrar=False,pesquisa=True,atualizar=True,clientes=tables.Cliente.getCliente(cpf))


@app.route("/produto/atualizar/<nome>", methods=["GET","POST"])
def atualizar_produto(nome):
    form = forms.ProdutoForm(request.form)
    if request.method == 'POST':
        formNome= str(request.form['nome'])
        formPreco = str(request.form['preco'])
        formFornecedor = str(request.form["fornecedor"])
        
        if form.validate_on_submit():
            tables.Produtos.setProduto(formNome,formPreco,formFornecedor)
            return redirect(url_for('Pesquisar_produto'))
        else:
            return render_template('produto.html',ProdutoForm=form,cadastrar=False,pesquisa=True,atualizar=True,produtos=tables.Produtos.getProduto(nome))

        
    return render_template('produto.html',ProdutoForm=form,cadastrar=False,pesquisa=True,atualizar=True,produtos=tables.Produtos.getProduto(nome))

@app.route("/orcamento/cadastrar/", methods=["GET","POST"])
def Cadastrar_Orcamento():
    
    if request.method == 'POST':
        formCPF= str(request.args.get('cpf_cliente'))
        nomedoprod = request.args.get('nome_produto')
        print(formCPF)
        print(nomedoprod)
        produtos = tables.Produtos.getAllProduto()
        return redirect(url_for('Cadastrar_Orcamento'))
        
        
        
    return redirect(url_for('Cadastrar_Orcamento')) 

