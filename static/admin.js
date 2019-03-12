function hideShow (titleValue) {

	var input = document.createElement('input');
    input.type = 'hidden';
	input.name = 'param1';
    input.value = titleValue.split(':', 2)[1];
    $('#showhide').append(input);

	$('#showhide').submit();
	//window.location.href="adminAction?param1="+titleValue;
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
