
$(function()
{      
    $(document).ready(function(){
        $('.dinheiro').maskMoney();
     });    
   
    
    $( "#cnpj" ).focus(function() {
        $("#cnpj").mask("99.999.999/9999-99");

      });
    //Executa a requisição quando o campo username perder o foco
    $('#cnpj').blur(function()
    { 
            cnpj = $('#cnpj').val().replace(/[^0-9]/g, '').toString()
            
            if(cnpj == ''){ return false;}
               
            if (cnpj.length != 14){
                console.log(cnpj.length)
                alert("CNPJ Invalido");
                document.getElementById("cnpj").setCustomValidity('CNPJ invalido');
                return false;
            }
            // Elimina CNPJs invalidos conhecidos
            if (cnpj == "00000000000000" || 
                cnpj == "11111111111111" || 
                cnpj == "22222222222222" || 
                cnpj == "33333333333333" || 
                cnpj == "44444444444444" || 
                cnpj == "55555555555555" || 
                cnpj == "66666666666666" || 
                cnpj == "77777777777777" || 
                cnpj == "88888888888888" || 
                cnpj == "99999999999999")
                {
                alert("CNPJ Invalido");
                
                document.getElementById("cnpj").setCustomValidity('CNPJ invalido');
                return false;
                } 
            tamanho = cnpj.length - 2
            numeros = cnpj.substring(0,tamanho);
            digitos = cnpj.substring(tamanho);
            soma = 0;
            pos = tamanho - 7;
            for (i = tamanho; i >= 1; i--) {
              soma += numeros.charAt(tamanho - i) * pos--;
              if (pos < 2)
                    pos = 9;
            }
            resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
            if (resultado != digitos.charAt(0)){
                alert("CNPJ Invalido");
                document.getElementById("cnpj").setCustomValidity('CNPJ invalido');
                return false;
            }
            tamanho = tamanho + 1;
            numeros = cnpj.substring(0,tamanho);
            soma = 0;
            pos = tamanho - 7;
            for (i = tamanho; i >= 1; i--) {
              soma += numeros.charAt(tamanho - i) * pos--;
              if (pos < 2)
                    pos = 9;
            }
            resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
            if (resultado != digitos.charAt(1)){
                alert("CNPJ Invalido");
                document.getElementById("cnpj").setCustomValidity('CNPJ invalido');
                return false;
            }
                   
            return true;
            
            
            
        });
       
        $( "#cpf" ).focus(function() {
        $("#cpf").mask("999.999.999-99");
        $('#cpf').attr('maxlength',14);
      });
    //Executa a requisição quando o campo username perder o foco
    $('#cpf').blur(function()
    {
        var cpf = $('#cpf').val().replace(/[^0-9]/g, '').toString();

        if( cpf.length == 11 )
        {
            var v = [];

            //Calcula o primeiro dígito de verificação.
            v[0] = 1 * cpf[0] + 2 * cpf[1] + 3 * cpf[2];
            v[0] += 4 * cpf[3] + 5 * cpf[4] + 6 * cpf[5];
            v[0] += 7 * cpf[6] + 8 * cpf[7] + 9 * cpf[8];
            v[0] = v[0] % 11;
            v[0] = v[0] % 10;

            //Calcula o segundo dígito de verificação.
            v[1] = 1 * cpf[1] + 2 * cpf[2] + 3 * cpf[3];
            v[1] += 4 * cpf[4] + 5 * cpf[5] + 6 * cpf[6];
            v[1] += 7 * cpf[7] + 8 * cpf[8] + 9 * v[0];
            v[1] = v[1] % 11;
            v[1] = v[1] % 10;

            //Retorna Verdadeiro se os dígitos de verificação são os esperados.
            if ( (v[0] != cpf[9]) || (v[1] != cpf[10]) )
            {
                

                alert("CPF Invalido");
                document.getElementById("cpf").setCustomValidity('CPF invalido');
                return false;
            }
        }
        else
        {
            
            alert("CPF Invalido");
            document.getElementById("cpf").setCustomValidity('CPF invalido');
            return false;
        }     
        
    });
});
