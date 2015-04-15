var connectReq;

// Send a new request
function sendConnectionCheckRequest(){
	if(window.XMLHttpRequest){
		connectReq = new XMLHttpRequest();
	}else{
		connectReq = new ActiveXObject("Microsoft.XMLHTTP");
	}

	connectReq.onreadystatechange = connectionRequest;
	connectReq.open("GET", "/letters/get-connection-request", true);
	connectReq.send();
}

function connectionRequest(){
	if(connectReq.readyState != 4 || connectReq.status != 200){
		return;
	}
	var items = JSON.parse(connectReq.responseText);

	var box = document.getElementById("letter-view-box");
	while (box.hasChildNodes()) {
        box.removeChild(box.firstChild);
    }

    box = $("#letter-view-box");
	for(var i = 0; i < items.length; i++){
		var item = items[i];
		var tb = 
		'<table class="comment-table">' +
		'<tr>' +
		'<td class="comment-table-user">' +
		'<img src="/static/img/default_user.png" style="height:20px; width:20px; "><br>' +
		item["whoFollow_name"] +
		'</td>' + 
		'<td class="comment-table-content" >' +
		'<div class="input-group"> accept friend request? ' +
		'<a href="/letters/accept/' + item["whoFollow_id"] + '" class="btn btn-info"><i class="fa fa-check"></i></a>' +
		'<a href="/letters/deny/' + item["whoFollow_name_id"] + '" class="btn btn-info"><i class="fa fa-times-circle"></i></a>' +
		'</div>' +
		'</td>' +
		'</tr>' +
		'</table>' +
		'<hr>';

		box.append(tb);
	}

	var btn_color = document.getElementById("friend-add-request");
	if(items.length > 0){
		btn_color.setAttribute('style','color:green');
	}else{
		btn_color.setAttribute('style','color:white');
	}

}


window.setInterval(sendConnectionCheckRequest, 3000);


