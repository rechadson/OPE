$(function () {
    $(document).on('click', '#pesquisarOrcamento', function () {
		
        window.location.replace("../Pedido/"+$("#codOrcamento").val());
    });
    return false
		
				
})