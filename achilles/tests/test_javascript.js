var jsdom = require('jsdom').jsdom;
var assert = require('assert');
var jsc = require('jscoverage');

doc = jsdom('<html><body><div data-ablock="test"></div></body></html>');
window = doc.createWindow();

$ = require('jquery')(window);
jsc.require(module, '../static/js/achilles.js');

if (process.env.COVERAGE_REPORT) {
    process.on('exit', function () {
        jsc.coverage();
        jsc.coverageDetail();
    });
}


suite('Blocks', function() {
    setup(function() {
        achilles = window.Achilles('/endpoint/');
    });

    test('Find a block', function() {
        assert.equal(achilles.blocks('test').length, 1);
    });

    test('Get the correct one', function() {
        assert.deepEqual(achilles.blocks('test')[0], $('[data-ablock=test]')[0]);
    });
});
