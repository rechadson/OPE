from app.Models import Alunos,Resposta
from app import db
from flask import request
from app.Services import Listar

def CadastrarAluno():
    dados = request.get_json()
    RA = dados["RA"]
    Nome = dados["Nome"]
    Ativo = dados["Ativo"]
    aluno = Alunos.Alunos(Nome,RA,Ativo)
    db.session.add(aluno)
    db.session.commit()
    
    Resposta.resposta["Status"] = "Sucesso"
    Resposta.resposta["Mensagem"] = "Alunos cadastrado."
    Resposta.resposta["Dados"] = Nome
    return Resposta.resposta