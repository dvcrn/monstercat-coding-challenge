var app = angular.module('monstercat', ["highcharts-ng"]);

function MainController ($scope) {
	// Using defers to wait for 3 parallel ajax requests
	var defers = [];
	var config = [
		{'url': 'api/albums.json', 'key': 'albums', 'title': 'Albums'},
		{'url': 'api/singles.json', 'key': 'singles', 'title': 'Singles'},
		{'url': 'api/streaming.json', 'key': 'streaming', 'title': 'Streaming'},
	]

	var chart_data = {};
	for (var i = 0; i < config.length; i++) {
		var conf = config[i];

		// Bind current config row to function
		(function (config) {
			defers.push($.get(config['url'], function (data) {
				config['data'] = data;
				chart_data[config.key] = config;
			}));
		})(conf);
	}

	// Wait for all defers to finish loading
	$.when.apply($, defers).done(function () {
		console.info('all finished');
		console.info(chart_data);

		for (key in chart_data) {
			var series_data = [];

			// Sort the array
			var keys = Object.keys(chart_data[key].data)
			keys.sort();

			for (i = 0; i < keys.length; i++) {
			    var date = keys[i];
			    series_data.push([date * 1000, chart_data[key].data[date]]);
			}

			$scope.chartConfig.series.push({'data': series_data, name: chart_data[key].title});
		}

		// Remove loading indicator and ping angularjs to refresh frontend
		$scope.chartConfig.loading = false;
		$scope.$digest();
	});

	$scope.chartConfig = {
        options: {
            chart: {
                type: 'spline'
            }
        },
        series: [],
        title: {
            text: 'Monstercat Sales Over Time'
        },

        loading: true,

        xAxis: {
         	type: "datetime",
            dateTimeLabelFormats: {
                month: '%e. %b',
                year: '%b'
            }
        }
    }
}