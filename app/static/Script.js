function myFunction() {
    
    window.alert("sometext");
  }
        

  <script>

  window.onload = function()
  
  {
  
  //Ou: document.getElementById("opcoes").addEventListener("change", function()...
  
  document.getElementById("SelectFornecedor").onchange = function()
  
  {
    var e = document.getElementById("SelectFornecedor");
    var itemSelecionado = e.options[e.selectedIndex].text;
    window.alert(fornecedores);
    if(itemSelecionado != "")
    {
      
      var i;
      for (i = 0; i < fornecedores.length; i++) { 
        window.alert(fornecedor);
        if(fornecedores[i] == fornecedor)
        {
          window.alert(itemSelecionado);
          document.getElementById("cnpj").setAttribute("value","teste1112");
        }
        
      }
    }
 
  
  }
  
  }
  
  </script>
<script>
function changeText(id) {
id.innerHTML = "Ooops!";
}
</script>
