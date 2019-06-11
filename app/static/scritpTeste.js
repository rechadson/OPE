$(function()
{
    //Executa a requisição quando o campo username perder o foco
    $('#cpf').blur(function()
    {
    function TestaCPF() {
        var cpf = $('#cpf').val().replace(/[^0-9]/g, '').toString();
        var Soma, Resto, borda_original;
        Soma = 0;
        
        if (cpf == "00000000000"){
            document.getElementById("cpf").setCustomValidity('Invalid');
            return false;
        }
        
        for (i=1; i<=9; i++){
            Soma = Soma + parseInt(cpf.substring(i-1, i)) * (11 - i);
        }
        
        Resto = (Soma * 10) % 11;
        if ((Resto == 10) || (Resto == 11)){
            Resto = 0;
        }
        
        if (Resto != parseInt(cpf.substring(9, 10))){
            document.getElementById("cpf").setCustomValidity('Invalid');
            return false;
        }
        
        Soma = 0;
        for (i = 1; i <= 10; i++){
            Soma = Soma + parseInt(cpf.substring(i-1, i)) * (12 - i);
        }
        
        Resto = (Soma * 10) % 11;
        if ((Resto == 10) || (Resto == 11)){
            Resto = 0;
        }
        
        if (Resto != parseInt(cpf.substring(10, 11))){
            document.getElementById("cpf").setCustomValidity('Invalid');
            return false;
        }
        
        document.getElementById("cpf").setCustomValidity('');
        return true;
    }
});
});