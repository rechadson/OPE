$(function () {
	var scntDiv = $('.produto');
	var carrinhos = $('.container');
$(document).on('click', '#addInput', function () {
$.ajax({
url: '/adicionar/produto/',
data: $('#formprod').serialize(),
type: 'POST',
success: function(response) {
  $('<li class="list-group-item d-flex justify-content-between lh-condensed">'+
'<div>'+
'<textarea class="nomeproduto form-control" name="nomeProduto" id="nomeproduto" rows="1" readonly="readonly">'+response.nome+'</textarea>'+
'</div>'+
'<span class="precoprod">'+response.preco+'</span>'+
'<a class="btn btn-danger" href="javascript:void(0)" id="remInput">'+
				'<span class="glyphicon glyphicon-minus" aria-hidden="true"></span> '+
				'Remover produto'+
	'</a>'+'</li>').appendTo(scntDiv);
		
    carrinhos.each(function(){
        var carrinhoAtual = $(this);
        var valorItem = carrinhoAtual.find('.precoprod');
        var resultado = 0.0;

        valorItem.each(function(){
            var tdAtual = $(this);
            var pegaValor = parseFloat(tdAtual.text());
            resultado = parseFloat(resultado + pegaValor);
        });

        $('#total').text(resultado);
        
    });
},
error: function(error) {
	console.log(error);
}
});
		return false;
	});
	$(document).on('click', '#remInput', function () {
		$(this).parents('li').remove();
		carrinhos.each(function(){
			var carrinhoAtual = $(this);
			var valorItem = carrinhoAtual.find('.precoprod');
			var resultado = 0.0;
	
			valorItem.each(function(){
				var tdAtual = $(this);
				var pegaValor = parseFloat(tdAtual.text());
				resultado = parseFloat(resultado + pegaValor);
			});
	
			$('#total').text(resultado);
			
		});
		return false;
	});
});
$(document).on('click', '#gerar', function () {
var cont = 0;
$('.needs-validation .nomeproduto').each(function(){
			var cpf = $('CPF').val();
			var nomeproduto = $(this).text();
			cont+=1
			console.log(nomeproduto);
	$.ajax({
		url: '/orcamento/cadastrar/',
		data: $('.needs-validation').serialize(),
		type: 'POST',
		success: function(response) {
			
			console.log(this);
			
		},
		error: function(error) {
			console.log(error);
		}
		});
		$(this).parents('li').remove();
		$('#total').text("0");
			
		
		
});
	
		return false;
});


