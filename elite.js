window.onload=onWindowLoad;

window.onerror = function(msg, url, line, col, error) {
    var extra = !col ? '' : '\ncolumn: ' + col;
    extra += !error ? '' : '\nerror: ' + error;

    alert("Error: " + msg + "\nurl: " + url + "\nline: " + line + extra);
    return false;
};

var serviceurl = "http://localhost:8000/";
var stationStorage = {};
var systemStorage = {};

 	function onWindowLoad()
  	{
  		// Basic JS check
		var jsCheck = document.getElementById("jsCheck");
		jsCheck.parentNode.removeChild(jsCheck);

		addOrUpdateStep(null, 0);

		// Basic jQuery check
		$(document).ready(function() {
		$("#jQueryCheck").html("");	
			var jsCheck = document.getElementById("jQueryCheck");
			if(jsCheck.innerHTML == "") {
				jsCheck.parentNode.removeChild(jsCheck);
			}
	 


		});

//			testStep = {};
//			testStep.system = "Eravate";
//			testStep.station = "Russell Ring";
//			testStep.missions = [];
//			mission1 = {};
//			mission1.commodity = "Beryllium";
//			mission1.type = "Buy";
//			mission1.amount = "76";
//			mission2 = {};
//			mission2.commodity = "Basic Medicines";
//			mission2.type = "Buy";
//			mission2.amount = "12";
//			testStep.missions.push(mission1);
//			testStep.missions.push(mission2);
  	}

function removeMission(element) {
	var oldDiv = element.parentNode;
	oldDiv.parentNode.removeChild(oldDiv);
}

function missiontype(element) {
	parent = element.parentNode;
	if(element.value == "Delivery") {
		addAutocompleteBox(parent, "commodity", "Commodity", "comodities");
		addBox(parent, "missionXYamoun", "Amount");
		addAutocompleteBox(parent, "targetSystem", "System", "systems");
		addAutocompleteBox(parent, "targetStation", "Station", "stations");
		addBox(parent, "reward", "Reward");
	}
	if(element.value == "Intel") {
		addAutocompleteBox(parent, "system", "System", "systems");
		addAutocompleteBox(parent, "station", "Station", "stations");
		addBox(parent, "reward", "Reward");
	}
	if(element.value == "Source") {
		addAutocompleteBox(parent, "commodity", "Commodity", "comodities");
		addBox(parent, "amount", "Amount");
		addBox(parent, "reward", "Reward");
	}	
}

function addMission(stepId) {
	 step = document.getElementById("step"+stepId);
	 missions = childById(step, "missions");
	 missionId = missions.childElementCount;

	mission = document.createElement('li');
	mission.id = "step" + stepId + "mission" + missionId;
	mission.setAttribute("class", "mission");
	missions.append(mission);

	var removeButton = document.createElement('button');
	removeButton.innerHTML = "Remove";
	removeButton.setAttribute("onClick", "removeMission(this)");
	mission.append( removeButton );

	input = addAutocompleteBox(mission, "type", "Task", "missions");
	input.setAttribute("onChange", "missiontype(this)");  // use Validation API
}

function addBox(parent, id, label) {
	span = document.createElement('span');
	span.innerHTML = label+": ";
	parent.appendChild(span);

	input = document.createElement('input');
	input.id = id;
	parent.appendChild(input);
}

function addAutocompleteBox(parent, id, label, mode) {
	span = document.createElement('span');
	span.innerHTML = label+": ";
	parent.appendChild(span);

	input = document.createElement('input');
	input.id = id;
	parent.appendChild(input);

	$(input).autocomplete({
		source: serviceurl + mode
	});

	return input;
}

function addSystemBox(parent) {
	span = document.createElement('span');
	span.innerHTML = "System: ";
	parent.appendChild(span);

	systemInput = document.createElement('input');
	systemInput.id = "system";
	parent.appendChild(systemInput);

	$(systemInput).autocomplete({
		source: serviceurl + "systems",
		select: function(event, ui) {
			systemInput.setAttribute("systemid", ui.item.data);
		}
	});

	return systemInput;
}

function addStationBox(parent, systemBox) {
	span = document.createElement('span');
	span.innerHTML = "Station: ";
	parent.appendChild(span);

	stationInput = document.createElement('input');
	stationInput.id = "station";
	parent.appendChild(stationInput);

	$(stationInput).autocomplete({
		source: function(request, response ) {
			$.getJSON(
				serviceurl + "stations",
				{ term: request.term,
					system: systemBox.getAttribute("systemid") }, 
				response
			);
		},
		select: function(event, ui) {
			stationInput.setAttribute("stationid", ui.item.data);
			stationInput.setAttribute("systemid", ui.item.systemId);
			systemBox.value = ui.item.systemName;
			systemBox.setAttribute("systemid", ui.item.systemId);
		}
	});

	systemBox.addEventListener("change", function(){
		if( systemBox.getAttribute("systemid") != stationInput.getAttribute("systemid") ) {
			stationInput.value = "";
		}
	}); 

	return stationInput;
}

function addOrUpdateStep(stepJson, stepId) {
	var step = document.getElementById("step"+stepId);
	if(!step) {
		step = document.createElement('div');
		step.id = "step"+stepId;
		step.setAttribute("class", "step");
		
		systemBox = addSystemBox(step);
		stationBox = addStationBox(step, systemBox);
		systemBox.station = stationBox;

				addButton = document.createElement("button");
				addButton.setAttribute("onClick", "addMission("+stepId+")");
				addButton.innerHTML = "Add Mission";
				step.appendChild(addButton);

				missions = document.createElement('ul');
				missions.id = "missions";
				step.appendChild(missions);

				steps = document.getElementById('steps');
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
			data.steps = [];
			
			for( stepDiv of document.getElementById('steps').childNodes) {
				var step = {};
				step.system = childById(stepDiv, "system").value;
				step.station = childById(stepDiv, "station").value;
				step.missions = [];
				for( missionLi of childById(stepDiv, "missions").childNodes) {
					var mission = {};
					mission.type = childById(missionLi, "type").value;
					if(mission.type == "Intel") {
						mission.reward = childById(missionLi, "reward").value;
						mission.station = childById(missionLi, "station").value;
						mission.system = childById(missionLi, "system").value;
					}
					if(mission.type == "Delivery") {
						mission.reward = childById(missionLi, "reward").value;
						mission.station = childById(missionLi, "station").value;
						mission.system = childById(missionLi, "system").value;
						mission.amount = childById(missionLi, "amount").value;
						mission.commodity = childById(missionLi, "commodity").value;
					}
					if(mission.type == "Source") {
						mission.reward = childById(missionLi, "reward").value;
						mission.amount = childById(missionLi, "amount").value;
						mission.commodity = childById(missionLi, "commodity").value;
					}
					step.missions.push(mission);
				}
				data.steps.push( step );
			}

     // alert(JSON.stringify(data, null, 2));

  		xhttp.open("GET", serviceurl + "compute?data=" + JSON.stringify(data));
  		xhttp.send();  		
		}
		
function childById(parent, id) {
	for( child of parent.childNodes ) {
		if(child.id == id) {
			return child;
		}
	}
}