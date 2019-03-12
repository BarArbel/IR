
function showResultPage(titleValue) {

	var fileName = titleValue.split('/', 1)[0];
	window.location.href="get_file_page?param1="+fileName;

}

function validateQuery() {
	// Replace delimiters with space
	var searchQuery = document.getElementsByClassName("query")[0]["search"].value.toLowerCase().replace(/[`~@#$%^*_+\-=?;:'",.<>\{\}\[\]\\\/]/gi, ' ');

	// Replace whitespaces with space
	searchQuery = searchQuery.replace(/\s\s+/g, ' ');
	document.getElementsByClassName("query")[0]["search"].value = searchQuery;
	alert(document.getElementsByClassName("query")[0]["search"].value());
}

function addClickListener()
{
	// Get all results
	var resultsArr = document.getElementsByClassName("result");

	// Add listeners to all results
	for (var i = resultsArr.length - 1; i >= 0; i--) {
		resultsArr[i].addEventListener("click", function(){
			titleValue=$("h2", this).html();
  			showResultPage(titleValue);
		});
	}

}

function validatePass() {
	
  	if (document.getElementsByClassName("adminPass")[0]["Enter"].value != "1234") {
    	alert("Wrong Password!");
    	return false;
    }
}

function adminPass() {

	var modal = document.getElementById('myModal');
	var btn = document.getElementById("myBtn");
	var span = document.getElementsByClassName("close")[0];

	// When the user clicks on the button, open the modal 
	btn.onclick = function() {
	  modal.style.display = "block";
	}

	// When the user clicks on <span> (x), close the modal
	span.onclick = function() {
	  modal.style.display = "none";
	}

	// When the user clicks anywhere outside of the modal, close it
	window.onclick = function(event) {
	  if (event.target == modal) {
	    modal.style.display = "none";
	  }
	}

}


$( document ).ready(function() {

	addClickListener();
	adminPass();
	

});


