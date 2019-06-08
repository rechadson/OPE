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

    def insertProduto(nome,preco,fornecedor_id):
        inserir = Produtos(nome,preco,fornecedor_id)
        db.session.add(inserir)
        db.session.commit()

    def getAllProduto():
        produto = Produtos.query.all()
       
        return produto

    def setProduto(nome,preco,fornecedor_id):
        produto = Produtos.query.filter_by(nome = nome).first()
        produto.nome = nome
        produto.preco = preco
        produto.fornecedor_id = fornecedor_id
        db.session.commit()

    def getProduto(nome):
        produto = Produtos.query.filter_by(nome = nome).all()
        return produto
    def getProdutoID(id):
        produto = Produtos.query.filter_by(id = id).all()
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
    data = db.Column(db.DateTime)
    cliente_cpf = db.Column(db.Integer,db.ForeignKey('Cliente.CPF'))
    cliente = db.relationship('Cliente',foreign_keys=cliente_cpf)

    def __init__(self,preco,cliente_cpf,data):
        self.preco = preco
        self.cliente_cpf = cliente_cpf
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
    def insertOrcamento(preco,cliente_cpf,data):
        inserir = Orcamento(preco,cliente_cpf,data)
        db.session.add(inserir)
        db.session.commit()
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
        produto = Orcamento_Produto.query.filter_by(orcamento_id = orcamento_id).all()
        return produto

    def insertOrcamentoProduto(orcamento_id,Produto_id):
        inserir = Orcamento_Produto(orcamento_id,Produto_id)
        db.session.add(inserir)
        db.session.commit()
   

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
        return fornecedor
    def getFornecedor(cnpj):
        fornecedor = Fornecedor.query.filter_by(cnpj = cnpj).all()
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

    