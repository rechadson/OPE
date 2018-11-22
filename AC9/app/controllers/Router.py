from flask import jsonify
from flask import request
from app.Services import Delete,Insert,Listar,ListarRa,Update
from app import app



@app.route("/Alunos/atualizar", methods=["PUT"])
def atualizar():

    return jsonify(Update.AtualizarAlunos())

@app.route("/Alunos", methods=["GET"])
def listar():
        
    return jsonify(Listar.ListarAlunos())

@app.route("/Alunos/<RA>", methods=["GET"])
def listarRA(RA):
    
    return jsonify(ListarRa.ConsultarAlunos(RA))

@app.route("/Alunos/cadastrar", methods=["POST"])
def inserir():
    
    return jsonify(Insert.CadastrarAluno())

@app.route("/Alunos/excluir/<RA>", methods=["DELETE"])
def excluir(RA):
    return jsonify(Delete.ExcluirAlunos(RA))