'use strict';

app.factory('AuthService', function ($http, $q , $window , API_SERVER) {

  var authenticate = function (username, password, endpoint) {
    var deferred = $q.defer();
    var url = API_SERVER + endpoint;
    
    $http.post(url, 'username=' + username + '&password=' + password, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }).then(
      function (response) {
        var token = response.data.token;
        var username = response.data.username;

        var user_is_lec = response.data.user_is_lec;
    
        if (token && username) {
          $window.localStorage.token = token;
          $window.localStorage.username = username;
          $window.localStorage.user_is_lec = user_is_lec;
          deferred.resolve(true);
        } else {
          deferred.reject('Invalid data received from server');
        }
      },
      function (response) {
        deferred.reject(response.data.error);
      }
    );
    return deferred.promise;
  };

  var logout = function () {
    var deferred = $q.defer();
    var url = API_SERVER + 'logout/';
  
    $http.post(url).then(
      function () {
        $window.localStorage.removeItem('token');
        $window.localStorage.removeItem('username');
        $window.localStorage.removeItem('user_is_lec');
        deferred.resolve();
      },
      function (error) {
        deferred.reject(error.data.error);
      }
    );
    return deferred.promise;
  };

  return {
    register: function (username, password) {
      return register(username, password, 'register/');
    },
     login: function (username, password) {
      return authenticate(username, password, 'login/');
    },
    logout: function () {
      return logout();
    }
  };


});
