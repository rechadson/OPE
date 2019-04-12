function duplicarCampos(){
	var clone = document.getElementsByClassName('produto').clo(true);
	var destino = document.getElementsByClassName('produto');
	destino.appendChild (clone);
	
	///var camposClonados = clone.getElementsByTagName('input');
	
	//for(i=0; i<camposClonados.length;i++){
		//camposClonados[i].value = '';
	//}	
}

function removerCampos(id){
	var node1 = document.getElementById('destino');
	node1.removeChild(node1.childNodes[0]);
}
