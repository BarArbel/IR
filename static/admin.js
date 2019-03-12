function hideShow (titleValue) {

	titleValue = titleValue.split(':', 2)[1];

	window.location.href="adminAction?param1="+titleValue;
}

function addClickListener()
{
	// Get all files
	var fileArr = document.getElementsByClassName("file");

	// Add listeners to all files
	for (var i = fileArr.length - 1; i >= 0; i--) {
		fileArr[i].addEventListener("click", function(){
			titleValue=$("h2", this).html();
  			hideShow(titleValue);
		});
	}
}

$( document ).ready(function() {

	addClickListener();

});
