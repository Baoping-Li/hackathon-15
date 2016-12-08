angular
.module('capitalsApp', [])
.controller(
		'listController',
		function($scope, $sce, $http) {
			var search = this;
			$scope.capitals = []
			$scope.trustSrc = function(src) {
			    return $sce.trustAsResourceUrl(src);
			}
			$scope.updateTable = function($name) {
				var $url = "https://capital-service-dot-hackathon-team-015.appspot.com/api/capitals"
				$http.get($url).then(function(response) {
					var distinct = []
					var array = response.data
					var distinctCountries = [] 

					for (var i = 0; i < array.length; i++)
						if (distinct.indexOf(array[i].country) == -1)
						{
							distinct.push(array[i].country)
							array[i].mapurl = "https://maps.google.com/maps?q=" + array[i].location.latitude + "," + array[i].location.longitude + "&hl=es;z=14&output=embed"
							distinctCountries.push(array[i])
						}
						
						distinctCountries.sort(function(a, b){
							if(a.country < b.country) return -1;
							if(a.country > b.country) return 1;
							return 0;
						});

						$scope.capitals = distinctCountries
				});
			};
			$scope.updateTable();
		});

