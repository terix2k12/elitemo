 	function onWindowLoad()
  	{
		var jsCheck = document.getElementById("jsCheck");
		jsCheck.innerHTML = "";
  	}

	function removeMission(element) {
		var oldDiv = element.parentNode;
		oldDiv.parentNode.removeChild(oldDiv);		
	}
  	
  	function addMission(element) {
  		var newMission = "";
		newMission += "	Type: <input list='missionDropdown' name='mission'>";
		newMission += "	Commodity: <input class='commoditiesAutocomplete' name='commodity'>";
		newMission += "	Target: <input class='stationsAutocomplete' name='commodity'/>";
		newMission += "	Tonnes: <input name='commodity'/>";
		// newMission += "	Value: <input name='commodity'/>";
		newMission += " <button onClick='removeMission(this)' type='button'>Remove</button>";

		var newDiv = document.createElement('div');
		newDiv.innerHTML = newMission;

  		element.parentNode.appendChild(newDiv);
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