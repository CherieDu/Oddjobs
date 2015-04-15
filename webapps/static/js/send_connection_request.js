var send_req;

document.getElementById("connect-req-btn").onclick = function (){
	console.log("send friend request");

	var letter = document.getElementById("connect-req-btn");
	var user_id = letter.attributes["letter_owner"].value;

	send_req = createRequest();
	send_req.onreadystatechange = sendConnectionReq;
	send_req.open("GET", "/letters/request-connection/" + user_id, true);
	send_req.send();
}

function sendConnectionReq(){
	if(send_req.readyState != 4 || send_req.status != 200){
		return;
	}

	document.getElementById("requst-result-msg").innerHTML = "request has been sent";
};


// var a = document.getElementById("connect-req-btn");
// a.attributes["letter_owner"].value;