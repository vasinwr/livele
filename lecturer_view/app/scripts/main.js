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
  this.right_click = function(){
    page_no += 1;
    getPDF();
  }

  this.left_click = function(){
    page_no -= 1;
    getPDF();
  }
});



app.controller('MainmenuController', ['$http', 'SharedData', function($http, SharedData){
  this.SharedData = SharedData;
  this.hide = false; 
  this.docs = {};
  this.xs = this.docs; //this.xs = lecutre_list().docs;
//this.xs = [{'pk': 6, 'filename': 'CH1'}, {'pk': 7, 'filename': 'BP'}]
  this.icon_hover = false;

  var ctrl = this;
  this.json = {'x':'nothing'};

  this.getlecture = function(key){
    console.log(key);
    console.log("blah")
    $http.get('http://127.0.0.1:8000/slides/select_lecture/'+key).success(function(data){
    //ctrl.json = data;
    });
    $http.get('http://127.0.0.1:8000/slides/get_pdf/').success(function(data){
    //ctrl.json = data;
    });
  };
  this.getjson = function(){
    $http.get('http://127.0.0.1:8000/slides/returnsomejson').success(function(data){
      ctrl.json = data;
    });
  };
  this.getleclist = function(name){
    console.log("a");
    $http.get('http://127.0.0.1:8000/slides/lecture_list/a').success(function(data){
     //console.log(ctrl.xs == eval(JSON.parse(data)));
     ctrl.xs = eval(JSON.parse(data));
     ctrl.docs = ctrl.xs;
    });
   };
  this.getpdf = function(){
    console.log("getpdf");
    getPDF();
  }
  }]);




/*
app.directive('menuList', function(){
  return{
    restrict: 'E',
    templateUrl: 'ng_template/menu-list.html'
  };
});
*/



var url ='http://127.0.0.1:8000/slides/get_pdf';
//window.open(url);
console.log(url);
var maxPages = 0;
var scale = 1.5;
var canvas = document.getElementById('pdfviewer');
var context = canvas.getContext('2d');
var viewport = 0;
var renderContext = 0;
var page_no = 1;
//getPDF();
function getPDF() {
  PDFJS.disableWorker = true;
//  PDFJS.workerSrc = "scripts/pdf.worker.js";
  PDFJS.getDocument(url).then(function getPdfViewer(pdf) {
    // Fetch the first page
    maxPages = pdf.numPages;
    pdf.getPage(page_no).then(function getPageViewer(page) {
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
      


