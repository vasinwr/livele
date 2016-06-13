app.controller('LectureCtrl', function($scope, $window, $location, $http){
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
               {question: 'what happened to our coke machine', votes: 3}];

  var ctrl = $scope;
  $scope.update_question = function(questions){
    //TODO: questions received from websocket message (top 3 questions)
    ctrl.ques = questions;
  };
  $scope.update_summary = function(summary){
    //TODO: summary received from websocket message 
    ctrl.summary = summary;
  };
  $scope.backhome = function(){
    $location.path('/mainmenu');
  };
  $scope.click = function(summary){
    //TODO: summary received from websocket message 
    ctrl.clicked = true;
  };
  $scope.prev = function(){
    return $http.get('http://127.0.0.1:8000/slides/lecture/go_prev_page/')
  };
  $scope.next = function(){
    return $http.get('http://127.0.0.1:8000/slides/lecture/go_next_page/')
  };
});
