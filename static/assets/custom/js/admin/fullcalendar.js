$(document).ready(function() {

    var date = new Date();
	var d = date.getDate();
	var m = date.getMonth();
	var y = date.getFullYear();

	/* initialize the calendar
	-----------------------------------------------------------------*/
	
	var calendar =  $('#calendar').fullCalendar({
		header: {
			left: 'title',
			center: 'agendaDay,agendaWeek,month',
			right: 'prev,next today'
		}
	});
	
});
