app.controller('LectureCtrl', function($scope, $window, $location, $http){
  if (!$window.localStorage.token) {
    $location.path('/');
    return;
  }
  if ($window.localStorage.user_is_lec != 1) {
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
  $scope.ques = [];

  $scope.slow = 0;
  $scope.fast = 0;
  $scope.audience = 0;
  $scope.fullscreen = false;

  var ctrl = $scope;
  $scope.update_question = function(){
    $http.get('http://127.0.0.1:8000/slides/lecture/show_questions/').success(function(data){
      ctrl.ques = eval(data)
    });
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
    return $http.get('http://127.0.0.1:8000/slides/lecture/go_prev_page/');
  };
  $scope.next = function(){
    return $http.get('http://127.0.0.1:8000/slides/lecture/go_next_page/');
  };
  $scope.get_mood = function(){
    return $http.get('http://127.0.0.1:8000/slides/lecture/get_mood/');
  };
  $scope.curr = function(){
    return $http.get('http://127.0.0.1:8000/slides/lecture/get_curr_page/');
  };
  $scope.goto_questions = function (){
    $location.path('/questions');
  };
  $scope.get_speed = function(){
    $http.get('http://127.0.0.1:8000/slides/lecture/get_speed/').success(function(data){
      var d = eval(data);
      ctrl.slow  = d.slow;
      ctrl.fast  = d.fast;
      ctrl.audience = d.audience;
    });
  }
  $scope.update_speed = function(slow,fast, audience){
    ctrl.slow = slow;
    ctrl.fast = fast; 
    ctrl.audience = d.audience;
  }
});
