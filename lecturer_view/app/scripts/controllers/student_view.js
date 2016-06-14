app.controller('StudentViewCtrl', function($scope, $window, $location, $http){
  if (!$window.localStorage.token) {
    $location.path('/');
    return;
  }
  $scope.left_hover = false; 
  $scope.right_hover = false;
  $scope.current = false;
  $scope.toggle_follow = true;
  //fast/slow needs to get from backend not false
  $scope.fast_clicked = false;
  $scope.slow_clicked = false;

  $scope.backhome = function(){
    $location.path('/mainmenu');
  }
  var ctrl = $scope;

  $scope.ques = [];

  $scope.question = ''
  
  $scope.addQuestion = function() {
    $http.post('http://127.0.0.1:8000/slides/lecture/question/', $scope.question).success(function(data){
      $scope.update_question();
    });
    $scope.question = '';
  };

  $scope.upvote = function(pk) {
    $http.get('http://127.0.0.1:8000/slides/lecture/qvote/'+pk).success(function(data){
    });
  };
  $scope.update_question = function(){
    console.log('update q called')
    $http.get('http://127.0.0.1:8000/slides/lecture/get_page_questions/').success(function(data){
       $scope.ques = eval(data)
    });
  };
  $scope.happy = function(){
    return $http.get('http://127.0.0.1:8000/slides/lecture/vote_up/');
  };
  $scope.unhappy = function(){
    return $http.get('http://127.0.0.1:8000/slides/lecture/vote_down/');
  };
  $scope.check_speed = function(){
    $http.get('http://127.0.0.1:8000/slides/lecture/check_speed/').success(function(data){
       var st = eval(data);
       console.log(st);
       if(st == 0){
         ctrl.fast_clicked = false;
         ctrl.slow_clicked = false;
       }else if(st == 1){
         ctrl.fast_clicked = false;
         ctrl.slow_clicked = true;
       }else if(st == 2){
         ctrl.fast_clicked = true;
         ctrl.slow_clicked = false;
       }
    });
  };
  $scope.slow = function(){
    ctrl.slow_clicked = !ctrl.slow_clicked;
    if(ctrl.fast_clicked){
      ctrl.fast_clicked = false;
    }
    return $http.get('http://127.0.0.1:8000/slides/lecture/too_slow/');
  };
  $scope.fast = function(){
    ctrl.fast_clicked = !ctrl.fast_clicked;
    if(ctrl.slow_clicked){
      ctrl.slow_clicked = false;
    }
    return $http.get('http://127.0.0.1:8000/slides/lecture/too_fast/');
  };
  $scope.get_mood = function(){
    return $http.get('http://127.0.0.1:8000/slides/lecture/get_mood/');
  };
  $scope.curr = function(){
    return $http.get('http://127.0.0.1:8000/slides/lecture/get_curr_page/');
  };
  $scope.prev = function(){
    return $http.get('http://127.0.0.1:8000/slides/lecture/go_prev_page/');
  };
  $scope.next = function(){
    return $http.get('http://127.0.0.1:8000/slides/lecture/go_next_page/');
  };
  $scope.follow = function(){
    return $http.get('http://127.0.0.1:8000/slides/lecture/go_curr_page/');
  };
});
