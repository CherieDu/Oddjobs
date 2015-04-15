var cmtReq;

// Send a new request
function sendConnectionCheckRequest(){
	if(window.XMLHttpRequest){
		cmtReq = new XMLHttpRequest();
	}else{
		cmtReq = new ActiveXObject("Microsoft.XMLHTTP");
	}

	cmtReq.onreadystatechange = newCommentUpdate;
	cmtReq.open("GET", "/letters/get-new-comment", true);
	cmtReq.send();
}

function newCommentUpdate(){
	if(cmtReq.readyState != 4 || cmtReq.status != 200){
		return;
	}
	var items = JSON.parse(cmtReq.responseText);

	var box = document.getElementById("cmt-view-box");
	while (box.hasChildNodes()) {
        box.removeChild(box.firstChild);
    }


    box = $("#cmt-view-box");
	for(var i = 0; i < items.length; i++){
		var item = items[i];

		var tb = 
		'<table class="new-cmt-table">' +
		'<tr>' +
		'<td width="70%">' +
		item["fields"]["content"]+
		'</td>' +
		'<td width="30%">' +
		'<a href="/letters/veiw-new-cmt/' + item["pk"] + '" class="btn btn-info"><i class="fa fa-eye"></i></a>' +
		'</td>' +
		'</tr>' +
		'</table>' +
		'<hr>';

		box.append(tb);
	}

	var btn_color = document.getElementById("new-cmt");
	if(items.length > 0){
		btn_color.setAttribute('style','color:green');
	}else{
		btn_color.setAttribute('style','color:white');
	}

}


window.setInterval(sendConnectionCheckRequest, 3000);


