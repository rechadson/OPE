from app import db

class Alunos(db.Model):
    __tablename__ = "Alunos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    RA = db.Column(db.Integer, nullable=False)
    Ativo = db.Column(db.String(80), nullable=False)
    def __init__(self,nome,RA,Ativo):
        self.nome = nome
        self.RA = RA
        self.Ativo = Ativo

    
