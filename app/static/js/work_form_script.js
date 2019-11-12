function getTimeSlotInfo() {
    var x = document.getElementById("MonStart", "MonEnd" , "Monday").value;  
    //var y = document.getElementById("MonEnd").value;   
    //var z = Monday
    //document.getElementById("DisplayTimeSlot")= x, y, z;
	document.getElementById("DisplayTimeSlot").innerHTML = x;
	//document.getElementById("DisplayTimeSlot").innerHTML = y;
	//document.getElementById("DisplayTimeSlot").innerHTML = z;

}


function TimeSlot(start, end, day) {
    this.startTime = start;
    this.endTime = end;
    this.day = day;
}

function addTimeSlot(day, MonStart, MonEnd){
    var timeslots = new Array(n)
    for (var i=0; i<n;){
        timeslots[i] = new TimeSlot()
    }
    return timeslots
}

TimeSlot.prototype.toString = function TimeSlotToString() {
    return '' + this.start + '' +this.end+ '' + this.day;
}
var TimeSlot = {}
console.log()










/*
var TimeSlotMonday = [];
var TimeSlotTuesday = [];
var TimeSlotWednesday= [];
var TimeSlotThursday = [];
var TimeSlotFriday = [];
var TimeSlotSaturday = [];
var TimeSlotSunday = [];


var startTime = document.getElementById("startTime");
var valueSpan = document.getElementById("value");

startTime.addEventListener("input", function() {
  valueSpan.innerText = startTime.value;
}, false);


function addEventListener

//var timeslot = {};


function makeEmployeesObj(n) {
  var employees = {}
  for (var i = 0; i < n; ++i) {
    employees[i] = new Employee()
  }
  return employees
}



*/