from app import db
from datetime import datetime

class Produtos(db.Model):
    __tablename__ = "Produtos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    preco = db.Column(db.Float(120), nullable=False)
    fornecedor_id = db.Column(db.Integer,db.ForeignKey('Fornecedor.id'))
    fornecedor = db.relationship('Fornecedor',foreign_keys=fornecedor_id)
    def __init__(self,nome,preco,fornecedor_id):
        self.nome = nome
        self.preco = preco
        self.fornecedor_id = fornecedor_id
    def getProduto(id):
        produto = Produtos.query.filter_by(id = id).all()
        return produto

    def getAllProduto():
        produto = Produtos.query.all()
        return produto

    def __repr__(self):
        return '<User %r>' % self.nome

class Clinte(db.Model):
    __tablename__ = "Clinte"
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

    def __repr__(self):
        return '<Clinte %r>' % self.nome

class Orcamento(db.Model):
    __tablename__ = "Orcamento"
    id = db.Column(db.Integer, primary_key=True)
    preco = db.Column(db.Float(120), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    produto_id = db.Column(db.Integer,db.ForeignKey('Produtos.id'))
    produto = db.relationship('Produtos',foreign_keys=produto_id)
    cliente_cpf = db.Column(db.Integer,db.ForeignKey('Clinte.CPF'))
    cliente = db.relationship('Clinte',foreign_keys=cliente_cpf)

    def __init__(self,produto_id,cliente_cpf,preco,data):
        self.preco = preco
        self.data = data
        self.produto_id = produto_id
        self.cliente_cpf = cliente_cpf

    def __repr__(self):
        return '<Orcamento %r>' % self.id

class Pedido(db.Model):
    __tablename__ = "Pedido"
    id = db.Column(db.Integer, primary_key=True)
    orcamento_id = db.Column(db.Integer,db.ForeignKey('Orcamento.id'))
    orcamento = db.relationship('Orcamento',foreign_keys=orcamento_id)

    def __init__(self,orcamento_id):        
        self.orcamento_id = orcamento_id

    def __repr__(self):
        return '<User %r>' % self.username

class Fornecedor(db.Model):
    __tablename__ = "Fornecedor"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cnpj = db.Column(db.Integer,unique=True, nullable=False)

    def __init__(self,nome,email,cnpj):
        self.nome = nome
        self.email = email
        self.cnpj = cnpj

    def getAllFornecedor():
        fornecedor = Fornecedor.query.all()
        print(fornecedor)
        return fornecedor

    def getFornecedor(cnpj):
        fornecedor = Fornecedor.query.filter_by(cnpj = cnpj).first()
        return fornecedor
    
    def insertFornecedor(nome,email,cnpj):
        inserir = Fornecedor(nome,email,cnpj)
        db.session.add(inserir)
        db.session.commit()
    def setFornecedor(nome,email,cnpj):
        fornecedor = Fornecedor.query.filter_by(cnpj = cnpj).first()
        fornecedor.nome = nome
        fornecedor.email = email
        db.session.commit()
    def __repr__(self):
        return '<User %r>' % self.nome
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

    