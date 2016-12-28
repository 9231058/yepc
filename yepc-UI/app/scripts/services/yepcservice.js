'use strict';

/**
 * @ngdoc service
 * @name yepcUiApp.yepcService
 * @description
 * # yepcService
 * Service in the yepcUiApp.
 */
angular.module('yepcUiApp')
  .service('yepcService', function ($http) {
    // AngularJS will instantiate a singleton by calling "new" on this function

    this.parse = function (text) {
      $http.post('/yacc', text).then(function (response) {
      });
    };
  });
