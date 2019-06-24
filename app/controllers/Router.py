# coding=utf-8
from app import app,db
from flask import render_template, redirect, url_for, flash,session,request,jsonify
from app.models import forms, tables
from datetime import datetime,date
import smtplib
import sqlite3
import locale
import sys
from app.models.tables import Orcamento
locale.setlocale(locale.LC_ALL,'')
locale.localeconv()['currency_symbol']
@app.route("/<user><inputPassword>", methods=["POST"])
@app.route("/", methods=["GET","POST"],defaults={"user":None,"inputPassword":None})
def login(user,inputPassword):
    session['Login']=''
    form = forms.LoginForm()
    if form.validate_on_submit(): 
        print(form.username.data)
        formLogin  = str(form.username.data)
        formSenha = str(form.password.data)
        
        login = tables.Usuario.getUser(formLogin)
        senha = tables.Usuario.getSenha(formSenha)
        if login:
            if senha:
                session['Login'] = "valido"
                print(formLogin)
                return redirect(url_for('index'))
            else:
                flash('Senha Inválida!')
                return redirect(url_for('login'))
        else:
            flash('Usuario inválido ou não existe!')
            return redirect(url_for('login'))
        
    return render_template('login.html',LoginForm=form)
@app.route("/Cadastrar/usuario/", methods=["GET", "POST"])
def CadastrarUsuario():
    if session["Login"] == "valido":
        try:
            if request.method == 'POST':
                User= str(request.form['Usuario'])
                Senha = str(request.form['Senha'])
                print(User)
                print(Senha)
                tables.Usuario.inserirUsuario(User,Senha)
                flash("Usuario cadastrado com Sucesso")
                return redirect(url_for('CadastrarUsuario'))
            return render_template('cadastrarUsuario.html')
        except:  
            flash("Falha ao cadastrar usuário tente novamente")      
            return redirect(url_for('CadastrarUsuario'))
    else:
        return redirect(url_for('login'))
@app.route("/logout/", methods=["GET", "POST"])
def logout(): 
    session["Login"]=""
    print(session)
    return redirect(url_for('login'))

@app.route("/home/", methods=["GET", "POST"])
def index():
    print(session)
    if session["Login"] == "valido":
        return render_template('index.html')
    else:
        return redirect(url_for('login'))
@app.route("/orcamento/", methods=["GET","POST"])
def Orcamento():
    if session["Login"] == "valido":
        return render_template('orcamento.html',produtos = tables.Produtos.getAllProduto())
    else:
        return redirect(url_for('login'))
    

@app.route("/metragem/produto/", methods=["GET","POST"])
def Calcularmetragem():
    if session["Login"] == "valido":
        prod =  str(request.form['prod'])
        produtos = tables.Produtos.getProduto(prod)
        for produto in produtos:
            if produto.metragem:
                return jsonify({"Metragem":"Calcular"})
            return jsonify({"Metragem":"NaoCalcular"})
    else:
        return redirect(url_for('login'))       
@app.route("/adicionar/produto/", methods=["GET","POST"])
def AdicionarProduto():
    if session["Login"] == "valido":
        produtos = tables.Produtos.getAllProduto()
        prod =  str(request.form['prod'])
        metragem = int(request.form['metragem'])
        for produto in produtos:
            if produto.nome == prod:
                preco = produto.preco*metragem
                preco=locale.currency(preco, grouping=True) 
                return jsonify({"nome":produto.nome,"preco":preco,"fornecedor":produto.fornecedor_cnpj,"id":produto.id})
    else:
        return redirect(url_for('login'))
@app.route("/fornecedor/cadastrar/", methods=["GET","POST"])
def Cadastrar_fornecedor():
    if session["Login"] == "valido":
        form = forms.FornecedorForm()
        print("foi")
        if form.validate_on_submit():
            formNome= str(form.fornecedor.data)
            formEmail = str(form.email.data)
            formCnpj = str(form.cnpj.data)
            try:
                print(formCnpj)
                tables.Fornecedor.insertFornecedor(formNome,formEmail,formCnpj)
                flash('Fornecedor '+formNome+' cadastrado com Sucesso')
            except:
                flash('CNPJ Já cadastrado')
                return render_template('Fornecedor.html',FornecedorForm=form,cadastrar=True)
            return redirect(url_for('Cadastrar_fornecedor'))

        return render_template('Fornecedor.html',FornecedorForm=form,cadastrar=True)
    else:
        return redirect(url_for('login')) 
@app.route("/fornecedor/", methods=["GET","POST"])
def Pesquisar_fornecedor():
    if session["Login"] == "valido":
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
    else:
        return redirect(url_for('login'))
@app.route("/fornecedor/atualizar/", methods=["GET","POST"])
def atualizar_fornecedor():
    if session["Login"] == "valido":
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
    else:
        return redirect(url_for('login'))
@app.route("/fornecedor/deletar/", methods=["GET","POST"])
def deletar_fornecedor():
    if session["Login"] == "valido":
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
    else:
        return redirect(url_for('login'))
@app.route("/cliente/cadastrar/", methods=["GET","POST"])
def Cadastrar_cliente():
    if session["Login"] == "valido":
        form = forms.ClienteForm()
        if form.validate_on_submit():
            formNome= str(form.nome.data)
            formCpf = str(form.cpf.data)
            formTelefone = str(form.telefone.data)
            formEndereco = str(form.endereco.data)
            complemento= str(request.form['Complemento'])
            cidade= str(request.form['Cidade'])
            estado= str(request.form['Estado'])
            cep= str(request.form['CEP'])
            email= str(request.form['email'])
            try:
                tables.Cliente.insertCliente(formNome,email,formCpf,formTelefone,formEndereco,cidade,estado,complemento,cep)
                flash('Cliente cadastrado com sucesso')
            except:
                flash('CPF já cadastrado')
                return render_template("cliente.html", ClienteForm=form, cadastrar=True)
            return redirect(url_for('Cadastrar_cliente'))

        return render_template("cliente.html", ClienteForm=form, cadastrar=True )
    else:
        return redirect(url_for('login'))
@app.route("/cliente/deletar/<cpf>", methods=["GET","POST"])
def Deletar_cliente(cpf):
    if session["Login"] == "valido":
        with sqlite3.connect('storage.db') as conn:
            try:
                cur = conn.cursor()
                print("iniciar o delete")
                print(cpf)
                OrcamentoCliente = tables.Pedido.getPedidobycliente(cpf)
                if OrcamentoCliente:
                    flash("Cliente não pode ser deletado por existir Pedido vinculado")
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
    else:
        return redirect(url_for('login'))
@app.route("/produto/cadastrar/", methods=["GET","POST"])
def Cadastrar_produto():    
    if session["Login"] == "valido":
        form = forms.ProdutoForm()
        if form.validate_on_submit():
            formNome= str(form.nome.data)
            formPreco = str(form.preco.data)
            formFornecedor = str(request.form['fornecedor'])
            preco=formPreco.replace(".","")
            preco=preco.replace(",",".")
            metragem = int(request.form['metragem'])
            try:
                
                if tables.Fornecedor.getFornecedorByNome(formFornecedor):
                    for fornecedor in tables.Fornecedor.getFornecedorByNome(formFornecedor):
                        fornecedorCNPJ = fornecedor.cnpj
                    
                    if tables.Produtos.insertProduto(formNome,preco,metragem,fornecedorCNPJ):
                        flash("Produto cadastrado com Sucesso")
                        return redirect(url_for('Cadastrar_produto'))
                    
                return render_template("produto.html", ProdutoForm=form, cadastrar=True,fornecedores=tables.Fornecedor.getAllFornecedor())
            except:
                print("erro aqui")
                flash('CNPJ do fornecedor não encontrado')
                return render_template("produto.html", ProdutoForm=form, cadastrar=True,fornecedores=tables.Fornecedor.getAllFornecedor())
        return render_template("produto.html", ProdutoForm=form, cadastrar=True,fornecedores=tables.Fornecedor.getAllFornecedor())
    else:
        return redirect(url_for('login'))
@app.route("/produto/deletar/<id>", methods=["GET","POST"])
def DeletarProduto(id):
    if session["Login"] == "valido":
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
        
        return redirect(url_for('Pesquisar_produto'))
    else:
        return redirect(url_for('login'))

@app.route("/produto/", methods=["GET","POST"])
def Pesquisar_produto():
    if session["Login"] == "valido":
        form = forms.ProdutoForm()
        with sqlite3.connect('storage.db') as conn:
                    
            if form.validate_on_submit():
                formNome = str(form.nome.data)
                try:
                    prod=[]
                    cur = conn.cursor()
                    cur.execute('SELECT * FROM Produtos WHERE nome LIKE ?',("%"+formNome+"%", ))
                    produt=cur.fetchall()
                    conn.commit()
                    for linha in produt: 
                        precomoeda = str(locale.currency(linha[2], grouping=True)).replace("R$","").strip(" ")
                        fornecedor = tables.Fornecedor.getFornecedor(linha[4])
                        prod.append([linha,precomoeda,fornecedor.nome])   
                    if produt:
                        return render_template('produto.html',ProdutoForm=form,cadastrar=False,pesquisa=True,produtos=prod)
                
                    else:
                        flash('Produto não encontrado')
                        return redirect(url_for('Pesquisar_produto'))
                except:
                    flash('Produto não encontrado')
                    return redirect(url_for('Pesquisar_produto'))
           
        return render_template('produto.html',ProdutoForm=form,cadastrar=False,produtos=tables.Produtos.getAllProduto())
    else:
        return redirect(url_for('login'))


@app.route("/cliente/", methods=["GET","POST"])
def Pesquisar_cliente():
    if session["Login"] == "valido":
        form = forms.ClienteForm()
        try:
            if form.validate_on_submit():
                formCpf = str(form.cpf.data)
                client=tables.Cliente.getCliente(formCpf)
                if client:
                    return render_template('cliente.html',ClienteForm=form,cadastrar=False,pesquisa=True,clientes=tables.Cliente.getCliente(formCpf))
                
                else:
                    flash('Cliente não encontrado')
                    return redirect(url_for('Pesquisar_cliente'))
            if request.method == 'POST':
                formCpf= str(request.form['cpf'])
                client=tables.Cliente.getCliente(formCpf)
                if client:
                    for cliente in client:    
                        return jsonify({"email":cliente.email,"CPF":cliente.CPF,"nome":cliente.nome,"telefone":cliente.telefone,"Endereco":cliente.Endereco,"Cidade":cliente.Cidade,"Estado":cliente.Estado,"Complemento":cliente.Complemento,"CEP":cliente.CEP})
                return jsonify({"CPF":"Não cadastrado"})
        except:
            return render_template('cliente.html',ClienteForm=form,cadastrar=False,clientes=tables.Cliente.getAllCliente())
        return render_template('cliente.html',ClienteForm=form,cadastrar=False,clientes=tables.Cliente.getAllCliente())
    else:
        return redirect(url_for('login'))
@app.route("/cliente/atualizar/<cpf>", methods=["GET","POST"])
def atualizar_cliente(cpf):
    if session["Login"] == "valido":
        form = forms.ClienteForm(request.form)
        try:
            if request.method == 'POST':
                formNome= str(request.form['cliente'])
                email= str(request.form['email'])
                formCpf = str(request.form['cpf'])
                formTelefone = str(request.form["telefone"])
                formEndereco = str(request.form['endereco'])
                complemento= str(request.form['Complemento'])
                cidade= str(request.form['Cidade'])
                estado= str(request.form['Estado'])
                cep= str(request.form['CEP'])
                tables.Cliente.setCliente(formNome,email,formCpf,formTelefone,formEndereco,cidade,estado,complemento,cep)
                flash('Cliente '+formNome+' atualizado com sucesso')
                return redirect(url_for('Pesquisar_cliente'))
        except:
            flash('Falaha ao atualizar cliente '+formNome+' tente novamente')
            return render_template('cliente.html',ClienteForm=form,cadastrar=False,pesquisa=True,atualizar=True,clientes=tables.Cliente.getCliente(cpf))
    else:
        return redirect(url_for('login'))

@app.route("/produto/atualizar/<id>", methods=["GET","POST"])
def atualizar_produto(id):
    if session["Login"] == "valido":
        form = forms.ProdutoForm(request.form)
        if request.method == 'POST':
            formNome= str(request.form['nome'])
            formPreco = str(request.form['preco'])
            formPreco = formPreco.replace('.','')
            formPreco = formPreco.replace(',','.')
            formFornecedor = str(request.form["fornecedor"])
            metragem = int(request.form['metragem'])
            fornecedorCnpj = tables.Fornecedor.getFornecedorByNome(formFornecedor)
            for idfornecedor in fornecedorCnpj:
                Fornecedor=idfornecedor.cnpj
            if fornecedorCnpj:
                print(formNome)
                flash("Produto "+formNome+" atualizado com Sucesso")
                tables.Produtos.setProduto(id,formNome,formPreco,metragem,Fornecedor)
                return redirect(url_for('Pesquisar_produto'))
            else:
                return render_template('produto.html',ProdutoForm=form,cadastrar=False,pesquisa=True,atualizar=True,produtos=tables.Produtos.getProduto(formNome))     
        return render_template('produto.html',ProdutoForm=form,cadastrar=False,pesquisa=True,atualizar=True,produtos=tables.Produtos.getProduto(formNome))
    else:
        return redirect(url_for('login'))
@app.route("/orcamento/cadastrar/", methods=["GET","POST"])
def Cadastrar_Orcamento():
    if session["Login"] == "valido":
        if request.method == 'POST':
            dados = request.get_json()
            total = dados["Total"].replace(".","")
            total = float(total.replace(",","."))
            data = date.today()
            dataEntrega = int(dados["DiasEntrega"])
            Status = "Aguardando"
            #data=data.strftime("%d/%m/%y")
            try:
                codigoGerado = tables.Orcamento.insertOrcamento(total,data,dataEntrega,Status)
                if(codigoGerado!=""):
                    condId = int(codigoGerado)
                    print(total)
                    for produto in dados["nomeProduto"]:
                        idProduto = tables.Produtos.getProdutoID(produto)
                        tables.Orcamento_Produto.insertOrcamentoProduto(condId,idProduto.id)
                
                    return jsonify({"Resultado":"Susess","codigoOrcamento":codigoGerado})
            
            except:
                return jsonify({"Resultado":"Error"}) 
        return jsonify({"Resultado":"Error"}) 
    else:
        return redirect(url_for('login'))
@app.route("/relatorio/<lista>",methods=["GET","POST"])
@app.route("/relatorio/",methods=["GET","POST"],defaults={"lista":None})
def relatorio(lista):
    if session["Login"] == "valido":
        with sqlite3.connect('storage.db') as conn:
            try:
                cur = conn.cursor()
                if request.method == 'POST':
                    total = 0
                    if request.form['acao']=="pesquisar":
                        tipo = str(request.form['tipoRelatorio'])
                        return jsonify({"Tipo":tipo})
                    tipo = request.form['tipo']
                    datainicial= request.form['DataInicial']
                    datafinal = request.form['DataFinal']
                    if tipo == "Pedido":
                        CPF = request.form['cpf'].strip(" ")
                        if CPF == "":
                            itens = []
                            cur.execute('SELECT * FROM Pedido where data >=? and data <= ?',(datainicial,datafinal, ))
                            relatorio=cur.fetchall()
                            for linha in relatorio: 
                                precomoeda = str(locale.currency(linha[4], grouping=True)).replace("R$","").strip(" ")
                                total = total + linha[4]
                                orcamento = tables.Orcamento.getOrcamento(linha[1])
                                for linhaentrega in orcamento:
                                    entrega = int(linhaentrega.prazoEntrega)
                                datafim = linha[3].replace("-","/")
                                datafim = datetime.strptime(datafim, '%Y/%m/%d').date()
                                datafim =date.fromordinal(datafim.toordinal()+entrega)
                                datafim = datafim.strftime("%d/%m/%Y")
                                data = linha[3].replace("-","/")
                                data = datetime.strptime(data, '%Y/%m/%d').date()
                                data = data.strftime("%d/%m/%Y")
                                itens.append([linha,datafim,data,precomoeda])
                            conn.commit()
                        else:
                            itens = []
                            cur.execute('SELECT * FROM Pedido where cliente_cpf = ? and data >=? and data <= ?',(CPF,datainicial,datafinal, ))
                            relatorio=cur.fetchall()
                            for linha in relatorio: 
                                precomoeda = str(locale.currency(linha[4], grouping=True)).replace("R$","").strip(" ")
                                total = total + linha[4]
                                orcamento = tables.Orcamento.getOrcamento(linha[1])
                                for linhaentrega in orcamento:
                                    entrega = int(linhaentrega.prazoEntrega)
                                datafim = linha[3].replace("-","/")
                                datafim = datetime.strptime(datafim, '%Y/%m/%d').date()
                                datafim =date.fromordinal(datafim.toordinal()+entrega)
                                datafim = datafim.strftime("%d/%m/%Y")
                                data = linha[3].replace("-","/")
                                data = datetime.strptime(data, '%Y/%m/%d').date()
                                data = data.strftime("%d/%m/%Y")
                                itens.append([linha,datafim,data,precomoeda])
                            conn.commit()
                        total = locale.currency(total, grouping=True)
                        return render_template("RelatorioPedidos.html", pedidos = itens,total=total)
                    if tipo == "Orçamento":
                        itens = []
                        status = str(request.form['Status']).strip(" ")
                        print(status)
                        if status == "":
                            cur.execute('SELECT * FROM Orcamento where data >=? and data <= ?',(datainicial,datafinal, ))
                            relatorio=cur.fetchall()
                            for linha in relatorio: 
                                precomoeda = str(locale.currency(linha[1], grouping=True)).replace("R$","").strip(" ")
                                total = total + linha[1]
                                print(total)
                                datafim = linha[2].replace("-","/")
                                datafim = datetime.strptime(datafim, '%Y/%m/%d').date()
                                datafim =date.fromordinal(datafim.toordinal()+15)
                                datafim = datafim.strftime("%d/%m/%Y")
                                data = linha[2].replace("-","/")
                                data = datetime.strptime(data, '%Y/%m/%d').date()
                                data = data.strftime("%d/%m/%Y")
                                itens.append([linha,datafim,data,precomoeda])
                                conn.commit()
                        else:
                            print(status)
                            cur.execute('SELECT * FROM Orcamento where data >=? and data <= ? and Status = ?',(datainicial,datafinal,status, ))
                            relatorio=cur.fetchall()
                            for linha in relatorio:
                                print(relatorio)
                                precomoeda = str(locale.currency(linha[1], grouping=True)).replace("R$","").strip(" ")
                                total = total + linha[1]
                                datafim = linha[2].replace("-","/")
                                datafim = datetime.strptime(datafim, '%Y/%m/%d').date()
                                datafim =date.fromordinal(datafim.toordinal()+15)
                                datafim = datafim.strftime("%d/%m/%Y")
                                data = linha[2].replace("-","/")
                                data = datetime.strptime(data, '%Y/%m/%d').date()
                                data = data.strftime("%d/%m/%Y")
                                itens.append([linha,datafim,data,precomoeda])
                                conn.commit()
                        total = locale.currency(total, grouping=True)
                        return render_template("RelatorioOrcamento.html", orcamentos = itens,total=total)
            except:
                flash("Erro ao gerar relatório")
                return redirect(url_for('RelatorioPesquisar'))
    else:
        return redirect(url_for('login'))    
@app.route("/Relatorio/Pesquisar/")
def RelatorioPesquisar():
    if session["Login"] == "valido":
        return render_template("RelatorioPesquisar.html")
    else:
        return redirect(url_for('login'))
@app.route("/imprimir/orcamento/<codigoOrcamento>", methods=["GET","POST"])
def imprimirOrcamento(codigoOrcamento):
    if session["Login"] == "valido":
        try:
            orcamento = tables.Orcamento.getOrcamento(codigoOrcamento)
            for intem in orcamento:
                preco = locale.currency(intem.preco, grouping=True)
                codOrcamento = intem.id
                data = intem.data
                diasEntrega = int(intem.prazoEntrega)
                datafim = date.fromordinal(data.toordinal()+15)
                data = data.strftime("%d/%m/%Y")
                datafim = datafim.strftime("%d/%m/%Y")
            if codigoOrcamento:
                if orcamento:
                    produtos = []
                    codProduto = tables.Orcamento_Produto.getOrcamentoProduto(codigoOrcamento)
                    for cod in codProduto:
                        produtos.append(tables.Produtos.getProdutoID(cod.Produto_id))
                    return render_template("impressaoOrcamento.html",cart=produtos,total=preco,orcamento=codOrcamento,data=data,datafim=datafim,diasEntrega=diasEntrega)
            return redirect(url_for('Orcamento'))
        except OSError as err:
            print("OS error: {0}".format(err))
        except ValueError:
            print("Could not convert data to an integer.")
            return redirect(url_for('Orcamento'))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return redirect(url_for('Orcamento'))
    else:
        return redirect(url_for('login'))
@app.route("/pedido/imprimir/<codigoPedido>", methods=["GET","POST"])
def imprimirPedido(codigoPedido):
    if session["Login"] == "valido":
        try:
            Pedido = tables.Pedido.getPedido(codigoPedido)
            orcamento = tables.Orcamento.getOrcamento(Pedido.orcamento_id)
            Cliente = tables.Cliente.getCliente(Pedido.cliente_cpf)
            print(Cliente)
            for intem in orcamento:
                preco = locale.currency(Pedido.valor, grouping=True)
                codOrcamento = intem.id
                data = Pedido.data
                diasEntrega = int(intem.prazoEntrega)
                datafim = date.fromordinal(data.toordinal()+diasEntrega)
                data = data.strftime("%d/%m/%Y")
                datafim = datafim.strftime("%d/%m/%Y")
            if codigoPedido:
                if orcamento:
                    produtos = []
                    codProduto = tables.Orcamento_Produto.getOrcamentoProduto(Pedido.orcamento_id)
                    for cod in codProduto:
                        produtos.append(tables.Produtos.getProdutoID(cod.Produto_id))
                    return render_template("impressaoPedido.html",cart=produtos,total=preco,Pedido=Pedido.id,data=data,datafim=datafim,diasEntrega=diasEntrega,Cliente=Cliente)
            return redirect(url_for('Pedido'))
        except OSError as err:
            print("OS error: {0}".format(err))
        except ValueError:
            print("Could not convert data to an integer.")
            return redirect(url_for('Pedido'))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return redirect(url_for('Pedido'))
    else:
        return redirect(url_for('login'))
@app.route("/Pedido/<codigoOrcamento>", methods=["GET","POST"])
@app.route("/Pedido/", methods=["GET","POST"],defaults={"codigoOrcamento":None})

def Pedido(codigoOrcamento):
    if session["Login"] == "valido":
        try:
            Pedido = tables.Pedido.getPedidobyOrcamento(codigoOrcamento)
            orcamento = tables.Orcamento.getOrcamento(codigoOrcamento)
            print(Pedido)
            for precoOrcamento in orcamento:
                precoatual = locale.currency(precoOrcamento.preco, grouping=True)
                preco = locale.currency(precoOrcamento.preco, grouping=True).replace("R$","").strip(" ")
            if codigoOrcamento:
                if orcamento:
                    produtos = []
                    codProduto = tables.Orcamento_Produto.getOrcamentoProduto(codigoOrcamento)
                    for cod in codProduto:
                        produtos.append(tables.Produtos.getProdutoID(cod.Produto_id))
                    if Pedido:
                        return render_template("Pedido.html",codigoPedido=Pedido.id,cart=produtos,precoOrcamento=precoatual,orcamento=preco,codigoOrcamento=codigoOrcamento,codigo=True,pesquisa=False)
                    return render_template("Pedido.html",cart=produtos,precoOrcamento=precoatual,orcamento=preco,codigoOrcamento=codigoOrcamento,codigo=True,pesquisa=False)
                
                return redirect(url_for('Orcamento'))
            return render_template("Pedido.html")   
        except:
            return render_template("Pedido.html")
    else:
        return redirect(url_for('login'))

@app.route("/Pedido/verificar/<codigoPedido>", methods=["GET","POST"])
def listarPedido(codigoPedido):
    if session["Login"] == "valido":
        try:
            Pedido = tables.Pedido.getPedido(codigoPedido)
            orcamento = tables.Orcamento.getOrcamento(Pedido.orcamento_id)
            Cliente = tables.Cliente.getCliente(Pedido.cliente_cpf)
            for precoOrcamento in orcamento:
                precoatual = locale.currency(precoOrcamento.preco, grouping=True)
                preco = locale.currency(precoOrcamento.preco, grouping=True).replace("R$","").strip(" ")
                codigoOrcamento = precoOrcamento.id
            if Pedido:
                if orcamento:
                    produtos = []
                    codProduto = tables.Orcamento_Produto.getOrcamentoProduto(codigoOrcamento)
                    for cod in codProduto:
                        produtos.append(tables.Produtos.getProdutoID(cod.Produto_id))
                    return render_template("Pedido.html",codigoPedido=codigoPedido,Pedido = Pedido,Cliente=Cliente,cart=produtos,precoOrcamento=precoatual,orcamento=preco,codigoOrcamento=codigoOrcamento,pesquisa=True,codigo=False)
                return redirect(url_for('Orcamento'))
            return render_template("Pedido.html")   
        except:
            return render_template("Pedido.html")
    else:
        return redirect(url_for('login'))
@app.route("/Orcamento/verificar/<codigoOrcamento>", methods=["GET","POST"])
def listarOrcamento(codigoOrcamento):
    if session["Login"] == "valido":
        try:
            orcamento = tables.Orcamento.getOrcamento(codigoOrcamento)
            for precoOrcamento in orcamento:
                precoatual = locale.currency(precoOrcamento.preco, grouping=True)
                preco = locale.currency(precoOrcamento.preco, grouping=True).replace("R$","").strip(" ")
                codigoOrcamento = precoOrcamento.id
            if Pedido:
                if orcamento:
                    produtos = []
                    codProduto = tables.Orcamento_Produto.getOrcamentoProduto(codigoOrcamento)
                    for cod in codProduto:
                        produtos.append(tables.Produtos.getProdutoID(cod.Produto_id))
                    return render_template("Orcamento.html",Pedido = Pedido,Cliente=Cliente,cart=produtos,precoOrcamento=precoatual,orcamento=preco,codigoOrcamento=codigoOrcamento,pesquisa=True,codigo=False)
                return redirect(url_for('Orcamento'))
            return render_template("Pedido.html")   
        except:
            return render_template("Pedido.html")
    else:
        return redirect(url_for('login'))

@app.route("/Pedido/cadastrar/", methods=["GET","POST"])
def CadastrarPedido():
    if session["Login"] == "valido":
        if request.method == 'POST':
            formNome= str(request.form['Nome'])
            valor= str(request.form['valor'])
            valor=valor.replace("R$","")
            valor=valor.replace(".","")
            valor=valor.replace(",",".")
            cpf= str(request.form['cpf'])
            email= str(request.form['email'])
            telefone= str(request.form['Telefone'])
            endereco= str(request.form['Endereco'])
            complemento= str(request.form['Complemento'])
            cidade= str(request.form['Cidade'])
            estado= str(request.form['Estado'])
            cep= str(request.form['CEP'])
            formaPagamento= str(request.form['Pagamento'])
            codigoOrcamento = int(request.form['codOrcamento'])
            data=date.today()
            try:
                cliente = tables.Cliente.getCliente(cpf)
                if cliente == []:
                    tables.Cliente.insertCliente(formNome,email,cpf,telefone,endereco,cidade,estado,complemento,cep)
                orcamento = tables.Orcamento.getOrcamento(codigoOrcamento)
                Status="Aprovado"
                for dataorcamento in orcamento:
                    data = dataorcamento.data
                    datamaxima = date.fromordinal(data.toordinal()+15)
                if date.today()>datamaxima:

                    flash("Orçamento "+str(codigoOrcamento)+" Está com mais de 15 dias após gerado")
                    return render_template("Pedido.html")

                pedido = tables.Pedido.getPedidobyOrcamento(codigoOrcamento)
                if pedido:
                    flash("Orçamento "+str(codigoOrcamento)+" já foi utilizado em outro pedido")
                    return render_template("Pedido.html")
                print("inserindo pedido")
                tables.Pedido.cadastrarPedido(codigoOrcamento,cpf,data,valor,formaPagamento)
                flash("Pedido realizado com Sucesso")
                orcamento = tables.Orcamento.setStatusOrcamento(codigoOrcamento,Status)
                pedido = tables.Pedido.getPedidobyOrcamento(codigoOrcamento)
                return redirect(url_for('imprimirPedido',codigoPedido=pedido.id))
            except:
                flash("Falha ao gerar pedido tente novamente")
                return render_template("Pedido.html")

        return render_template("Pedido.html")
    else:
        return redirect(url_for('login'))
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('login'))
@app.errorhandler(401)
def page_not_found(e):
    return redirect(url_for('login'))
@app.errorhandler(403)
def page_not_found(e):
    return redirect(url_for('login'))
@app.errorhandler(500)
def page_not_found(e):
    return redirect(url_for('login'))
@app.errorhandler(400)
def page_not_found(e):
    return redirect(url_for('login'))