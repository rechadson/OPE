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
'<h6 class="my-0">'+response.nome+'</h6>'+
'<small class="nomeProduto" name="nome_Produto" id="nome_Produto">'+response.nome+'</small>'+
'</div>'+
'<span class="precoprod">'+response.preco+'</span>'+
'<a class="btn btn-danger" href="javascript:void(0)" id="remInput">'+
				'<span class="glyphicon glyphicon-minus" aria-hidden="true"></span> '+
				'Remover produto'+
	'</a>'+'</li>').appendTo(scntDiv);

    carrinhos.each(function(){
        var carrinhoAtual = $(this);
        var valorItem = carrinhoAtual.find('.precoprod');
        var resultado = 0;

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
			var resultado = 0;

			valorItem.each(function(){
				var tdAtual = $(this);
				var pegaValor = parseFloat(tdAtual.text());
				resultado = parseFloat(resultado + pegaValor);
			});

			$('#total').text(resultado);

		});
		return false;
	});
	$(document).on('click', '#gerar', function () {
		var json = {};
		json["CPF"]=$('#CPF').val();
		
		json["nomeProduto"] = ListarProdutos();
		json["Total"]=$('#total').text();
		function ListarProdutos(){
            var produto= Array();
			var produtos = $('#cart');
			console.log(produtos);
            produtos.each(function(){
				var nomePrd = $(this).find('.nomeProduto')
				console.log(nomePrd);
				nomePrd.each(function(){
					produto.push($(this).text())
					console.log(produto);
				});
			});
			return produto;
            
            
		}	
		console.log(json);
		$.ajax({
			url: '/orcamento/cadastrar/',
			type: 'POST',
			dataType: 'json',
			data: JSON.stringify(json),
            contentType: "application/json; charset=utf-8",
			success: function(response) {
				if(response.Resultado == "Susess")
				{
						$('.produto > *').remove();
						$('#total').text("R$ 0");
						window.location.replace("../Pedido/"+response.codigoOrcamento);
						alert('Orçamento Gerado com Sucesso')
						
				}
				if(response.Resultado == "Cliente")
				{
					window.location.replace("../cliente/cadastrar/");
					alert('Cliente não cadastrado')
				}
				
			},
			error: function(error) {
				console.log(error);
			}
			});	
				
		return false;
});
	return false;
});


