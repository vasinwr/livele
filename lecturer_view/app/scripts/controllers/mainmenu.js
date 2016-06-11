app.controller('MainmenuCtrl', function($scope, $http, $window, $location, AuthService){
 /* if (!$window.localStorage.token) {
    $location.path('/');
    return;
  }
  $scope.token = $window.localStorage.token;
  $scope.username = $window.localStorage.username;
  $scope.logout = function () {
    AuthService.logout().then(
      function () {
        $location.path('/');
      },
      function (error) {
        $scope.error = error;
      }
    );
  };
*/
  $scope.json = {'x': 'nothing'};
  $scope.lecture_list = [1, 2];
  $scope.icon_hover = false;

  var ctrl = $scope;

  $scope.getjson = function(){
    $http.get('http://127.0.0.1:8000/slides/returnsomejson/').success(function(data){
      ctrl.json = data;
    });
  };
  $scope.getleclist = function(name){
    $http.get('http://127.0.0.1:8000/slides/lecture_list/a').success(function(data){
     ctrl.lecture_list = eval(JSON.parse(data));
    });
   };
  $scope.select_slide = function(pk){
    // Derek: set database to save that this user picks this lecture(pk)
    console.log("slide selected");
      // this will jump to another html section with another controller so it will not know about this pk
      $location.path('/lecture');
  }

  $scope.course_list = [{'name':'cat'}, 
                        {'name':'turtle'}, 
                        {'name':'pizza'}];
  $scope.getcourses = function(){
    $http.get('http://127.0.0.1:8000/slides/course_list/').success(function(data){
     ctrl.course_list = data.courses;
    });
  }
  $scope.select_course = function(course){
    //TODO make api below
    $http.get('http://127.0.0.1:8000/slides/select_course/'+course).success(function(data){
     ctrl.lecture_list = data;
    });
  }
});

