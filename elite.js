 	function onWindowLoad()
  	{
		var jsCheck = document.getElementById("jsCheck");
		jsCheck.innerHTML = "";
  	}

  	window.onload=onWindowLoad;
  	
	// Basic jQuery
	$(document).ready(function() {
		$("#jQueryCheck").html("");
		$('.systemsAutocomplete').autocomplete({
    		source: "http://localhost:8000/systems"
		});
		$('.stationsAutocomplete').autocomplete({
    		source: "http://localhost:8000/stations"
		});
		$('.commoditiesAutocomplete').autocomplete({
    		source: "http://localhost:8000/commodities"
		});
	});

/* onSelect: function (suggestion) {
        alert('You selected: ' + suggestion.value + ', ' + suggestion.data);
    }*/