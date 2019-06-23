$(function () {
    $(document).on('click', '#pesquisarOrcamento', function () {
		
        window.location.replace("../../Pedido/"+$("#codOrcamento").val());
    });
    
    $('#cpf').change(function() {
		$.ajax({
		url: '/cliente/',
		data: $('#FormPedido').serialize(),
		type: 'POST',
		success: function(response) {
			console.log(response)
			if(response.CPF != "Não cadastrado"){
                $("#Nome").val(response.nome)
                $("#Telefone").val(response.telefone)
                $("#Endereco").val(response.Endereco)
                $("#Complemento").val(response.Complemento)
                $("#Estado").val(response.Estado)
                $("#Cidade").val(response.Cidade)
                $("#CEP").val(response.CEP) 
                $("#CEP").attr("readonly","readonly")
                $("#Nome").attr("readonly","readonly")
                $("#Telefone").attr("readonly","readonly")
                $("#Endereco").attr("readonly","readonly")
                $("#Complemento").attr("readonly","readonly")
                $("#Estado").attr("readonly","readonly")
                $("#Cidade").attr("readonly","readonly")
                $("#CEP").attr("readonly","readonly")             
        }
        else{
            $("#cpf").val("")
            $("#Nome").val("")
            $("#Telefone").val("")
            $("#Endereco").val("")
            $("#Complemento").val("")
            $("#Estado").val("")
            $("#Cidade").val("") 
            $("#CEP").val("")
            $("#CEP").removeAttr("readonly")
            $("#Nome").removeAttr("readonly")
            $("#Telefone").removeAttr("readonly")
            $("#Endereco").removeAttr("readonly")
            $("#Complemento").removeAttr("readonly")
            $("#Estado").removeAttr("readonly")
            $("#Cidade").removeAttr("readonly")
            $("#CEP").removeAttr("readonly")  
        }
		},
		error: function(error) {
			console.log(error);
		}
		});
	});
		
	return false			
})