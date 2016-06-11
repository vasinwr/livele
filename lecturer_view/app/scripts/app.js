var app = angular.module('frontendApp',[
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ngRoute'
]);

app.config(['$routeProvider','$httpProvider', function($routeProvider, $httpProvider) {
  $httpProvider.interceptors.push('AuthInterceptor');
  $routeProvider
    .when('/', {
      templateUrl: 'views/auth.html',
      controller: 'AuthCtrl'
    })
    .when('/mainmenu', {
      templateUrl: 'views/mainmenu.html',
      controller: 'MainmenuCtrl'

    })
    .when('/lecture', {
      templateUrl: 'views/lecture.html',
      controller: 'LectureCtrl'
    })
    .when('/student', {
      templateUrl: 'views/student_view.html',
      controller: 'StudentViewCtrl'
    })
    .otherwise({
      redirectTo: '/'
    });
}]);

app.constant('API_SERVER', 'http://127.0.0.1:8000/slides/api/');
