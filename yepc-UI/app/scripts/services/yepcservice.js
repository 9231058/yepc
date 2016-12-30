'use strict';

/**
 * @ngdoc service
 * @name yepcUiApp.yepcService
 * @description
 * # yepcService
 * Service in the yepcUiApp.
 */
angular.module('yepcUiApp')
  .service('YepcService', function ($http) {
    // AngularJS will instantiate a singleton by calling "new" on this function

    this.tokenize = function (text) {
      return $http.post('/lex', text).then(function (response) {
        return response.data;
      });
    };

    this.parse = function (text) {
      return $http.post('/yacc', text).then(function (response) {
        return response.data;
      });
    };

    this.code = function (text) {
      return $http.post('/code', text).then(function (response) {
        return response.data;
      });
    };

    this.generate = function (text) {
      return $http.post('/generate', text).then(function (response) {
        return response.data;
      });
    };
  });
