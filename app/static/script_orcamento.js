$(function () {
	var scntDiv = $('.produto');
	var carrinhos = $('.container');
	
	$('#inlineFormCustomSelect').change(function() {
		$.ajax({
		url: '/metragem/produto/',
		data: $('#formprod').serialize(),
		type: 'POST',
		success: function(response) {
			console.log(response.Metragem)
			if(response.Metragem == "Calcular"){
			$("#Metragem").attr("class", "visible col-md-6 mb-3")	
		}
		if(response.Metragem == "NaoCalcular"){
			$("#metragemitem").val("1")
			$("#Metragem").attr("class", "invisible col-md-6 mb-3")
			
		}
		},
		error: function(error) {
			console.log(error);
		}
		});
	});
$(document).on('click', '#addInput', function () {
$.ajax({
url: '/adicionar/produto/',
data: $('#formprod').serialize(),
type: 'POST',
success: function(response) {
  $('<li class="list-group-item">'+
'<div class="p-2">'+
'<h6 class="my-0">'+response.nome+'</h6>'+
'<small>Codigo do produto: </small>'+
'<small class="nomeProduto" name="nome_Produto" id="nome_Produto">'+response.id+'</small>'+
'</div>'+
'<div class="p-2"><span class="dinheiro">'+response.preco +'</span></div>'+
'<div class="p-2"><a class="btn btn-danger" href="javascript:void(0)" id="remInput">'+
				'<span class="glyphicon glyphicon-minus" aria-hidden="true"></span> '+
				'Remover produto'+
	'</a></div>'+'</li>').appendTo(scntDiv);

    carrinhos.each(function(){
        var carrinhoAtual = $(this);
        var valorItem = carrinhoAtual.find('.dinheiro');
        var resultado = 0;
		var moeda;
		var c;
		var n;
		var d;
		var t;
        valorItem.each(function(){
			var arredondar;
			var tdAtual = $(this).text().replace('R$','');
			tdAtual = tdAtual.replace('.','')
			var pegaValor = parseFloat(tdAtual.replace(',', '.'));		
			resultado = parseFloat(resultado + pegaValor);
			arredondar= Math.round(resultado * 100);
			resultado = Math.ceil(arredondar)/100;
		});
		n = resultado;
		c = isNaN(c = Math.abs(c)) ? 2 : c, d = d == undefined ? "," : d, t = t == undefined ? "." : t, s = n < 0 ? "-" : "", i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", j = (j = i.length) > 3 ? j % 3 : 0;
    	moeda = s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
		$('#total').maskMoney();
		$('#total').text(moeda);
		
		
		
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
			var valorItem = carrinhoAtual.find('.dinheiro');
			var resultado = 0;
			var moeda;
			var c;
			var n;
			var d;
			var t;
			valorItem.each(function(){
				var arredondar;
				var tdAtual = $(this).text().replace('R$','');
				tdAtual = tdAtual.replace('.','')
				var pegaValor = parseFloat(tdAtual.replace(',', '.'));
				resultado = parseFloat(resultado + pegaValor);
				arredondar= Math.round(resultado * 100);
				resultado = Math.ceil(arredondar)/100;
			});
			n = resultado;
			c = isNaN(c = Math.abs(c)) ? 2 : c, d = d == undefined ? "," : d, t = t == undefined ? "." : t, s = n < 0 ? "-" : "", i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", j = (j = i.length) > 3 ? j % 3 : 0;
			moeda = s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
			$('#total').maskMoney();
			$('#total').text(moeda);
		});
		return false;
	});
	$(document).on('click', '#gerar', function () {
		var json = {};
		
		json["nomeProduto"] = ListarProdutos();
		json["Total"]=$('#total').text();
		json["DiasEntrega"]=$("#diasEntrega").val();
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
						window.location.replace("../imprimir/orcamento/"+response.codigoOrcamento);
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


