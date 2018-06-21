var fs = require('fs');

// Some random image URLs.
var urls = [
  'https://www.memcachier.com/assets/logo.png',
  'https://blog.memcachier.com/2017/09/01/maglev-our-new-consistent-hashing-scheme/figure_12.png',
  'https://blog.memcachier.com/2017/07/17/aws-infrastructure-migration-results/avg-latency-us-east-1.png',
  'https://skybluetrades.net/dv/mediterranean-bathymetry-small.png',
  'https://skybluetrades.net/dv/enso-cartoons-small.png'
];

// Possible thumbnail sizes.
var sizes = ['64', '128', '256'];

exports.run = function() {
  // Pick a random image URL and size.
  var image_url = urls[Math.floor(Math.random() * urls.length)];
  var sz = sizes[Math.floor(Math.random() * sizes.length)];

  // Go to the index page and fill in the URL and size.
  browser.url('/');
  $('#id_image_url').setValue(image_url);
  $('#id_thumbnail_size').selectByValue(sz);

  // Submit form.
  var start = Date.now();
  $('input[type=submit]').click();

  // Check the result is OK.
  var total_time = Date.now() - start;
  expect($('h3').getText()).toBe('Thumbnail result');

  // Extract information and record.
  var url = $('#image-url').getText();
  var size = $('#thumbnail-size').getText();
  var duration = $('#processing-time').getText();
  var server = $('#server-name').getText();
  var res = url + ' ' + size + ' ' + server + ' ' + duration + ' ' + total_time + '\n';
  fs.appendFileSync('results.dat', res);
};
