app.controller('StudentViewCtrl', function($scope, $window, $location){
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

  $scope.addQuestion = function() {
    //function to add Question to database
    $scope.question = '';
  };

  $scope.upvote = function (index) {
    //upvote(index) <--upvote question in database
  };


  $scope.happy = false; //functions for votes
  //is it ^ or $scope.happy = function() {}
  $scope.unhappy = false;
  $scope.fast = false;
  $scope.slow = false;
});
