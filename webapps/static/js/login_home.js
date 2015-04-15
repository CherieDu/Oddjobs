var req;
var get_box = document.getElementById('get-box');
var write_box = document.getElementById('write-box');
var cmt_box = document.getElementById('comment-box-1');
var new_cmt_box = document.getElementById('comment-box-2');
var view_cmt_box = document.getElementById('view-cmt-box');
var letter_view_box = document.getElementById('letter-view-box');
var cmt_view_box = document.getElementById('cmt-view-box');



document.getElementById("new-cmt").onclick = function () {
	console.log("new comment");
	if(cmt_view_box.attributes['class'].value == 'not-show'){
		cmt_view_box.setAttribute('class', 'show');
		letter_view_box.setAttribute('class', 'not-show');
	}else{
		cmt_view_box.setAttribute('class', 'not-show');
	}
}

document.getElementById("friend-add-request").onclick = function (){
	console.log("friend_add_request");
	if(letter_view_box.attributes['class'].value == 'not-show'){
		letter_view_box.setAttribute('class', 'show');
		cmt_view_box.setAttribute('class', 'not-show');
	}else{
		letter_view_box.setAttribute('class', 'not-show');
	}
}


document.getElementById("write-btn").onclick = function (){
	console.log("write");
	if(write_box.attributes['class'].value == 'not-show'){
		write_box.setAttribute('class', 'show');
	}else{
		write_box.setAttribute('class', 'not-show');
	}
	get_box.setAttribute('class', 'not-show');
	cmt_box.setAttribute('class', 'not-show');
	new_cmt_box.setAttribute('class', 'not-show');
	view_cmt_box.setAttribute('class', 'not-show');
}



document.getElementById("cmt-btn").onclick = function (){
	console.log("comment");
	if(cmt_box.attributes['class'].value == "not-show"){
		cmt_box.setAttribute('class', 'show');
	}else{
		cmt_box.setAttribute('class', 'not-show');
	}
}


document.getElementById("cancel-btn").onclick = function (){
	console.log("cancel");
	write_box.setAttribute('class', 'not-show');
}



document.getElementById("get-btn").addEventListener("click", getFunctionShow);
// document.getElementById("get-btn").addEventListener("click", getNewLetter); // problem

function getFunctionShow(){
	console.log("get");
	if(get_box.attributes['class'].value == 'not-show'){
		get_box.setAttribute('class', 'show');
	}else{
		get_box.setAttribute('class', 'not-show');
		// req = createRequest();
		// req.onreadystatechange = updateLetterContent;
		// req.open("GET", "/letters/get", true);
		// req.send();
	}
	write_box.setAttribute('class', 'not-show');
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
