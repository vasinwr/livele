app.controller('StudentViewCtrl', function($scope, $window, $location, $http){
  if (!$window.localStorage.token) {
    $location.path('/');
    return;
  }
  $scope.left_hover = false; 
  $scope.right_hover = false;
  $scope.current = false;
  $scope.toggle_follow = true;

  $scope.backhome = function(){
    $location.path('/mainmenu');
  }

  $scope.ques = [];

  $scope.question = ""
  
  $scope.addQuestion = function() {
    $http.post('http://127.0.0.1:8000/slides/lecture/question/', $scope.question).success(function(data){
      $scope.update_question();
    });
    $scope.question = '';
  };

  $scope.upvote = function(pk) {
    $http.get('http://127.0.0.1:8000/slides/lecture/qvote/'+pk).success(function(data){
      $scope.update_question();
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
  $scope.get_mood = function(){
    return $http.get('http://127.0.0.1:8000/slides/lecture/get_mood/');
  };
  $scope.prev = function(){
    return $http.get('http://127.0.0.1:8000/slides/lecture/go_prev_page/');
  };
  $scope.next = function(){
    return $http.get('http://127.0.0.1:8000/slides/lecture/go_next_page/');
  };
  $scope.follow = function(){
    if ($scope.toggle_follow) {
      return $http.get('http://127.0.0.1:8000/slides/lecture/go_curr_page/');
    }
    else {
      return 0;
    }
  };
  $scope.fast = false;
  $scope.slow = false;
});
