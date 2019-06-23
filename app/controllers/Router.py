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

@app.route("/metragem/produto/", methods=["GET","POST"])
def Calcularmetragem():
    prod =  str(request.form['prod'])
    produtos = tables.Produtos.getProduto(prod)
    for produto in produtos:
        if produto.metragem:
            return jsonify({"Metragem":"Calcular"})
        return jsonify({"Metragem":"NaoCalcular"})
@app.route("/adicionar/produto/", methods=["GET","POST"])
def AdicionarProduto():
    
    produtos = tables.Produtos.getAllProduto()
    prod =  str(request.form['prod'])
    metragem = int(request.form['metragem'])
    for produto in produtos:
        if produto.nome == prod:
            preco = produto.preco*metragem
            preco=locale.currency(preco, grouping=True) 
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
            flash('Fornecedor '+formNome+' cadastrado com Sucesso')
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
        complemento= str(request.form['Complemento'])
        cidade= str(request.form['Cidade'])
        estado= str(request.form['Estado'])
        cep= str(request.form['CEP'])
        try:
            tables.Cliente.insertCliente(formNome,formCpf,formTelefone,formEndereco,cidade,estado,complemento,cep)
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
    
@app.route("/produto/cadastrar/", methods=["GET","POST"])
def Cadastrar_produto():    
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
                    precomoeda = str(locale.currency(linha[2], grouping=True)).replace("R$","").strip(" ")
                    fornecedor = tables.Fornecedor.getFornecedor(linha[4])
                    prod.append([linha,precomoeda,fornecedor.nome])   
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
    print("aqui foi")   
    return render_template('produto.html',ProdutoForm=form,cadastrar=False,produtos=tables.Produtos.getAllProduto())



@app.route("/cliente/", methods=["GET","POST"])
def Pesquisar_cliente():
    form = forms.ClienteForm()
    try:
        if form.validate_on_submit():
            formCpf = str(form.cpf.data)
            client=tables.Cliente.getCliente(formCpf)
            print(client)
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
                    return jsonify({"CPF":cliente.CPF,"nome":cliente.nome,"telefone":cliente.telefone,"Endereco":cliente.Endereco,"Cidade":cliente.Cidade,"Estado":cliente.Estado,"Complemento":cliente.Complemento,"CEP":cliente.CEP})
            return jsonify({"CPF":"Não cadastrado"})
    except:
        return render_template('cliente.html',ClienteForm=form,cadastrar=False,clientes=tables.Cliente.getAllCliente())
    return render_template('cliente.html',ClienteForm=form,cadastrar=False,clientes=tables.Cliente.getAllCliente())
    
@app.route("/cliente/atualizar/<cpf>", methods=["GET","POST"])
def atualizar_cliente(cpf):
    form = forms.ClienteForm(request.form)
    try:
        if request.method == 'POST':
            formNome= str(request.form['cliente'])
            formCpf = str(request.form['cpf'])
            formTelefone = str(request.form["telefone"])
            formEndereco = str(request.form['endereco'])
            complemento= str(request.form['Complemento'])
            cidade= str(request.form['Cidade'])
            estado= str(request.form['Estado'])
            cep= str(request.form['CEP'])
            tables.Cliente.setCliente(formNome,formCpf,formTelefone,formEndereco,cidade,estado,complemento,cep)
            flash('Cliente '+formNome+' atualizado com sucesso')
            return redirect(url_for('Pesquisar_cliente'))
    except:
        flash('Falaha ao atualizar cliente '+formNome+' tente novamente')
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

@app.route("/orcamento/cadastrar/", methods=["GET","POST"])
def Cadastrar_Orcamento():
    if request.method == 'POST':
        dados = request.get_json()
        total = dados["Total"].replace(".","")
        total = float(total.replace(",","."))
        data = date.today()
        dataEntrega = int(dados["DiasEntrega"])
        Status = "Aguardando"
        print(dataEntrega)
        #data=data.strftime("%d/%m/%y")
        try:
            codigoGerado = tables.Orcamento.insertOrcamento(total,data,dataEntrega,Status)
            print("aqui foi")
            print(codigoGerado)
            if(codigoGerado!=""):
                condId = int(codigoGerado)
                print(total)
                for produto in dados["nomeProduto"]:
                    idProduto = tables.Produtos.getProdutoID(produto)
                    print(idProduto.id)
                    print(condId)
                    tables.Orcamento_Produto.insertOrcamentoProduto(condId,idProduto.id)
            
                return jsonify({"Resultado":"Susess","codigoOrcamento":codigoGerado})
        
        except:
            return jsonify({"Resultado":"Error"}) 
    return jsonify({"Resultado":"Error"}) 

@app.route("/relatorio/<lista>",methods=["GET","POST"])
@app.route("/relatorio/",methods=["GET","POST"],defaults={"lista":None})
def relatorio(lista):
    print("entrou no relatorio")
    with sqlite3.connect('storage.db') as conn:
        try:
            cur = conn.cursor()
            if request.method == 'POST':
                if request.form['acao']=="pesquisar":
                    print("tipo de ralatorio")
                    tipo = str(request.form['tipoRelatorio'])
                    return jsonify({"Tipo":tipo})
                tipo = request.form['tipo']
                datainicial= request.form['DataInicial']
                datafinal = request.form['DataFinal']
                print(datafinal)
                print(datainicial)
                if tipo == "Pedido":
                    CPF = request.form['cpf'].strip(" ")
                    print(CPF)
                    if CPF == "":
                        itens = []
                        print("sem cpf")
                        cur.execute('SELECT * FROM Pedido where data >=? and data <= ?',(datainicial,datafinal, ))
                        relatorio=cur.fetchall()
                        for linha in relatorio: 
                            precomoeda = str(locale.currency(linha[4], grouping=True)).replace("R$","").strip(" ")
                            orcamento = tables.Orcamento.getOrcamento(linha[1])
                            for linhaentrega in orcamento:
                                entrega = int(linhaentrega.prazoEntrega)
                            datafim = linha[3].replace("-","/")
                            datafim = datetime.strptime(datafim, '%Y/%m/%d').date()
                            datafim =date.fromordinal(datafim.toordinal()+entrega)
                            datafim = datafim.strftime("%d/%m/%Y")
                            data = linha[3].replace("-","/")
                            print(data)
                            data = datetime.strptime(data, '%Y/%m/%d').date()
                            print(data)
                            data = data.strftime("%d/%m/%Y")
                            print("data sem cpf")
                            print(data)
                            itens.append([linha,datafim,data,precomoeda])
                        print(itens)
                        conn.commit()
                        print(itens)
                    else:
                        itens = []
                        cur.execute('SELECT * FROM Pedido where cliente_cpf = ? and data >=? and data <= ?',(CPF,datainicial,datafinal, ))
                        relatorio=cur.fetchall()
                        for linha in relatorio: 
                            precomoeda = str(locale.currency(linha[4], grouping=True)).replace("R$","").strip(" ")
                            orcamento = tables.Orcamento.getOrcamento(linha[1])
                            for linhaentrega in orcamento:
                                entrega = int(linhaentrega.prazoEntrega)
                            datafim = linha[3].replace("-","/")
                            datafim = datetime.strptime(datafim, '%Y/%m/%d').date()
                            datafim =date.fromordinal(datafim.toordinal()+entrega)
                            datafim = datafim.strftime("%d/%m/%Y")
                            data = linha[3].replace("-","/")
                            print(data)
                            data = datetime.strptime(data, '%Y/%m/%d').date()
                            print(data)
                            data = data.strftime("%d/%m/%Y")
                            print("data foi")
                            print(data)
                            itens.append([linha,datafim,data,precomoeda])
                        conn.commit()
                    return render_template("RelatorioPedidos.html", pedidos = itens)
                if tipo == "Orçamento":
                    itens = []
                    cur.execute('SELECT * FROM Orcamento where data >=? and data <= ?',(datainicial,datafinal, ))
                    relatorio=cur.fetchall()
                    for linha in relatorio: 
                        precomoeda = str(locale.currency(linha[1], grouping=True)).replace("R$","").strip(" ")
                        datafim = linha[2].replace("-","/")
                        datafim = datetime.strptime(datafim, '%Y/%m/%d').date()
                        datafim =date.fromordinal(datafim.toordinal()+15)
                        datafim = datafim.strftime("%d/%m/%Y")
                        data = linha[2].replace("-","/")
                        data = datetime.strptime(data, '%Y/%m/%d').date()
                        data = data.strftime("%d/%m/%Y")
                        itens.append([linha,datafim,data,precomoeda])
                        conn.commit()
                    return render_template("RelatorioOrcamento.html", orcamentos = itens)
        except:
            flash("Erro ao gerar relatório")
            return redirect(url_for('RelatorioPesquisar'))
    
@app.route("/Relatorio/Pesquisar/")
def RelatorioPesquisar():
   
    return render_template("RelatorioPesquisar.html")
@app.route("/imprimir/orcamento/<codigoOrcamento>", methods=["GET","POST"])
def imprimirOrcamento(codigoOrcamento):
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
            print(data)
            print(datafim)
        if codigoOrcamento:
            if orcamento:
                produtos = []
                codProduto = tables.Orcamento_Produto.getOrcamentoProduto(codigoOrcamento)
                for cod in codProduto:
                    produtos.append(tables.Produtos.getProdutoID(cod.Produto_id))
                print(produtos)
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

@app.route("/Pedido/<codigoOrcamento>", methods=["GET","POST"])
@app.route("/Pedido/", methods=["GET","POST"],defaults={"codigoOrcamento":None})

def Pedido(codigoOrcamento):
   
    try:
        orcamento = tables.Orcamento.getOrcamento(codigoOrcamento)
        for precoOrcamento in orcamento:
            precoatual = locale.currency(precoOrcamento.preco, grouping=True)
            preco = locale.currency(precoOrcamento.preco, grouping=True).replace("R$","").strip(" ")
            print(preco)
        if codigoOrcamento:
            if orcamento:
                produtos = []
                codProduto = tables.Orcamento_Produto.getOrcamentoProduto(codigoOrcamento)
                for cod in codProduto:
                    produtos.append(tables.Produtos.getProdutoID(cod.Produto_id))
                print(produtos)
                return render_template("Pedido.html",cart=produtos,precoOrcamento=precoatual,orcamento=preco,codigoOrcamento=codigoOrcamento,codigo=True)
            return redirect(url_for('Orcamento'))
        return render_template("Pedido.html")   
    except:
        return render_template("Pedido.html")

@app.route("/Pedido/cadastrar/", methods=["GET","POST"])
def CadastrarPedido():
    print("aqui foi")
    if request.method == 'POST':
        formNome= str(request.form['Nome'])
        valor= str(request.form['dinheiro'])
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
                print("cliente vazio")
                tables.Cliente.insertCliente(formNome,cpf,telefone,endereco,cidade,estado,complemento,cep)
            orcamento = tables.Orcamento.getOrcamento(codigoOrcamento)
            Status="Aprovado"
            for dataorcamento in orcamento:
                data = dataorcamento.data
                datamaxima = date.fromordinal(data.toordinal()+15)
                print(datamaxima)
                print(date.today())
            if date.today()>datamaxima:

                flash("Orçamento "+str(codigoOrcamento)+" Está com mais de 15 dias após gerado")
                return render_template("Pedido.html")

            pedido = tables.Pedido.getPedidobyOrcamento(codigoOrcamento)
            if pedido:
                print("pedido colocado")
                flash("Orçamento "+str(codigoOrcamento)+" já foi utilizado em outro pedido")
                return render_template("Pedido.html")
            print("não tem pedido")
            print()
            tables.Pedido.cadastrarPedido(codigoOrcamento,cpf,data,valor)
            flash("Pedido realizado com Sucesso")
            orcamento = tables.Orcamento.setStatusOrcamento(codigoOrcamento,Status)
            return render_template("Pedido.html")
        except:
            flash("Falha ao gerar pedido tente novamente")
            return render_template("Pedido.html")

    return render_template("Pedido.html")
