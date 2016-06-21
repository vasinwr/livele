'use strict';

app.controller('AuthCtrl', function ($scope, $location, $window, AuthService) {
  $scope.register = function () {
    var username = $scope.registerUsername;
    var password = $scope.registerPassword;

    if (username && password) {
      AuthService.register(username, password).then(
        function () {
          $location.path('/mainmenu');
        },
        function (error) {
          $scope.registerError = error;
        }
      );
    } else {
      $scope.registerError = 'Username and password required';
    }
  };

  $scope.login = function () {
    var username = $scope.loginUsername;
    var password = $scope.loginPassword;
  
    if (username && password) {
      AuthService.login(username, password).then(
        function () {
          if($window.localStorage.user_is_lec == 1){
            $location.path('/mainmenu');
          } else if($window.localStorage.user_is_lec == 0){
            $location.path('/student_mainmenu');
          }
        },
        function (error) {
          $scope.loginError = error;
        }
      );
    } else {
      $scope.error = 'Username and password required';
    }
  };

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

  $scope.to_clicker = function () {
    $location.path('/clicker_login');
  };
});
