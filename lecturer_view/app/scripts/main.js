console.log('asdf');
Mousetrap.bind(['right','space'], function() { alert('next page') });
Mousetrap.bind('left', function() { alert('previous page') });

var app = angular.module('lecture',[]);

app.factory('SharedData', function(){
  return { mainmenuHide: false };
});

app.controller('MenuController', function(SharedData){
  this.SharedData = SharedData;
  this.hover = false; 
  this.clicked = false;
  this.summ_hover  =false ;
  this.ques_hover  =false ;
  this.navi_hover  =false ;
  this.home_hover  =false ;
  this.close_hover =false ;
  this.ques = [{question: 'what happens if I fail?', votes: 10}, 
               {question: 'are labs open on bank holiday', votes: 8},
               {question: 'what happened to our coke machine', votes: 3}]
});



app.controller('SidesController', function(){
  this.left_hover = false; 
  this.right_hover = false;
});



app.controller('MainmenuController', ['$http', 'SharedData', function($http, SharedData){
  this.SharedData = SharedData;
  this.hide = false; 
  this.xs = [1,2,3,4,5];
  this.icon_hover = false;

  var ctrl = this;
  this.json = {'x':'nothing'};

  this.getjson = function(){
    $http.get('http://127.0.0.1:8000/slides/returnsomejson').success(function(data){
      ctrl.json = data;
    });
  };
}]);





app.directive('menuList', function(){
  return{
    restrict: 'E',
    templateUrl: 'ng_template/menu-list.html'
  };
});




var url ="http://127.0.0.1:8000/slides/getpdf";
//window.open(url);
console.log(url);
var maxPages = 0;
var scale = 1.5;
var canvas = document.getElementById('pdfviewer');
var context = canvas.getContext('2d');
var viewport = 0;
var renderContext = 0;
getPDF();
function getPDF() {
  PDFJS.disableWorker = true;
//  PDFJS.workerSrc = "scripts/pdf.worker.js";
  PDFJS.getDocument(url).then(function getPdfViewer(pdf) {
    // Fetch the first page
    maxPages = pdf.numPages;
    pdf.getPage(1).then(function getPageViewer(page) {
      viewport = page.getViewport(scale);
      // Prepare canvas using PDF page dimensions
      canvas.height = viewport.height;
      canvas.width = viewport.width;
      // Render PDF page into canvas context
      renderContext = {
        canvasContext: context,
        viewport: viewport
      };
     page.render(renderContext);
    });
//    checkmax();
  });
}
      


