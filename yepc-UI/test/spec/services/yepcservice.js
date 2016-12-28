'use strict';

describe('Service: yepcService', function () {

  // load the service's module
  beforeEach(module('yepcUiApp'));

  // instantiate service
  var yepcService;
  beforeEach(inject(function (_yepcService_) {
    yepcService = _yepcService_;
  }));

  it('should do something', function () {
    expect(!!yepcService).toBe(true);
  });

});
