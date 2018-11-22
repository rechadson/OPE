from app.Models import Alunos,Resposta
import json




def ListarAlunos():
    Aluno = Alunos.Alunos.query.all()
    Resposta.resposta["Status"] = "Sucesso"
    Resposta.resposta["Mensagem"] = ""
    lista = []
    for aluno in Aluno:
        alunos = {"nome":aluno.nome,"RA":aluno.RA,"Ativo":aluno.Ativo}
        lista.append(alunos)
    Resposta.resposta["Dados"] = lista   
    print(Resposta.resposta)
    
    return Resposta.resposta
