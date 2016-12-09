angular
.module('capitalsApp', [])
.controller(
		'listController',
		function($scope, $sce, $http, $anchorScroll) {
			var search = this;
			$scope.capitals = []
			$scope.listedCapitals = []
			$scope.allCapitals = []
			$scope.maxListed = 20
			$scope.cursorPosition = 0
			$scope.trustSrc = function(src) {
			    return $sce.trustAsResourceUrl(src);
			};

			$scope.updateTable = function() {
				var $url = "https://capital-service-dot-hackathon-team-015.appspot.com/api/capitals/all"
				//var $url = "http://localhost:8080/api/capitals/all"
				$http.get($url).then(function(response) {
					var distinct = []
					var array = response.data
					var distinctCountries = [] 

					for (var i = 0; i < array.length; i++)
						if (distinct.indexOf(array[i].country) == -1)
						{
							distinct.push(array[i].country)
							array[i].mapurl = "https://maps.google.com/maps?q=" + array[i].location.latitude + "," + array[i].location.longitude + "&hl=es&z=4&output=embed"
							distinctCountries.push(array[i])
						}
						
						distinctCountries.sort(function(a, b){
							if(a.country < b.country) return -1;
							if(a.country > b.country) return 1;
							return 0;
						});

						$scope.allCapitals = distinctCountries
						$scope.updateView();
				});
			}
			
			$scope.updateView = function()
			{
				var $endPosition = $scope.cursorPosition + $scope.maxListed
				if($endPosition >= $scope.allCapitals.length)
				{
					$endPosition = $scope.allCapitals.length - 1
				}

				$scope.capitals = $scope.allCapitals.slice($scope.cursorPosition, $endPosition)
				$anchorScroll()
			}

			$scope.nextPage = function()
			{
				$scope.cursorPosition = $scope.cursorPosition + 20
				if($scope.cursorPosition >= $scope.allCapitals.length)
				{
					$scope.cursorPosition = $scope.allCapitals.length - 1
				}

				$scope.updateView()
			}

			$scope.previousPage = function()
			{
				$scope.cursorPosition = $scope.cursorPosition - 20
				if($scope.cursorPosition < 0)
				{
					$scope.cursorPosition = 0
				}
				
				$scope.updateView()
			}
			

			$scope.updateTable();
			$scope.updateView();
		});

angular
.module('mapsApp', [])
.controller(
		'mapsController',
		function($scope, $sce, $http) {
			var search = this;
			$scope.capitals = []
			$scope.updateCapitals = function() {
				var $url = "https://capital-service-dot-hackathon-team-015.appspot.com/api/capitals/all"
				//var $url = "http://localhost:8080/api/capitals/all"
				$http.get($url).then(function(response) {
					var distinct = []
					var array = response.data
					var distinctCountries = [] 
					for (var i = 0; i < array.length; i++)
						if (distinct.indexOf(array[i].country) == -1)
						{
							distinct.push(array[i].country)
							array[i].mapurl = "https://maps.google.com/maps?q=" + array[i].location.latitude + "," + array[i].location.longitude + "&hl=es&z=4&output=embed"
							distinctCountries.push(array[i])
							var marker = document.createElement("google-map-marker");
							var latitude = document.createAttribute("latitude");
							latitude.value = array[i].location.latitude;
							marker.setAttributeNode(latitude);
							var longitude = document.createAttribute("longitude");
							longitude.value = array[i].location.longitude;
							marker.setAttributeNode(longitude);
							var title = document.createAttribute("title");
							title.value = array[i].name;
							marker.setAttributeNode(title);
							Polymer.dom(document.getElementById("googleMaps")).appendChild(marker);
						}
						
						distinctCountries.sort(function(a, b){
							if(a.country < b.country) return -1;
							if(a.country > b.country) return 1;
							return 0;
						});

						$scope.capitals = distinctCountries
				});
			}
			$scope.updateCapitals();
		});