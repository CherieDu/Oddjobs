var req;

var get_box = document.getElementById('get-box');

document.getElementById("get-btn-non-login").addEventListener("click", getFunctionShow);
document.getElementById("get-btn-non-login").addEventListener("click", getNewLetter);

function getFunctionShow(){
	console.log("get");
	get_box.setAttribute('class', 'show');
}


function getNewLetter(){
		req = createRequest();
		req.onreadystatechange = updateLetterContent;
		req.open("GET", "/letters/get", true);
		req.send();
}

function updateLetterContent(){
	if(req.readyState != 4 || req.status != 200){
		return;
	}
	var items = JSON.parse(req.responseText);
	var letter_content;
	if(items[0] == undefined){
		letter_content = "Sorry, seem no letter there...";
	}else{
		letter_content = items[0]['fields']['content'];
	}

	document.getElementById("get_a_letter").innerHTML = letter_content;
}