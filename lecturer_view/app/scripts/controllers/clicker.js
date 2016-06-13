app.controller('ClickerCtrl', function($scope, $window, $location, $http, AuthService){
  if (!$window.localStorage.token) {
    $location.path('/clicker_login');
    return;
  }
  if ($window.localStorage.user_is_lec != 1) {
    AuthService.logout().then(
      function(){
        $location.path('/clicker_login');
      });
    return;
  }
  $scope.logout = function () {
    AuthService.logout().then(
      function () {
        $location.path('/');
      },
      function (error) {
        $scope.error = error;
      }
    );
  };
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
