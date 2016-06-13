app.controller('ClickerCtrl', function($scope, $window, $location, $http){
  $scope.next = function () {
    $http.get('http://127.0.0.1:8000/slides/clicker_next/');
  };
  $scope.prev = function () {
    $http.get('http://127.0.0.1:8000/slides/clicker_prev/');
  };
  $scope.menu = function () {
    $http.get('http://127.0.0.1:8000/slides/clicker_menu/');
  };
});
