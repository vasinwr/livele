app.controller('StudentViewCtrl', function($scope, $window, $location, $http){
  if (!$window.localStorage.token) {
    $location.path('/');
    return;
  }
  $scope.left_hover = false; 
  $scope.right_hover = false;
  $scope.current = false;

  $scope.backhome = function(){
    $location.path('/mainmenu');
  }

  $scope.ques = [{question: 'Question 1', votes: 10}, 
               {question: 'Question 2', votes: 8},
               {question: 'Question 3', votes: 3}];

  $scope.question = ""
  
  $scope.addQuestion = function() {
    $http.post('http://127.0.0.1:8000/slides/lecture/question/', $scope.question).success(function(data){

    });
    $scope.question = '';
  };

  $scope.upvote = function (index) {
    //upvote(index) <--upvote question in database
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
  $scope.fast = false;
  $scope.slow = false;
});
