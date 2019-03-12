window.onload=onWindowLoad;

window.onerror = function(msg, url, line, col, error) {
    var extra = !col ? '' : '\ncolumn: ' + col;
    extra += !error ? '' : '\nerror: ' + error;

    alert("Error: " + msg + "\nurl: " + url + "\nline: " + line + extra);
    return false;
};

function getStepSys(element) {
		parentId = element[0].parentNode.parentNode.id
		stepId = parentId.slice(-1)
    return $("#system"+stepId).val()
}

 	function onWindowLoad()
  	{
  		// Basic JS check
		var jsCheck = document.getElementById("jsCheck");
		jsCheck.innerHTML = "";

		addOrUpdateStep(null, 0);

		// Basic jQuery check
		$(document).ready(function() {
			$("#jQueryCheck").html("");
			
			$('.stationAutocomplete').autocomplete({
					source: function(request, response ) {
						$.getJSON(
							"http://localhost:8000/stations",
							{ term: request.term,
								system: getStepSys(this.element) }, 
							response
						);
					}
			});
			$('.systemAutocomplete').autocomplete({
    			source: "http://localhost:8000/systems",
    			minLength: 2
			});
			$('.commoditiesAutocomplete').autocomplete({
    			source: "http://localhost:8000/commodities",
    			minLength: 3
			});
		});

			testStep = {};
			testStep.system = "Eravate";
			testStep.station = "Russell Ring";
			testStep.missions = [];
			mission1 = {};
			mission1.commodity = "Beryllium";
			mission1.type = "Buy";
			mission1.amount = "76";
			mission2 = {};
			mission2.commodity = "Basic Medicines";
			mission2.type = "Buy";
			mission2.amount = "12";
			testStep.missions.push(mission1);
			testStep.missions.push(mission2);
  	}

function removeMission(element) {
	var oldDiv = element.parentNode;
	oldDiv.parentNode.removeChild(oldDiv);
}

function missiontype(element) {
	if(element.value == "Delivery") {
		var commodity = document.createElement('span');
		commodity.innerHTML = "commodity"
		element.parentNode.append( commodity );
		var amount = document.createElement('span');
		amount.innerHTML = "amount"
		element.parentNode.append( amount );
		var destination = document.createElement('span');
		destination.innerHTML = "destination";
		element.parentNode.append( destination );
		var reward = document.createElement('span');
		reward.innerHTML= "reward";
		element.parentNode.append( reward );
	}
}

function addMission(element) {
	var newMissionDiv = document.createElement('div');
	element.parentNode.appendChild(newMissionDiv);

	var removeButton = document.createElement('button');
	removeButton.innerHTML = "Remove";
	// removeButton.setAttribute("type", "button");
	removeButton.setAttribute("onClick", "removeMission(this)");
	newMissionDiv.append( removeButton );

	//div = document.createElement('div');
	//p = document.createElement('span');
	input = document.createElement('input');
	// input.setAttribute("class", "missionsAutocomplete");
	input.setAttribute("onChange", "missiontype(this)");
	$(input).autocomplete({
		source: "http://localhost:8000/missions"
	});
	// input.id = label + stepId;
	//p.innerHTML = label+": ";
	//div.appendChild(p);
	//div.appendChild(input);

	newMissionDiv.append( input ); // use Validation API

	var newMission = "";
	  // newMission += "	Type: <input list='missionDropdown' name='mission'>";
		// newMission += "	Commodity: <input class='commoditiesAutocomplete' name='commodity'>";
		// newMission += "	Target: <input class='stationsAutocomplete' name='commodity'/>";
		// newMission += "	Tonnes: <input name='tonnes'/>";
		// newMission += "	Value: <input />";
	

}

		function addBox(label, stepId) {
			div = document.createElement('div');
			p = document.createElement('span');
			input = document.createElement('input');
			input.setAttribute("class", label+"Autocomplete");
			input.id = label + stepId;
			p.innerHTML = label+": ";
			div.appendChild(p);
			div.appendChild(input);

			return div;
		}

    function addOrUpdateStep(stepJson, stepId) {
			var step = document.getElementById( ("step"+stepId) );
			if(!step){
				steps = document.getElementById('steps');
				step = document.createElement('div');
				step.id = "step"+stepId;
				step.setAttribute("class", "step");
				step.appendChild(addBox("system", stepId))
				step.appendChild(addBox("station", stepId))

				missions = document.createElement('ul');
				missions.innerHTML = 'Missions: <button onClick="addMission(this)" type="button">Add</button> <br/>';
				step.appendChild(missions);

				steps.appendChild(step);
			}     
			
			if(stepJson) {
				step.childNodes[0].childNodes[1].value = stepJson.system; 
				step.childNodes[1].childNodes[1].value = stepJson.station;
				
				for( m in stepJson.missions){	
					mission = stepJson.missions[m]
					var missionDiv = document.createElement('li');
					missionDiv.innerHTML = mission["type"] + " " + mission["amount"] + " Units of " + mission.commodity 
					step.childNodes[2].appendChild(missionDiv)
				}

			}
    }

  	function compute() {
 		   var xhttp = new XMLHttpRequest();
 		   xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
			   var resp = this.responseText;
    	   data = JSON.parse(resp);

         for( step in data.route) {
					addOrUpdateStep(data.route[step], step)
				 }		 
				 
        } else {
    			// document.getElementById("demo").innerHTML = "Error on commodities receive " + this.readyState + " " + this.status;
    		}
  		};

      var data = {};
      data.cargohold = document.getElementById('cargohold').value;
      data.landingpad = document.getElementById('landingpad').value;
      data.jumprange = document.getElementById('jumprange').value;
      data.maxhops = document.getElementById('maxhops').value;
      data.route = [];
      var step0 = {};
      step0.systemId = document.getElementById('system0').value;
      step0.stationId = document.getElementById('station0').value;
      data.route.push( step0 );

      // alert(JSON.stringify(data, null, 2));

  		xhttp.open("GET", "http://localhost:8000/compute?data=" + JSON.stringify(data));
  		xhttp.send();  		
  	}

	function testApi() {
		// Check for the various File API support.
		
		if (!(window.File && window.FileReader && window.FileList && window.Blob)) {
  			alert('The File APIs are not fully supported in this browser.');
		}

		// Great success! All the File APIs are supported. 
	}
 
  function handleFileSelect(evt) {
    var files = evt.target.files; // FileList object

    // files is a FileList of File objects. List some properties.
    var output = [];
    for (var i = 0, f; f = files[i]; i++) {
      output.push('<li><strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
                  f.size, ' bytes, last modified: ',
                  f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a',
                  '</li>');
 

	var reader = new FileReader();
    reader.onload = function() {
 	     
 		var output = [];
 	 
       var jsonArray = JSON.parse(reader.result );//

        var firstElem = jsonArray[0];
        // output.push(firstElem.id);
       for( x in jsonArray) {
       	output.push( jsonArray[x].name );
  
         }

			document.getElementById('contents').innerHTML = output.join('');
       	};

 	reader.readAsText(f);
 }
    

    document.getElementById('list').innerHTML = '<ul>' + output.join(' # ') + '</ul>';
  }

  function foo(){
  	
// get most recent from https://eddb.io/archive/v6/stations.json

// infos about FileReader https://www.html5rocks.com/en/tutorials/file/dndfiles/


 document.getElementById('files').addEventListener('change', handleFileSelect, false);
  }