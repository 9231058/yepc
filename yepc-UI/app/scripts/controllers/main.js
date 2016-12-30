'use strict';

/**
 * @ngdoc function
 * @name yepcUiApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the yepcUiApp
 */
angular.module('yepcUiApp')
.controller('MainCtrl', function ($scope, YepcService) {
  $scope.tokenize = function () {
    YepcService.tokenize($scope.source).then(function (data) {
      $scope.tokens = data;
    });
  };

  $scope.toC = function () {
    YepcService.code($scope.source).then(function (data) {
      $scope.cSource = data;
    });
  };

  $scope.generate = function () {
    YepcService.generate($scope.source).then(function (data) {
      var downloadLink = angular.element('<a></a>');
      downloadLink.attr('href', 'download/' + data);
      downloadLink[0].click();
    });
  };

  $scope.fromFile = function () {
    var file = document.getElementById('file').files[0];
    var reader = new FileReader();
    reader.onload = function (e) {
      $scope.source = e.target.result;
    };
    if (file) {
      reader.readAsText(file);
    }
  };
});
