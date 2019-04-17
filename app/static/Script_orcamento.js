$(function () {
	var scntDiv = $('.produto');
$(document).on('click', '#addInput', function () {
$.ajax({
url: '/adicionar/produto/',
data: $('#formprod').serialize(),
type: 'POST',
success: function(response) {
  $('<li class="list-group-item d-flex justify-content-between lh-condensed">'+
'<div id="preco">'+
'<h6 class="my-0">'+response.nome+'</h6>'+
'<small class="text-muted" name="nome_Produto">'+response.nome+'</small>'+
'</div>'+
'<span class="text">'+response.preco+'</span>'+
'<a class="btn btn-danger" href="javascript:void(0)" id="remInput">'+
				'<span class="glyphicon glyphicon-minus" aria-hidden="true"></span> '+
				'Remover produto'+
	'</a>'+'</li>').appendTo(scntDiv);  },
error: function(error) {
	console.log(error);
}
});
	
		return false;
	});
	$(document).on('click', '#remInput', function () {
		$(this).parents('li').remove();
		return false;
	});
});
$(document).on('click', '#gerar', function () {
var scntDiv = $('.produto');
$.ajax({
url: '/orcamento/cadastrar/',
data: $('.needs-validation').serialize(),
type: 'POST',
success: function(response) {
  console.log("teste");
  
},
error: function(error) {
	console.log(error);
}
});
	
		return false;
	});


