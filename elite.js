 	function onWindowLoad()
  	{
		var jsCheck = document.getElementById("jsCheck");
		jsCheck.innerHTML = "";
  	}

  	window.onload=onWindowLoad;
  	
	// Basic jQuery
	$(document).ready(function() {
		$("#jQueryCheck").html("");
		$('#startSystem').autocomplete({
    		source: "http://localhost:8000/systems"
		});
	});

/* onSelect: function (suggestion) {
        alert('You selected: ' + suggestion.value + ', ' + suggestion.data);
    }*/