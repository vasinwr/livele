"use strict";console.log("asdf"),Mousetrap.bind(["right","space"],function(){alert("next page")}),Mousetrap.bind("left",function(){alert("previous page")});var app=angular.module("lecture",[]);app.controller("MenuController",function(){this.hover=!1,this.clicked=!1,this.summ_hover=!1,this.ques_hover=!1,this.navi_hover=!1,this.home_hover=!1,this.close_hover=!1,this.ques=[{question:"what happens if I fail?",votes:10},{question:"are labs open on bank holiday",votes:8},{question:"what happened to our coke machine",votes:3}]}),app.directive("menuList",function(){return{restrict:"E",templateUrl:"ng_template/menu-list.html"}}),app.controller("SidesController",function(){this.left_hover=!1,this.right_hover=!1});