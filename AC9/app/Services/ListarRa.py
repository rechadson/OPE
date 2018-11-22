from app.Models import Alunos,Resposta

def ConsultarAlunos(RA):
    Aluno = Alunos.Alunos.query.all()
    print(RA)
    lista = []
    
    if len(Aluno) !=0:
        for P in Aluno:
            print(P.RA , RA)
            if P.RA == int(RA):
               
                Resposta.resposta["Status"] = "Sucesso"
                Resposta.resposta["Mensagem"] = ""
                alunos = {"nome":P.nome,"RA":P.RA,"Ativo":P.Ativo}
                lista.append(alunos)
                Resposta.resposta["Dados"] = lista
                return Resposta.resposta
            Resposta.resposta["Status"] = "Falha"
            Resposta.resposta["Mensagem"] = "Aluno não encontrado"
            Resposta.resposta["Dados"] = None
    else:
        Resposta.resposta["Status"] = "Falha"
        Resposta.resposta["Mensagem"] = "Não Há alunos cadastrado"
        Resposta.resposta["Dados"] = None
    return Resposta.resposta