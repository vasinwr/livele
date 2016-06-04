console.log('asdf');
Mousetrap.bind(['right','space'], function() { alert("next page") });
Mousetrap.bind('left', function() { alert("previous page") });

var app = angular.module('lecture',[]);
app.controller('MenuController', function(){
  this.x = 123; 
  this.menu_clicked = false;
});
