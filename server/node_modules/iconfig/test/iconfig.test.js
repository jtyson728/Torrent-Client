/*!
 * response-patch - lib/iconfig.test.js
 * Author: jifeng <wade428@163.com>
 */

"use strict";

/**
 * Module dependencies.
 */

var iconfig = require('../');
var path = require('path');
var should = require('should');

var config = {
  switchs : false
}

//在服务器端 switchs: true
var client = iconfig({
  config: config,
  iservice: {
    host: '10.232.13.90',
    cache: path.join(process.env.HOME, 'config_cache')
  },
  appname:'iconfig'
});

describe('iconfig', function () {
  before(function (done) {
    client.ready(function () {
      done();
    })
  });
  it('normal sync config', function () {
    config.switchs.should.be.true;
  });

  it('check ready ok', function (done) {
    client.ready(function () {
      done();
    });
  });

});