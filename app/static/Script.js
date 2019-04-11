function myFunction() {
    
    window.alert("sometext");
  }
        



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
  
 
function changeText(id) {
id.innerHTML = "Ooops!";
}
function duplicarCampos(){
	var clone = document.getElementById('origem').cloneNode(true);
	var destino = document.getElementById('destino');
	destino.appendChild (clone);
	
	var camposClonados = clone.getElementsByTagName('input');
	
	for(i=0; i<camposClonados.length;i++){
		camposClonados[i].value = '';
	}
	
	
	
}

function removerCampos(id){
	var node1 = document.getElementById('destino');
	node1.removeChild(node1.childNodes[0]);
}
