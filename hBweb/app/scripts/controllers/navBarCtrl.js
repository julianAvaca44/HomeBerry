'use strict';

/**
 * @ngdoc function
 * @name hBwebApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the hBwebApp
 */
angular.module('hBwebApp')
	.controller('NavBarCtrl', function ($scope) {
	    $scope.demo = {
	        isOpen: false,
	        selectedDirection: 'left'
	    };
	});