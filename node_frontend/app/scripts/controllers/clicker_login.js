app.controller('ClickerLoginCtrl', function ($scope, $location, $window, AuthService) {

  $scope.login = function () {
    var username = $scope.loginUsername;
    var password = $scope.loginPassword;
  
    if (username && password) {
      AuthService.login(username, password).then(
        function () {
          $location.path('/clicker');
        },
        function (error) {
          $scope.loginError = error;
        }
      );
    } else {
      $scope.error = 'Username and password required';
    }
  };
});
