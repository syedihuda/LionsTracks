//------------- Dashboard.js -------------//
$(document).ready(function() {

	//------------- Sparklines in header stats -------------//
	$('#spark-visitors').sparkline([5,8,10,8,7,12,11,6,13,8,5,8,10,11,7,12,11,6,13,8], {
		type: 'bar',
		width: '100%',
		height: '20px',
		barColor: '#dfe2e7',
		zeroAxis: false
	});

	//------------- Animated progressbars on tiles -------------//
	//animate bar only when reach the bottom of screen
	$('.animated-bar .progress-bar').waypoint(function(direction) {
		$(this).progressbar({display_text: 'none'});
	}, { offset: 'bottom-in-view' });
	
	//------------- CounTo for tiles -------------//
	$('.stats-number').countTo({
        speed: 1000,
        refreshInterval: 50
    });

    //------------- Flot charts -------------//

	//define chart colours first
	var chartColours = {
		blue: '#60b1cc',
		orange: '#cfa448',
		gray: '#bac3d2',
		red: '#df6a78',
		teal: '#43aea8',
		gray_lighter: '#e8ecf1',
		gray_light: '#777777',
		gridColor: '#bfbfbf'
	}

	//convert the object to array for flot use
	var chartColoursArr = Object.keys(chartColours).map(function (key) {return chartColours[key]});

	//generate random number for charts
	randNum = function(series){
		return (Math.floor( Math.random()* (1+10-1) + series));
	}

	randNumRange = function(min, max){
		return (Math.floor((Math.random() * max) + min));
	}

	//-------------Line chart STEPS -------------//
	$(function () {
		//some data

		var d1 = step_data;
		var d2 = [];
        var d3 = [];
		for (i = 0; i < d1.length-1; i++) {
		    //d1.push([new Date(Date.today().add(i).days().getTime()), i + randNum(10)]);
		    d2.push([d1[i][0], randNumRange(4000, 4010)]);
			d3.push([d1[i][0], randNumRange(9000, 9500)]);
		}

		var chartMinDate = d1[0][0]; //first day
    	var chartMaxDate = d1[d1.length-1][0];//last day

    	var tickSize = [1, "day"];
    	var tformat = "%d/%b";
		//var tformat = "%Y";

		var options = {
			grid: {
				show: true,
			    aboveData: true,
			    color: chartColours.gridColor,
			    labelMargin: 15,
			    axisMargin: 0,
			    borderWidth: 0,
			    borderColor:null,
			    minBorderMargin: 5,
			    clickable: true,
			    hoverable: true,
			    autoHighlight: true,
			    mouseActiveRadius: 20
			},
	        series: {
	        	grow: {active:true},
	            lines: {
            		show: true,
            		fill: false,
            		lineWidth: 2,
            		steps: false
	            },
	            curvedLines: {
                    apply: false,
                    active: true,
                    monotonicFit: true
                },
	            points: {show:false}
	        },
	        legend: {
	        	position: "ne",
	        	margin: [0,-25],
	        	noColumns: 0,
	        	labelBoxBorderColor: null,
	        	labelFormatter: function(label, series) {
				    // just add some space to labes
				    return '&nbsp;&nbsp;' + label + ' &nbsp;&nbsp;';
				},
				width: 30,
				height: 2
	    	},
	        yaxis: { min: 0 },
		    xaxis: {
		    	mode: "time",
	        	minTickSize: tickSize,
	        	timeformat: tformat,
	        	min: chartMinDate,
	        	max: chartMaxDate,
	        	tickLength: 0
		    },
	        colors: chartColoursArr,
        	shadowSize:1,
	        tooltip: true, //activate tooltip
			tooltipOpts: {
				content: "%s : %y.0",
				shifts: {
					x: -30,
					y: -50
				}
			}
	    };

    	$.plot($("#line-chart-payments"), [
    		{
    			label: "Syed",
    			data: d1,
    			//lines: {fillColor: chartColours.orange}
    		},
    		{
    			label: "Peer Group",
    			data: d2,
    			//lines: {fillColor: chartColours.gray}
    		},
            //{
    		//	label: "Columbia",
    		//	data: d3,
    		//	//lines: {fillColor: chartColours.teal}
    		//}

    	], options);

	});

	//-------------Line chart DISTANCE -------------//
	$(function () {
		//some data
		var d1 = distance_data;
		var d2 = [];
        var d3 = [];
		for (i = 0; i < d1.length-1; i++) {
		    //d1.push([new Date(Date.today().add(i).days().getTime()), i + randNum(10)]);
		    d2.push([d1[i][0], randNumRange(1000, 1010)]);
			d3.push([d1[i][0], randNumRange(1000, 1500)]);
		}

		var chartMinDate = d1[0][0]; //first day
    	var chartMaxDate = d1[d1.length-1][0];//last day

    	var tickSize = [1, "day"];
    	var tformat = "%d/%b";
		//var tformat = "%Y";

		var options = {
			grid: {
				show: true,
			    aboveData: true,
			    color: chartColours.gridColor,
			    labelMargin: 15,
			    axisMargin: 0,
			    borderWidth: 0,
			    borderColor:null,
			    minBorderMargin: 5,
			    clickable: true,
			    hoverable: true,
			    autoHighlight: true,
			    mouseActiveRadius: 20
			},
	        series: {
	        	grow: {active:true},
	            lines: {
            		show: true,
            		fill: false,
            		lineWidth: 2,
            		steps: false
	            },
	            curvedLines: {
                    apply: false,
                    active: true,
                    monotonicFit: true
                },
	            points: {show:false}
	        },
	        legend: {
	        	position: "ne",
	        	margin: [0,-25],
	        	noColumns: 0,
	        	labelBoxBorderColor: null,
	        	labelFormatter: function(label, series) {
				    // just add some space to labes
				    return '&nbsp;&nbsp;' + label + ' &nbsp;&nbsp;';
				},
				width: 30,
				height: 2
	    	},
	        yaxis: { min: 0 },
		    xaxis: {
		    	mode: "time",
	        	minTickSize: tickSize,
	        	timeformat: tformat,
	        	min: chartMinDate,
	        	max: chartMaxDate,
	        	tickLength: 0
		    },
	        colors: chartColoursArr,
        	shadowSize:1,
	        tooltip: true, //activate tooltip
			tooltipOpts: {
				content: "%s : %y.0",
				shifts: {
					x: -30,
					y: -50
				}
			}
	    };

    	$.plot($("#line-chart-distance"), [
    		{
    			label: "Syed",
    			data: d1,
    			//lines: {fillColor: chartColours.orange}
    		},
    		{
    			label: "Peer Group",
    			data: d2,
    			//lines: {fillColor: chartColours.gray}
    		},
            //{
    		//	label: "Columbia",
    		//	data: d3,
    		//	//lines: {fillColor: chartColours.teal}
    		//}

    	], options);

	});


	//-------------Line chart STAIRS -------------//
	$(function () {
		//some data
		var d1 = stairs_data;
		var d2 = [];
        var d3 = [];
		for (i = 0; i < d1.length-1; i++) {
		    //d1.push([new Date(Date.today().add(i).days().getTime()), i + randNum(10)]);
		    d2.push([d1[i][0], randNumRange(1, 4)]);
			d3.push([d1[i][0], randNumRange(1, 3)]);
		}

		var chartMinDate = d1[0][0]; //first day
    	var chartMaxDate = d1[d1.length-1][0];//last day

    	var tickSize = [1, "day"];
    	var tformat = "%d/%b";
		//var tformat = "%Y";

		var options = {
			grid: {
				show: true,
			    aboveData: true,
			    color: chartColours.gridColor,
			    labelMargin: 15,
			    axisMargin: 0,
			    borderWidth: 0,
			    borderColor:null,
			    minBorderMargin: 5,
			    clickable: true,
			    hoverable: true,
			    autoHighlight: true,
			    mouseActiveRadius: 20
			},
	        series: {
	        	grow: {active:true},
	            lines: {
            		show: true,
            		fill: false,
            		lineWidth: 2,
            		steps: false
	            },
	            curvedLines: {
                    apply: false,
                    active: true,
                    monotonicFit: true
                },
	            points: {show:false}
	        },
	        legend: {
	        	position: "ne",
	        	margin: [0,-25],
	        	noColumns: 0,
	        	labelBoxBorderColor: null,
	        	labelFormatter: function(label, series) {
				    // just add some space to labes
				    return '&nbsp;&nbsp;' + label + ' &nbsp;&nbsp;';
				},
				width: 30,
				height: 2
	    	},
	        yaxis: { min: 0 },
		    xaxis: {
		    	mode: "time",
	        	minTickSize: tickSize,
	        	timeformat: tformat,
	        	min: chartMinDate,
	        	max: chartMaxDate,
	        	tickLength: 0
		    },
	        colors: chartColoursArr,
        	shadowSize:1,
	        tooltip: true, //activate tooltip
			tooltipOpts: {
				content: "%s : %y.0",
				shifts: {
					x: -30,
					y: -50
				}
			}
	    };

    	$.plot($("#line-chart-stairs"), [
    		{
    			label: "Syed",
    			data: d1,
    			//lines: {fillColor: chartColours.orange}
    		},
    		{
    			label: "Peer Group",
    			data: d2,
    			//lines: {fillColor: chartColours.gray}
    		},
            //{
    		//	label: "Columbia",
    		//	data: d3,
    		//	//lines: {fillColor: chartColours.teal}
    		//}

    	], options);

	});

	//------------- Sparkline in payment received chart -------------//
	$('.spark-payments').sparkline([5,8,10,8,7,12,11,6,13,8,5,8,10,11,7,12,11,6,13], {
		type: 'bar',
		width: '100%',
		height: '20px',
		barColor: '#a8aeb7',
		zeroAxis: false
	});

	//------------- Montly sales goal chart -------------//
	var salesProgress = new ProgressBar.Circle('#sales-goal', {
	    color: '#47a877',
	    strokeWidth: 4,
	    fill: '#f1fcf7',
	    duration: 4000,
	    easing: 'bounce'
	});
	salesProgress.animate(0.7);
});