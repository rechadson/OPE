from app.Models import Alunos,Resposta
from app import db

def ExcluirAlunos(RA):    
    Aluno = Alunos.Alunos.query.all()
    lista = []
    if len(Aluno) !=0:
        for P in Aluno:
            
            if P.RA == int(RA):
                db.session.delete(P)
                db.session.commit()
                Resposta.resposta["Status"] = "Sucesso"
                Resposta.resposta["Mensagem"] = "Aluno Deletado com Sucesso."
                alunos = {"nome":P.nome,"RA":P.RA,"Ativo":P.Ativo}
                lista.append(alunos)
                Resposta.resposta["Dados"] = lista
                return Resposta.resposta
            else:
                Resposta.resposta["Status"] = "falha"
                Resposta.resposta["Mensagem"] = "Aluno não encontrado"
                P = None
                Resposta.resposta["Dados"] = P
    

    return Resposta.resposta