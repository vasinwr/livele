app.controller('questionCtrl', function($scope, $http, $window, $location, AuthService){
  if (!$window.localStorage.token) {
    $location.path('/');
    return;
  }
  if ($window.localStorage.user_is_lec != 1) {
    $location.path('/');
    return;
  }
  $scope.questions = [1,2,3];
  $scope.back = function(){
    $location.path('/lecture');
  }
});
