var bidButton = document.getElementById('snackbar-place-bid');
var bidmessage = document.getElementById('bidmessage')

bidButton.disabled = true;
bidButton.style.color = "red";
bidButton.style.border = "1px solid red";
bidButton.style.backgroundColor = "white";

bidmessage.addEventListener('input', function(e){
	if(bidmessage.value.length < 15){
    bidButton.disabled = true;
		bidButton.style.backgroundColor = "white";
		bidButton.style.color = "red";
		bidButton.style.border = "1px solid red"
	}
	else{
    bidButton.disabled = false;
		bidButton.style.backgroundColor = "blue";
		bidButton.style.color = "white";
		bidButton.style.border = "";
	}
})
