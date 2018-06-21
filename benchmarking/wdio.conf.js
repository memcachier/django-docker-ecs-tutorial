// In order to run test specs in parallel in webdriver.io, they need
// to be in separate spec files.  This is something of an abuse of the
// test system, but here we make copies of a single test spec file to
// run a set of random benchmark tests in parallel.  The work of the
// test is done in the run.js file, which is imported by the test
// template (template.js) that we copy to make spec files.  It's a
// little nasty, but it works...

var fs = require('fs');
var rl = require('readline');
var util = require('util');

// URL for accessing thumbnailer.
var thumbnailer_url = process.env.TEST_URL || 'http://localhost:8000';

// Run 100 tests, using browser instances in parallel as far as
// possible.
var ntests = 100;

// Indexed test spec file name.
function spec_file(i) { return './benches/run' + i + '.js'; }

// Clean test spec directory.
function clean_specs() {
  for (var i = 1; i <= ntests; ++i) {
    if (fs.existsSync(spec_file(i))) { fs.unlinkSync(spec_file(i)); }
  }
}

// Post process results.
function post_process() {
  console.log('post_process:');
  var results = {};
  var lines = fs.readFileSync('results.dat', 'utf8').split('\n');
  for (var i in lines) {
    var line = lines[i].trim();
    if (line !== '') {
      var flds = line.split(' ');
      var k = flds[0] + ':' + flds[1];
      var data = { server: flds[2],
                   tserver: parseInt(flds[3], 10),
                   ttotal: parseInt(flds[4], 10) };
      if (results[k])
        results[k].push(data);
      else
        results[k] = [data];
    }
  }
  fs.writeFileSync('results.json', util.format(results));
  fs.unlinkSync('results.dat');
}

exports.config = {
  specs: [ './benches/*.js' ],
  maxInstances: 10,
  capabilities: [{ browserName: 'firefox',
                   "moz:firefoxOptions": { args: ['-headless'] }}],
  sync: true,
  logLevel: 'silent',
  coloredLogs: true,
  deprecationWarnings: true,
  bail: 0,
  screenshotPath: './errorShots/',
  baseUrl: thumbnailer_url,
  waitforTimeout: 10000,
  connectionRetryTimeout: 90000,
  connectionRetryCount: 3,
  services: ['selenium-standalone'],
  framework: 'jasmine',
  jasmineNodeOpts: {
    defaultTimeoutInterval: 10000,
    expectationResultHandler: function(passed, assertion) { }
  },
  onPrepare: function (config, capabilities) {
    // Clean results file.
    if (fs.existsSync('results.dat')) { fs.unlinkSync('results.dat'); }

    // Create test specs for parallel test running.
    clean_specs();
    if (!fs.existsSync('benches')) { fs.mkdirSync('benches'); }
    for (var i = 1; i <= ntests; ++i) {
      fs.copyFileSync('template.js', spec_file(i));
    }
  },

  onComplete: function (exitCode, config, capabilities) {
    clean_specs();
    post_process();
  }
};
