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

function onWindowLoad() {
	// Basic JS check
	var jsCheck = document.getElementById("jsCheck");
	jsCheck.parentNode.removeChild(jsCheck);

	// Basic jQuery check
	$(document).ready(function() {
		$("#jQueryCheck").html("");	
		var jsCheck = document.getElementById("jQueryCheck");
		if(jsCheck.innerHTML == "") {
			jsCheck.parentNode.removeChild(jsCheck);
		}
	});

	current = document.getElementById("shipconfiguration");
	sysBox = addSystemBox(current);
	addStationBox(current, sysBox);
}

function test() {
	testData = {};
	
	testData.instructions = [];
	testData.cargohold = {};
	testData.missions = [];
	
	// Missions:
	mission1 = {};
	mission1.commodityId = 5;
	mission1.type = "Source";
	mission1.amount = 76;
	mission1.targetStationId = 76;
	
	mission2 = {};
	mission2.commodityId = 9;
	mission2.type = "Deliver";
	mission2.amount = 12;
	mission2.targetStationId = 45;
	mission2.sourceStationId = 34;
	
	mission3 = {};
	mission3.type = "Intel";
	mission3.targetStationId = 45;
	
	testData.missions.push(mission1);
	testData.missions.push(mission2);
	testData.missions.push(mission3);
	
	// Cargohold:
	testData.cargohold.cargospace = 16;
	testData.cargohold.emptycargospace = 5;
	testData.cargohold.cargo = [];
	unit1 = {};
	unit1.targetStationId = 734;
	unit1.commodityId = 9;
	unit1.volume = 7;
	unit2 = {};
	unit2.targetStationId = 521;
	unit2.commodityId = 5;
	unit2.volume = 4;
	testData.cargohold.cargo.push(unit1);
	testData.cargohold.cargo.push(unit2);
	
	// Instructions:
	ins1 = {}
	ins1.stationId = 1234;
	ins1.tasks = [];
	task11 = {"type":"collect", "commodityId":1, "volume":4}
	task12 = {"type":"drop", "commodityId":9, "volume":7}
	ins1.tasks.push(task11);
	ins1.tasks.push(task12);

	ins2 = {}
	ins2.stationId = 934;
	ins2.tasks = [];
	task21 = {"type":"collect", "commodityId":2, "volume":3}
	task22 = {"type":"drop", "commodityId":1, "volume":4}
	ins2.tasks.push(task21);
	ins2.tasks.push(task22);
	
	testData.instructions.push(ins1);
	testData.instructions.push(ins2);	
	
	// Test:
	handleResponse(testData);
}

function removeMission(element) {
	var oldDiv = element.parentNode;
	oldDiv.parentNode.removeChild(oldDiv);
}

function missiontype(element) {
	parent = element.parentNode;
	if(element.value == "Delivery") {
		
		parent.appendChild(document.createElement('br'));
		fromSystemBox = addSystemBox(parent);
		fromSystemBox.id = "systemFrom";
		fromStationBox = addStationBox(parent, fromSystemBox);
		fromStationBox.id = "stationFrom";

		parent.appendChild(document.createElement('br'));
		addAutocompleteBox(parent, "commodity", "Commodity", "comodities");
		addCommodityBox(parent);
		addBox(parent, "amount", "Amount");

		parent.appendChild(document.createElement('br'));
		toSystemBox = addSystemBox(parent);
		toSystemBox.id = "systemTo";
		toStationBox = addStationBox(parent, toSystemBox);
		toStationBox.id = "stationTo";
		
		parent.appendChild(document.createElement('br'));
		addBox(parent, "reward", "Reward");
	}
	if(element.value == "Intel") {
		sysBox = addSystemBox(parent);
		addStationBox(parent, sysBox);
		addBox(parent, "reward", "Reward");
	}
	if(element.value == "Source") {
		addCommodityBox(parent);
		addBox(parent, "amount", "Amount");
		addBox(parent, "reward", "Reward");
	}	
}

function addMission() {
	ship = document.getElementById("shipconfiguration");
	station = childById(ship, "system");
	stationId = station.getAttribute("systemid");

	mission = document.createElement('li');
	mission.setAttribute("class", "mission");

	var removeButton = document.createElement('button');
	removeButton.innerHTML = "Remove";
	removeButton.setAttribute("onClick", "removeMission(this.parent)");
	mission.append( removeButton );

	input = addAutocompleteBox(mission, "type", "Task", "missions");
	input.setAttribute("onChange", "missiontype(this)");  // use Validation API

	missions = document.getElementById("missions");
	missions.append(mission);
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

function addCommodityBox(parent) {
	span = document.createElement('span');
	span.innerHTML = "Commodity: ";
	parent.appendChild(span);

	commodityInput = document.createElement('input');
	commodityInput.id = "commodity";
	parent.appendChild(commodityInput);

	$(commodityInput).autocomplete({
		source: serviceurl + "commodities",
		select: function(event, ui) {
			commodityInput.setAttribute("commodityid", ui.item.data);
		}
	});

	return commodityInput;
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

function addOrUpdateStep(step, stepId) {
	var stepDiv = document.getElementById("step"+stepId);
	if(!stepDiv) {
		stepDiv = document.createElement('div');
		stepDiv.id = "step"+stepId;
		stepDiv.setAttribute("class", "step");

		systemBox = addSystemBox(stepDiv);
		stationBox = addStationBox(stepDiv, systemBox);
		systemBox.station = stationBox;

		tasks = document.createElement('ul');
		tasks.id = "tasks";
		stepDiv.appendChild(tasks);

		stepsDiv = document.getElementById('steps');
		stepsDiv.appendChild(stepDiv);
	}

	if(step) {
		childById(stepDiv, "station").value = step[0] // TODO .stationId;
		// TODO dont just set the ID, set station and system
		
		var taskUl = childById(stepDiv, "tasks");
		for(task of step[1]){ // TODO .tasks
			var taskLi = document.createElement('li');
			// taskLi.innerHTML = task.type + " " + task.volume + " Units of " + task.commodityId 
			taskLi.innerHTML = task[0] + " " + task[1] + " Units of " + task[2] 
			taskUl.appendChild(taskLi)
		}
	}
}

function handleCargohold(cargohold) {
	if(!cargohold.cargo) {
		return;
	}

	document.getElementById('emptycargospace').innerHTML = cargohold.emptycargospace;
	document.getElementById('cargospace').value = cargohold.cargospace;
	cargo = document.getElementById('cargo');
	for(unit of cargohold.cargo) {
		newunit = document.createElement('li');
		newunit.innerHTML = "c:"+unit.commodityId+" t:"+unit.targetStationId+" v:"+unit.volume;
		cargo.appendChild(newunit);
	}
}

function handleInstructions(instructions) {
	for(stepId in instructions) {
		step = instructions[stepId];
		addOrUpdateStep(step, stepId);
	}
}

function handleMissions(missions) {
	missionDiv = document.getElementById('missionboard');
	for(mission of missions) {
		newmission = document.createElement('li');
		newmission.innerHTML = "type:"+mission.type;
		missionDiv.appendChild(newmission);
	}
}

function handleResponse(jsonData) {
	handleCargohold(jsonData.cargohold);
	handleMissions(jsonData.missions);
	handleInstructions(jsonData.instructions);
}

function compute() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
		var resp = this.responseText;
		data = JSON.parse(resp);

		alert(JSON.stringify(data, null, 2));

		handleResponse(data);
		} else {
			// document.getElementById("demo").innerHTML = "Error on commodities receive " + this.readyState + " " + this.status;
		};
	}

	start = document.getElementById("shipconfiguration");
	stationInput = childById(start, "station");
	stationId = stationInput.getAttribute("stationid");
	systemInput = childById(start, "system");
	systemId = systemInput.getAttribute("systemid");

	var options = {};
	options.landingpad = document.getElementById('landingpad').value;
	options.jumprange = document.getElementById('jumprange').value;
	options.maxhops = document.getElementById('maxhops').value;
	options.currentStationId = stationId;
	options.currentSystemId = systemId;

	var data = {};
	data.options = options;
	data.cargohold = {};
	data.cargohold.cargospace = document.getElementById('cargospace').value;
	data.missions = [];

	for( missionLi of document.getElementById('missions').childNodes) {
		var mission = {};
		type = childById(missionLi, "type").value;
		if(type == "Intel") {
			mission.reward = childById(missionLi, "reward").value;
			mission.station = childById(missionLi, "station").value;
			mission.system = childById(missionLi, "system").value;
		}
		if(type == "Delivery") {
			reward = childById(missionLi, "reward").value;
			targetStationId = childById(missionLi, "station").getAttribute("systemid");
			amount = childById(missionLi, "amount").value;
			commodityId = childById(missionLi, "commodity").value;
			reward = childById(missionLi, "reward").value;

			mission = {"source":stationId, "target":targetStationId, "reward": reward, "commodity":commodityId, "amount":amount, "type":"deliver"};
		}
		if(type == "Source") {
			reward = childById(missionLi, "reward").value;
			amount = childById(missionLi, "amount").value;
			commodityId = childById(missionLi, "commodity").getAttribute("commodityid");

			mission = {"source":0, "target":stationId, "reward": reward, "commodity":commodityId, "amount":amount, "type":"Source"};
		}
		data.missions.push(mission);

	}

    alert(JSON.stringify(data, null, 2));
	// TODO http POST
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