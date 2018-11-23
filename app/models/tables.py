from app import db
from datetime import datetime

class Produtos(db.Model):
    __tablename__ = "produtos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    preco = db.Column(db.Float(120), nullable=False)
    fornecedor_id = db.Column(db.Integer,db.ForeignKey('fornecedores.id'))
    fornecedor = db.relationship('Fornecedor',foreign_keys=fornecedor_id)
    def __init__(self,nome,preco,fornecedor_id):
        self.nome = nome
        self.preco = preco
        self.fornecedor_id = fornecedor_id

    def __repr__(self):
        return '<User %r>' % self.nome

class Clinte(db.Model):
    __tablename__ = "clientes"
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
    __tablename__ = "orcamentos"
    id = db.Column(db.Integer, primary_key=True)
    preco = db.Column(db.Float(120), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    produto_id = db.Column(db.Integer,db.ForeignKey('produtos.id'))
    produto = db.relationship('Produtos',foreign_keys=produto_id)
    cliente_cpf = db.Column(db.Integer,db.ForeignKey('clientes.CPF'))
    cliente = db.relationship('Clinte',foreign_keys=cliente_cpf)

    def __init__(self,produto_id,cliente_cpf,preco,data):
        self.preco = preco
        self.data = data
        self.produto_id = produto_id
        self.cliente_cpf = cliente_cpf

    def __repr__(self):
        return '<Orcamento %r>' % self.id

class Pedido(db.Model):
    __tablename__ = "pedidos"
    id = db.Column(db.Integer, primary_key=True)
    orcamento_id = db.Column(db.Integer,db.ForeignKey('orcamentos.id'))
    orcamento = db.relationship('Orcamento',foreign_keys=orcamento_id)

    def __init__(self,orcamento_id):        
        self.orcamento_id = orcamento_id

    def __repr__(self):
        return '<User %r>' % self.username

class Fornecedor(db.Model):
    __tablename__ = "fornecedores"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self,nome,email,telefone):
        self.nome = nome
        self.email = email
        

    def __repr__(self):
        return '<User %r>' % self.username
class Usuario(db.Model):
    __tablename__ = "Usuario"
    id = db.Column(db.Integer, primary_key=True)
    User = db.Column(db.String(20),unique=True, nullable=False)
    Senha = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self,User,Senha):
        self.User = User
        self.Senha = Senha
        

    def __repr__(self):
        return '<User %r>' % self.User