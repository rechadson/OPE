$(function()
{      
    var scntDiv = $('#Relatorio');
$('#tipoRelatorio').change(function() {
    
    $.ajax({
    url: '/relatorio/',
    data: $('#formtiporelatorio').serialize(),
    type: 'POST',
    success: function(response) {
        console.log(scntDiv)
        if(response.Tipo == "Pedido"){
            $('#formularioRelatorio').remove()
            $('<form id="formularioRelatorio" action="../../relatorio/" METHOD="POST">'+
            '<div class="form-group col-md-3">'+
              '<label for="DataInicial">Data Inicial</label>'+
              '<input type="date" class="form-control" id="DataInicial" name="DataInicial"placeholder="Digite a Data" autofocus required>'+
            '</div>'+
            '<div class="form-group col-md-3">'+
              '<label for="DataFinal">Data Final</label>'+
              '<input type="date" class="form-control" id="DataFinal" name="DataFinal"placeholder="Digite a Data" autofocus required>'+
            '</div>'+
          '<div class="form-group col-md-6">'+
              '<label for="cpf">CPF do Cliente</label>'+
              '<input type="text" class="form-control" id="cpf"placeholder="Digite o CPF do cliente..." name="cpf">'+
          '</div>'+
          '<div class="form-group col-md-6">'+
              '<label for="Nome">Nome Do Produto</label>'+
              '<input type="text" class="form-control" id="Nome" placeholder="Digite o nome do produto..." name="produto">'+
          '</div>'+
          '<div class="form-group col-md-6">'+
            '<button class="btn btn-primary" id="gerarRelatorio">Gerar Relatório</button>'+
          '</div>'+
              '<input type="text" class="form-control invisible" id="tipo" name="tipo"value="Pedido">'+
              '<input type="text" class="form-control invisible" id="Nome" name="acao"value="gerar">'+
        '</form>').appendTo(scntDiv);
    }
    if(response.Tipo == "Orçamento"){
         $('#formularioRelatorio').remove()
        $('<form id="formularioRelatorio" action="../../relatorio/" METHOD="POST">'+
        '<div class="form-group col-md-3">'+
          '<label for="DataInicial">Data Inicial</label>'+
          '<input type="date" class="form-control" id="DataInicial" name="DataInicial"placeholder="Digite a Data" autofocus required>'+
        '</div>'+
        '<div class="form-group col-md-3">'+
          '<label for="DataFinal">Data Final</label>'+
          '<input type="date" class="form-control" id="DataFinal" name="DataFinal"placeholder="Digite a Data" autofocus required>'+
        '</div>'+
      '<div class="form-group col-md-6">'+
      '<button class="btn btn-primary" id="gerarRelatorio">Gerar Relatório</button>'+
      '</div>'+
      '<input type="text" class="form-control invisible" id="tipo" name="tipo"value="Orçamento">'+
      '<input type="text" class="form-control invisible" id="Nome" name="acao"value="gerar">'+
    '</form>').appendTo(scntDiv);
        
    }
    },
    error: function(error) {
        console.log(error);
    }
    });
});
$(document).on('click', '#gerarRelatorio', function () {
  $('#formularioRelatorio').submit();
});
});
