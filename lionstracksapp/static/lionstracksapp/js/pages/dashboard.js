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

	//-------------All Charts -------------//
	$(function () {
		var initData = step_data[0].data;
		var chartMinDate = initData[0][0]; //first day
		var chartMaxDate = initData[initData.length-1][0];//last day
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

		$.plot($("#line-chart-payments"), step_data, options);
		$.plot($("#line-chart-distance"), distance_data, options);
		$.plot($("#line-chart-stairs"), stairs_data, options);

		$('select').multipleSelect({
			selectAll: false,
			placeholder: "Compare with other users",
			onClick: function(view) {
				//alert(view.label + '(' + view.value + ') ' + (view.checked ? 'checked' : 'unchecked'));
				if(view.checked) {//make ajax call and add selected data
					$.ajax({url: "/lionstracksapp/usermetricsdata/?userid="+view.value+"&username="+view.label, success: function(result){
						var data = JSON.parse(result);
						step_data.push(JSON.parse(data.step_data));
						distance_data.push(JSON.parse(data.distance_data));
						stairs_data.push(JSON.parse(data.stairs_data));

						//plot data
						$.plot($("#line-chart-payments"), step_data, options);
						$.plot($("#line-chart-distance"), distance_data, options);
						$.plot($("#line-chart-stairs"), stairs_data, options);
					}});
				} else {//remove selected data
					jQuery.each(step_data, function(i, val) {
						if(val.label == view.label) // delete index
						{
							step_data.splice(i,1);
							distance_data.splice(i,1);
							stairs_data.splice(i,1);
						}
					});
					//plot data
					$.plot($("#line-chart-payments"), step_data, options);
					$.plot($("#line-chart-distance"), distance_data, options);
					$.plot($("#line-chart-stairs"), stairs_data, options);
				}
			}
		});
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