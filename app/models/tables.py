from app import db
from datetime import datetime
import sqlite3
import locale

locale.setlocale(locale.LC_ALL,'')
class Produtos(db.Model):
    __tablename__ = "Produtos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    preco = db.Column(db.Float(120), nullable=False)
    metragem = db.Column(db.Boolean())
    fornecedor_cnpj = db.Column(db.String,db.ForeignKey('Fornecedor.cnpj'))
    fornecedor = db.relationship('Fornecedor',foreign_keys=fornecedor_cnpj)
    def __init__(self,nome,preco,metragem,fornecedor_cnpj):
        self.nome = nome
        self.preco = preco
        self.metragem = metragem
        self.fornecedor_cnpj = fornecedor_cnpj
        
    def insertProduto(nome,preco,metragem,fornecedor_cnpj):
        fornecedor = Fornecedor.query.filter_by(cnpj = fornecedor_cnpj).first()
        if fornecedor:
            inserir = Produtos(nome,preco,metragem,fornecedor_cnpj)
            db.session.add(inserir)
            db.session.commit()
            return True
        return False
    def getAllProduto():
        produto = Produtos.query.all()
       
        return produto
    
    def setProduto(id,nome,preco,metragem,fornecedor_cnpj):
        produto = Produtos.query.filter_by(id = id).first()
        print(produto)
        produto.nome = nome
        produto.preco = preco
        produto.fornecedor_cnpj = fornecedor_cnpj
        produto.metragem = metragem
        db.session.commit()
    def getProdutoByFornecedor(fornecedor_cnpj):
        produto = Produtos.query.filter_by(fornecedor_cnpj = fornecedor_cnpj).all()
        return produto
    def getProduto(nome):
        produto = Produtos.query.filter_by(nome = nome).all() 
        return produto
    def getProdutoID(id):
        produto = Produtos.query.filter_by(id = id).first()
        return produto

class Cliente(db.Model):
    __tablename__ = "Cliente"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    CPF = db.Column(db.String(80),unique=True, nullable=False)
    telefone = db.Column(db.String(80), nullable=False)
    Endereco = db.Column(db.String(80), nullable=False)
    Cidade = db.Column(db.String(80), nullable=False)
    Estado = db.Column(db.String(80), nullable=False)
    Complemento = db.Column(db.String(80))
    CEP = db.Column(db.String(80))
    def __init__(self,nome,CPF,telefone,Endereco,Cidade,Estado,Complemento,CEP):
        self.nome = nome
        self.CPF = CPF
        self.telefone = telefone
        self.Endereco = Endereco
        self.Cidade = Cidade
        self.Estado = Estado
        self.Complemento = Complemento
        self.CEP = CEP
    def insertCliente(nome,CPF,telefone,Endereco,Cidade,Estado,Complemento,CEP):
        print("aqui foi cliente")
        inserir = Cliente(nome,CPF,telefone,Endereco,Cidade,Estado,Complemento,CEP)
        db.session.add(inserir)
        print("aqui inserindo cliente")
        db.session.commit()

    def getAllCliente():
        cliente = Cliente.query.all()
        print(cliente)
        return cliente

    def setCliente(nome,CPF,telefone,Endereco,Cidade,Estado,Complemento,CEP):
        cliente = Cliente.query.filter_by(CPF = CPF).first()
        cliente.nome = nome
        cliente.telefone = telefone
        cliente.Cidade = Cidade
        cliente.Estado = Estado
        cliente.Complemento = Complemento
        cliente.CEP = CEP
        db.session.commit()

    def getCliente(CPF):
        cliente = Cliente.query.filter_by(CPF = CPF).all()
        return cliente

    def __repr__(self):
        return '<Clinte %r>' % self.nome

class Orcamento(db.Model):
    __tablename__ = "Orcamento"
    id = db.Column(db.Integer, primary_key=True)
    preco = db.Column(db.Float(120), nullable=False)
    data = db.Column(db.Date)
    prazoEntrega = db.Column(db.Integer)

    def __init__(self,preco,data,prazoEntrega):
        self.preco = preco
        self.data = data
        self.prazoEntrega = prazoEntrega
    def getAllorcamento():
        orcamento = Orcamento.query.all()
        return orcamento

    def getOrcamento(id):
        orcamento = Orcamento.query.filter_by(id = id).all()
        return orcamento
    def getUltimoOrcamento():
        orcamento = Orcamento.query.all()
        return orcamento[-1].id
    def insertOrcamento(preco,data,prazoEntrega):
        inserir = Orcamento(preco,data,prazoEntrega)
        print("inserindo orçamento")
        print(inserir)
        db.session.add(inserir)
        db.session.commit()
        print("codigo sendo gerado")
        codigogerado = Orcamento.getUltimoOrcamento()
        return codigogerado

class Orcamento_Produto(db.Model):
    __tablename__ = "Orcamento_Produto"
    id = db.Column(db.Integer, primary_key=True)
    orcamento_id = db.Column(db.Integer,db.ForeignKey('Orcamento.id'))
    orcamento = db.relationship('Orcamento',foreign_keys=orcamento_id)
    Produto_id = db.Column(db.Integer,db.ForeignKey('Produtos.id'))
    produto = db.relationship('Produtos',foreign_keys=Produto_id)
    
    def __init__(self,orcamento_id,Produto_id):        
        self.orcamento_id = orcamento_id
        self.Produto_id = Produto_id

    def getOrcamentoProduto(orcamento_id):
        orcamento = Orcamento_Produto.query.filter_by(orcamento_id = orcamento_id).all()
        return orcamento
    def getOrcamentoByProduto(Produto_id):
        print("chegou")
        orcamento = Orcamento_Produto.query.filter_by(Produto_id = Produto_id).all()
        return orcamento
    def insertOrcamentoProduto(orcamento_id,Produto_id):
        inserir = Orcamento_Produto(orcamento_id,Produto_id)
        print(inserir)
        db.session.add(inserir)
        db.session.commit()
   

class Pedido(db.Model):
    __tablename__ = "Pedido"
    id = db.Column(db.Integer, primary_key=True)
    orcamento_id = db.Column(db.Integer,db.ForeignKey('Orcamento.id'))
    orcamento = db.relationship('Orcamento',foreign_keys=orcamento_id)
    cliente_cpf = db.Column(db.String,db.ForeignKey('Cliente.CPF'))
    cliente = db.relationship('Cliente',foreign_keys=cliente_cpf)
    data = db.Column(db.Date)
    valor = db.Column(db.Float)

    def __init__(self,orcamento_id,cliente_cpf,data,valor):        
        self.orcamento_id = orcamento_id
        self.cliente_cpf = cliente_cpf
        self.data = data
        self.valor = valor
    
    def cadastrarPedido(orcamento_id,cliente_cpf,data,valor):
        print("inserindo pedido")
        print(orcamento_id)
        print(cliente_cpf)
        print(data)
        inserir = Pedido(orcamento_id,cliente_cpf,data,valor)
        db.session.add(inserir)
        print("pedido inserido")
        db.session.commit()

    def getPedidobyOrcamento(orcamento_id):
        pedido = Pedido.query.filter_by(orcamento_id = orcamento_id).first()
        return pedido

    def getPedidobycliente(cliente_cpf):
        pedido = Pedido.query.filter_by(cliente_cpf = cliente_cpf).first()
        return pedido
    


class Fornecedor(db.Model):
    __tablename__ = "Fornecedor"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cnpj = db.Column(db.String,unique=True, nullable=False)

    def __init__(self,nome,email,cnpj):
        self.nome = nome
        self.email = email
        self.cnpj = cnpj

    def getAllFornecedor():
        fornecedor = Fornecedor.query.all()
        return fornecedor
    def getFornecedor(cnpj):
        fornecedor = Fornecedor.query.filter_by(cnpj = cnpj).first()
        return fornecedor
    def getFornecedorByNome(nome):
        fornecedor = Fornecedor.query.filter_by(nome = nome).all()
        return fornecedor
    def insertFornecedor(nome,email,cnpj):
        print("tentando")
        inserir = Fornecedor(nome,email,cnpj)
        print(inserir)
        db.session.add(inserir)
        db.session.commit()
        
    def setFornecedor(nome,email,cnpj):
        fornecedor = Fornecedor.query.filter_by(cnpj = cnpj).first()
        fornecedor.nome = nome
        fornecedor.email = email
        db.session.commit()
    
class Usuario(db.Model):
    __tablename__ = "Usuario"
    id = db.Column(db.Integer, primary_key=True)
    User = db.Column(db.String(20),unique=True, nullable=False)
    Senha = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self,User,Senha):
        self.User = User
        self.Senha = Senha
        
    def getUser(User):
        user = Usuario.query.filter_by(User = User).first()
        
        return user

    def getSenha(Senha):
        senha = Usuario.query.filter_by(Senha = Senha).first()
        
        return senha
