function duplicarCampos(){
	var clone = document.getElementById('inlineFormCustomSelect').cloneNode(true);
	var destino = document.getElementsByClassName('produto');
	destino.appendChild (clone.getElementById('inlineFormCustomSelect'));
	
	///var camposClonados = clone.getElementsByTagName('input');
	
	//for(i=0; i<camposClonados.length;i++){
		//camposClonados[i].value = '';
	//}	
}

function removerCampos(id){
	var node1 = document.getElementById('destino');
	node1.removeChild(node1.childNodes[0]);
}