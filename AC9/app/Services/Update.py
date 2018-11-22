from app.Models import Alunos,Resposta
from flask import request
from app import db

def AtualizarAlunos():
    dados = request.get_json()
    Aluno = Alunos.Alunos.query.all()
    lista = []
    if len(Aluno) !=0:
        for P in Aluno:
            
            if P.RA == int(dados["RA"]):
                P.nome = dados["Nome"]
                P.Ativo = dados["Ativo"]
                db.session.add(P)
                db.session.commit()
                Resposta.resposta["Status"] = "Sucesso"
                Resposta.resposta["Mensagem"] = "Aluno atualizado."
                alunos = {"nome":P.nome,"RA":P.RA,"Ativo":P.Ativo}
                lista.append(alunos)
                Resposta.resposta["Dados"] = lista
                return Resposta.resposta
        P=None
        Resposta.resposta["Status"] = "falha"
        Resposta.resposta["Mensagem"] = "RA não encontrado"
        Resposta.resposta["Dados"] = P

    return Resposta.resposta