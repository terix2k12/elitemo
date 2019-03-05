  window.onload=onWindowLoad;

 	function onWindowLoad()
  	{
  		// Basic JS check
		var jsCheck = document.getElementById("jsCheck");
		jsCheck.innerHTML = "";

		addOrUpdateStep(null, 0);

		// Basic jQuery check
		$(document).ready(function() {
			$("#jQueryCheck").html("");
			
			$('.systemAutocomplete').autocomplete({
    			source: "http://localhost:8000/systems",
    			minLength: 4
			});
			$('.stationAutocomplete').autocomplete({
    			source: "http://localhost:8000/stations",
    			minLength: 4
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
  	
  	function addMission(element) {
  		var newMission = "";
		newMission += "	Type: <input list='missionDropdown' name='mission'>";
		newMission += "	Commodity: <input class='commoditiesAutocomplete' name='commodity'>";
		newMission += "	Target: <input class='stationsAutocomplete' name='commodity'/>";
		newMission += "	Tonnes: <input name='tonnes'/>";
		// newMission += "	Value: <input />";
		newMission += " <button onClick='removeMission(this)' type='button'>Remove</button>";

		var newDiv = document.createElement('div');
		newDiv.innerHTML = newMission;

  		element.parentNode.appendChild(newDiv);
  	}

		function addBox(label) {
			div = document.createElement('div');
			p = document.createElement('span');
			input = document.createElement('input');
			input.setAttribute("class", label+"Autocomplete");
			input.id = label;
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
				step.appendChild(addBox("system"))
				step.appendChild(addBox("station"))

				missions = document.createElement('ul');
				missions.innerHTML = 'Missions: <button onClick="addMission(this)" disabled="true" type="button">Add</button> <br/>';
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
      step0.systemId = document.getElementById('system').value;
      step0.stationId = document.getElementById('station').value;
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