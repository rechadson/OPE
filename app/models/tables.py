from app import db
from datetime import datetime
import sqlite3

class Produtos(db.Model):
    __tablename__ = "Produtos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    preco = db.Column(db.Float(120), nullable=False)
    categoria_id = db.Column(db.Integer,db.ForeignKey('CategoriaProduto.id'))
    categoria = db.relationship('CategoriaProduto',foreign_keys=categoria_id)
    fornecedor_cnpj = db.Column(db.String,db.ForeignKey('Fornecedor.cnpj'))
    fornecedor = db.relationship('Fornecedor',foreign_keys=fornecedor_cnpj)
    def __init__(self,nome,preco,fornecedor_cnpj,Categoria):
        self.nome = nome
        self.preco = preco
        self.fornecedor_cnpj = fornecedor_cnpj
        self.Categoria = Categoria
    def insertProduto(nome,preco,fornecedor_cnpj,Categoria):
        print(fornecedor_cnpj)
        fornecedor = Fornecedor.query.filter_by(cnpj = fornecedor_cnpj).all()
        if fornecedor:
            inserir = Produtos(nome,preco,fornecedor_cnpj,Categoria)
            db.session.add(inserir)
            db.session.commit()
            return True
        return False
    def getAllProduto():
        produto = Produtos.query.all()
       
        return produto
    
    def setProduto(nome,preco,fornecedor_cnpj,Categoria):
        produto = Produtos.query.filter_by(nome = nome).first()
        produto.nome = nome
        produto.preco = preco
        produto.fornecedor_cnpj = fornecedor_cnpj
        produto.Categoria = Categoria
        db.session.commit()
    def getProdutoByFornecedor(fornecedor_cnpj):
        produto = Produtos.query.filter_by(fornecedor_cnpj = fornecedor_cnpj).all()
        return produto
    def getProduto(nome):
        produto = Produtos.query.filter_by(nome = nome).all()
        return produto
    def getProdutoID(id):
        
        produto = Produtos.query.filter_by(id = id).all()
        print(produto)
        return produto
    

    def __repr__(self):
        return '<User %r>' % self.nome

class Cliente(db.Model):
    __tablename__ = "Cliente"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    CPF = db.Column(db.String(80),unique=True, nullable=False)
    telefone = db.Column(db.String(80), nullable=False)
    Endereco = db.Column(db.String(80), nullable=False)
    def __init__(self,nome,CPF,telefone,Endereco):
        self.nome = nome
        self.CPF = CPF
        self.telefone = telefone
        self.Endereco = Endereco

    def insertCliente(nome,CPF,telefone,endereco):
        inserir = Cliente(nome,CPF,telefone,endereco)
        db.session.add(inserir)
        db.session.commit()

    def getAllCliente():
        cliente = Cliente.query.all()
        print(cliente)
        return cliente

    def setCliente(nome,CPF,telefone,endereco):
        cliente = Cliente.query.filter_by(CPF = CPF).first()
        cliente.nome = nome
        cliente.telefone = telefone
        cliente.endereco = endereco
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
    

    def __init__(self,preco,data):
        self.preco = preco
        self.data = data
    def getAllorcamento():
        orcamento = Orcamento.query.all()
        return orcamento

    def getOrcamento(id):
        orcamento = Orcamento.query.filter_by(id = id).all()
        return orcamento
    def getUltimoOrcamento():
        orcamento = Orcamento.query.all()
        return orcamento[-1].id
    def insertOrcamento(preco,data):
        inserir = Orcamento(preco,data)
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

    def __init__(self,orcamento_id):        
        self.orcamento_id = orcamento_id

    def __repr__(self):
        return '<User %r>' % self.username

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
        fornecedor = Fornecedor.query.filter_by(cnpj = cnpj).all()
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

class CategoriaProduto(db.Model):
    __tablename__ = "CategoriaProduto"
    id = db.Column(db.Integer, primary_key=True)
    Categoria = db.Column(db.String(20),unique=True, nullable=False)
    CalcularMetragem = db.Column(db.Boolean())

    def __init__(self,Categoria,CalcularMetragem):
        self.Categoria = Categoria
        self.CalcularMetragem = CalcularMetragem
        
    def getCategoriaByname(Categoria):
        categoria = CategoriaProduto.query.filter_by(Categoria = Categoria).first()
        
        return categoria
    def getCategoria():
        categoria = CategoriaProduto.query.all()
        
        return categoria
    def insertCategoria(Categoria,CalcularMetragem):
        print("tentando")
        inserir = CategoriaProduto(Categoria,CalcularMetragem)
        print(inserir)
        db.session.add(inserir)
        db.session.commit()

    