# coding=utf-8
from app import app,db
from flask import render_template, redirect, url_for, flash,session,request,jsonify
from app.models import forms, tables
from datetime import datetime,date
import sqlite3
import locale
import sys
from app.models.tables import Orcamento

locale.setlocale(locale.LC_ALL,'')

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

@app.route("/home/", methods=["GET", "POST"])
def index():
    valid = tables.Usuario.getUser(user)
    if session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))
@app.route("/orcamento/", methods=["GET","POST"])
def Orcamento():
    
    return render_template('orcamento.html',produtos = tables.Produtos.getAllProduto())

@app.route("/adicionar/produto/", methods=["GET","POST"])
def AdicionarProduto():
    locale.localeconv()['currency_symbol']
    produtos = tables.Produtos.getAllProduto()
    prod =  str(request.form['prod'])
    for produto in produtos:
        if produto.nome == prod:
            
            preco=locale.currency(produto.preco, grouping=True) 
            return jsonify({"nome":produto.nome,"preco":preco,"fornecedor":produto.fornecedor_cnpj,"id":produto.id})
    
@app.route("/fornecedor/cadastrar/", methods=["GET","POST"])
def Cadastrar_fornecedor():
    form = forms.FornecedorForm()
    print("foi")
    if form.validate_on_submit():
        formNome= str(form.fornecedor.data)
        formEmail = str(form.email.data)
        formCnpj = str(form.cnpj.data)
        try:
            print(formCnpj)
            tables.Fornecedor.insertFornecedor(formNome,formEmail,formCnpj)
        except:
            flash('CNPJ Já cadastrado')
            return render_template('Fornecedor.html',FornecedorForm=form,cadastrar=True)
        return redirect(url_for('Cadastrar_fornecedor'))

    return render_template('Fornecedor.html',FornecedorForm=form,cadastrar=True) 
@app.route("/fornecedor/", methods=["GET","POST"])
def Pesquisar_fornecedor():
    form = forms.FornecedorForm()
    
    if form.validate_on_submit():
        formCnpj = str(form.cnpj.data)
        try:
            fornecedore=tables.Fornecedor.getFornecedor(formCnpj)
        except:
            flash('CNPJ não encontrado')
            return render_template('Fornecedor.html',FornecedorForm=form,cadastrar=False,fornecedores=[])
        if fornecedore:
            return render_template('Fornecedor.html',FornecedorForm=form,cadastrar=False,pesquisa=True,fornecedores=fornecedore)
        else:
            return redirect(url_for('Pesquisar_fornecedor'))
    return render_template('Fornecedor.html',FornecedorForm=form,cadastrar=False,fornecedores=[])
@app.route("/fornecedor/atualizar/", methods=["GET","POST"])
def atualizar_fornecedor():
    form = forms.FornecedorForm(request.form)
    if request.method == 'POST':
        formNome= str(request.form['fornecedor'])
        formEmail = str(request.form['email'])
        formCnpj = str(request.form['cnpj'])
        
        if form.validate_on_submit():
            try:
                tables.Fornecedor.setFornecedor(formNome,formEmail,formCnpj)
                
            except:
                flash('Erro na atualização do fornecedor')
                return render_template('Fornecedor.html',FornecedorForm=form,cadastrar=False,pesquisa=True,atualizar=True,fornecedores=tables.Fornecedor.getFornecedor(cnpj))
            flash('Fornecedor '+formNome+' foi atualizado com sucesso')
            return redirect(url_for('Pesquisar_fornecedor'))
        else:
            return render_template('Fornecedor.html',FornecedorForm=form,cadastrar=False,pesquisa=True,atualizar=True,fornecedores=tables.Fornecedor.getFornecedor(cnpj))

        
    return render_template('Fornecedor.html',FornecedorForm=form,cadastrar=False,pesquisa=True,atualizar=True,fornecedores=tables.Fornecedor.getFornecedor(cnpj))
@app.route("/fornecedor/deletar/", methods=["GET","POST"])
def deletar_fornecedor():
    with sqlite3.connect('storage.db') as conn:
        try:
            form = forms.FornecedorForm(request.form)
            cur = conn.cursor()
            formCnpj = str(request.form['cnpj'])
            formNome= str(request.form['fornecedor'])
            print("iniciar o delete")
            print(formCnpj)
            produto = tables.Produtos.getProdutoByFornecedor(formCnpj)
            if produto:
                flash("Fornecedor "+formNome+" não pode ser deletado por existe Produto vinculado")
                return redirect(url_for('Pesquisar_fornecedor'))
            cur.execute('DELETE FROM Fornecedor WHERE cnpj = ?',(formCnpj, ))
            conn.commit()
            flash( "Fornecedor excluido com Sucesso")
            print("funcionol")
            return redirect(url_for('Pesquisar_fornecedor'))
  
        except:
            conn.rollback()
            flash("Falha ao Excluir Forncedor")
            print("falha no delete")
            return redirect(url_for('Pesquisar_fornecedor'))
    conn.close()
    print("aqui deu ruim")
    return redirect(url_for('Pesquisar_fornecedor'))

@app.route("/cliente/cadastrar/", methods=["GET","POST"])
def Cadastrar_cliente():
    form = forms.ClienteForm()
    if form.validate_on_submit():
        formNome= str(form.nome.data)
        formCpf = str(form.cpf.data)
        formTelefone = str(form.telefone.data)
        formEndereco = str(form.endereco.data)
        try:
            tables.Cliente.insertCliente(formNome,formCpf,formTelefone,formEndereco)
        except:
            flash('CPF já cadastrado')
            return render_template("cliente.html", ClienteForm=form, cadastrar=True)
        return redirect(url_for('Cadastrar_cliente'))

    return render_template("cliente.html", ClienteForm=form, cadastrar=True )
@app.route("/cliente/deletar/<cpf>", methods=["GET","POST"])
def Deletar_cliente(cpf):
    
    with sqlite3.connect('storage.db') as conn:
        try:
            cur = conn.cursor()
            print("iniciar o delete")
            print(cpf)
            OrcamentoCliente = tables.Orcamento.getClienteOrcamento(cpf)
            if OrcamentoCliente:
                flash("Cliente não pode ser deletado por existe orçamento vinculado")
                return redirect(url_for('Cadastrar_cliente'))
            cur.execute('DELETE FROM Cliente WHERE CPF = ?',(cpf, ))
            conn.commit()
            flash( "Cliente deletado com Sucesso")
            print("funcionol")
            return redirect(url_for('Pesquisar_cliente'))
  
        except:
            conn.rollback()
            flash("Falha ao deletar Cliente")
            print("falha no delete")
            return redirect(url_for('Pesquisar_cliente'))
    conn.close()
    print("aqui deu ruim")
    return redirect(url_for('Cadastrar_cliente'))
    
@app.route("/produto/cadastrar/", methods=["GET","POST"])
def Cadastrar_produto():
    cat=tables.CategoriaProduto.getCategoria()
    
    form = forms.ProdutoForm()
    if form.validate_on_submit():
        formNome= str(form.nome.data)
        formPreco = str(form.preco.data)
        formFornecedor = str(form.fornecedor.data)
        preco=formPreco.replace(".","")
        preco=preco.replace(",",".")
        categoria = str(request.form['categoria'])
        try:
            print("aqui foi")
            print(preco)
            print(formFornecedor)
            if tables.Produtos.insertProduto(formNome,preco,formFornecedor,categoria):
                flash("Produto cadastrado com Sucesso")
                return redirect(url_for('Cadastrar_produto'))
            flash('CNPJ do fornecedor não encontrado')
            return render_template("produto.html", ProdutoForm=form, cadastrar=True,categorias=tables.CategoriaProduto.getCategoria())
        except:
            print("erro aqui")
            flash('CNPJ do fornecedor não encontrado')
            return render_template("produto.html", ProdutoForm=form, cadastrar=True,categorias=tables.CategoriaProduto.getCategoria())
        
        

    return render_template("produto.html", ProdutoForm=form, cadastrar=True,categorias=tables.CategoriaProduto.getCategoria())
@app.route("/produto/deletar/<id>", methods=["GET","POST"])
def DeletarProduto(id):
    print("aqui foi")
    with sqlite3.connect('storage.db') as conn:
        try:
            cur = conn.cursor()
            OrcamentoProduto = tables.Orcamento_Produto.getOrcamentoByProduto(id)
            if OrcamentoProduto:
                flash("Produto não pode ser deletado por existe orçamento vinculado")
                return redirect(url_for('Pesquisar_produto'))
            cur.execute('DELETE FROM Produtos WHERE id = ?',(id, ))
            conn.commit()
            flash( "Produto deletado com Sucesso")
            print("funcionol")
            return redirect(url_for('Pesquisar_produto'))
        
        except:
            conn.rollback()
            flash("Falha ao deletar Produto")
            print("falha no delete")
            return redirect(url_for('Pesquisar_produto'))
    conn.close()
    print("aqui deu ruim")
    return redirect(url_for('Pesquisar_produto'))
   

@app.route("/produto/", methods=["GET","POST"])
def Pesquisar_produto():
    form = forms.ProdutoForm()
    with sqlite3.connect('storage.db') as conn:
                
        if form.validate_on_submit():
            formNome = str(form.nome.data)
            try:
                print("aqui foi")
                prod=[]
                cur = conn.cursor()
                cur.execute('SELECT * FROM Produtos WHERE nome LIKE ?',("%"+formNome+"%", ))
                produt=cur.fetchall()
                conn.commit()
                for linha in produt:
                    prod.append(tables.Produtos.getProduto(linha[1]))
                
                if produt:
                    print("aqui foi tambem")
                    print(prod)
                    return render_template('produto.html',ProdutoForm=form,cadastrar=False,pesquisa=True,produtos=prod)
            
                else:
                    flash('Produto não encontrado')
                    return redirect(url_for('Pesquisar_produto'))
            except:
                flash('Produto não encontrado')
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


@app.route("/produto/atualizar/<id>", methods=["GET","POST"])
def atualizar_produto(id):
    form = forms.ProdutoForm(request.form)
    if request.method == 'POST':
        formNome= str(request.form['nome'])
        formPreco = str(request.form['preco'])
        formPreco = formPreco.replace('.','')
        formPreco = formPreco.replace(',','.')
        formFornecedor = str(request.form["fornecedor"])
        fornecedorCnpj = tables.Fornecedor.getFornecedorByNome(formFornecedor)
        for id in fornecedorCnpj:
            Fornecedor=id.cnpj
        if fornecedorCnpj:
            flash("Produto "+formNome+" atualizado com Sucesso")
            tables.Produtos.setProduto(formNome,formPreco,Fornecedor)
            return redirect(url_for('Pesquisar_produto'))
        else:
            return render_template('produto.html',ProdutoForm=form,cadastrar=False,pesquisa=True,atualizar=True,produtos=tables.Produtos.getProduto(formNome))

        
    return render_template('produto.html',ProdutoForm=form,cadastrar=False,pesquisa=True,atualizar=True,produtos=tables.Produtos.getProduto(formNome))

@app.route("/orcamento/cadastrar/", methods=["GET","POST"])
def Cadastrar_Orcamento():
    if request.method == 'POST':
        dados = request.get_json()
        total = dados["Total"]
        data = date.today()
        #data=data.strftime("%d/%m/%y")
        try:
            codigoGerado = tables.Orcamento.insertOrcamento(total,data)
            print("aqui foi")
            print(codigoGerado)
            if(codigoGerado!=""):
                condId = int(codigoGerado)
                
                for produto in dados["nomeProduto"]:
                    idProduto = tables.Produtos.getProdutoID(produto)
                    for produto in idProduto:
                        prodid = int(produto.id)
                        tables.Orcamento_Produto.insertOrcamentoProduto(condId,prodid)
            
                return jsonify({"Resultado":"Susess","codigoOrcamento":codigoGerado})
        
        except:
            return jsonify({"Resultado":"Error"}) 
    return jsonify({"Resultado":"Error"}) 

@app.route("/Relatorio/Orcamento/")
def RelatorioOrcamento():
    
    return render_template("RelatorioOrcamento.html", orcament = tables.Orcamento.getAllorcamento())

@app.route("/Relatorio/Pedidos/")
def RelatorioPedidos():
   
    return render_template("RelatorioPedidos.html")

@app.route("/Relatorio/Pesquisar/")
def RelatorioPesquisar():
   
    return render_template("RelatorioPesquisar.html")
@app.route("/imprimir/orcamento/<codigoOrcamento>", methods=["GET","POST"])
def imprimirOrcamento(codigoOrcamento):
    try:
        orcamento = tables.Orcamento.getOrcamento(codigoOrcamento)
        
            
        if codigoOrcamento:
            if orcamento:
                for precoOrcamento in orcamento:
                    total = locale.currency(precoOrcamento.preco, grouping=True)
                produtos = []
                codProduto = tables.Orcamento_Produto.getOrcamentoProduto(codigoOrcamento)
               
                for cod in codProduto:
                    produtos.append(tables.Produtos.getProdutoID(cod.Produto_id))
                    print(produtos)
                    print(total)
                    print(codigoOrcamento)
                    
            return render_template('impressaoOrcamento.html',cart=produtos,total=total,codigo=codigoOrcamento)
    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
        return redirect(url_for('Orcamento'))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return redirect(url_for('Orcamento'))
    
    


@app.route("/Pedido/<codigoOrcamento>", methods=["GET","POST"])
@app.route("/Pedido/", methods=["GET","POST"],defaults={"codigoOrcamento":None})

def Pedido(codigoOrcamento):
   
    orcamento = tables.Orcamento.getOrcamento(codigoOrcamento)
    for precoOrcamento in orcamento:
        preco = locale.currency(precoOrcamento.preco, grouping=True) 
    if codigoOrcamento:
        if orcamento:
            produtos = []
            codProduto = tables.Orcamento_Produto.getOrcamentoProduto(codigoOrcamento)
            for cod in codProduto:
                produtos.append(tables.Produtos.getProdutoID(cod.Produto_id))
         
            return render_template("Pedido.html",cart=produtos,orcamento=preco,codigoOrcamento=codigoOrcamento)
        return redirect(url_for('Orcamento'))
    return render_template("Pedido.html")   

@app.route("/Pedido/cadastrar/", methods=["GET","POST"])
def CadastrarPedido():

    return render_template("Pedido.html")

@app.route("/Categoria/Atualizar/", methods=["GET","POST"])
def Atualizar_Categoria():

    return render_template("Pedido.html")
@app.route("/Categoria/", methods=["GET","POST"])
def ListaCategorias():

    return render_template("Pedido.html")
@app.route("/Categoria/cadastrar/", methods=["GET","POST"])
def Cadastrar_Categoria():

    return render_template("Pedido.html")