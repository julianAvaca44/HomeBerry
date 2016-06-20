'use strict';

/**
 * @ngdoc overview
 * @name hBwebApp
 * @description
 * # hBwebApp
 *
 * Main module of the application.
 */
angular
  .module('hBwebApp', [
    'ngAnimate',
    'ngAria',
    'ngCookies',
    'ngMessages',
    'ngResource',
    'ngSanitize',
    'ngMaterial',
    'ui.router'
  ])
  .config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise("/HomeBerry");
    $stateProvider
        .state('main', {
            abstract: true,
            url: "/HomeBerry",
            views:{
                "navBar":{
                  templateUrl: "../views/navBar.html",
                  controller: "NavBarCtrl"
                },
                "body":{
                  templateUrl: "../views/main.html",
                  controller: "MainCtrl"
                },
                "footer": {
                  templateUrl: "../views/footer.html"
                }
            } 
        })
        .state('main.home', {
          url: '',
          views: {
              '@main': {
                  templateUrl: "../views/home.html"
              }
            }
          })
        .state('main.devices', {
          url: '/devices',
          views: {
              '@main': {
                  templateUrl: "../views/devices.html"
              }
            }
          });
  });
