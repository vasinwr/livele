app.controller('questionCtrl', function($scope, $http, $window, $location, AuthService){
  if (!$window.localStorage.token) {
    $location.path('/');
    return;
  }
  if ($window.localStorage.user_is_lec != 1) {
    $location.path('/');
    return;
  }

  $scope.questions = [];
  var ctrl = $scope;

  $scope.back = function(){
    $location.path('/lecture');
  };
  $scope.update_question = function(){
    console.log('update q called');
    $http.get('http://127.0.0.1:8000/slides/lecture/show_questions/').success(function(data){
      ctrl.questions = eval(data)
    });
  };
  $scope.delete_question = function(index){
    alert(index);
  }
});
