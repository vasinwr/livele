app.controller('LectureCtrl', function($scope, $window, $location){
  if (!$window.localStorage.token) {
    $location.path('/');
    return;
  }
  $scope.left_hover = false; 
  $scope.right_hover = false;

  $scope.hover = false; 
  $scope.clicked = false;
  $scope.summ_hover  =false ;
  $scope.ques_hover  =false ;
  $scope.navi_hover  =false ;
  $scope.home_hover  =false ;
  $scope.close_hover =false ;
  $scope.ques = [{question: 'what happens if I fail?', votes: 10}, 
               {question: 'are labs open on bank holiday', votes: 8},
               {question: 'what happened to our coke machine', votes: 3}]

  $scope.backhome = function(){
    $location.path('/mainmenu');
  }
});
