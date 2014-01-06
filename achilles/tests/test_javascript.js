var jsdom = require('jsdom').jsdom;
var assert = require('assert');
var jsc = require('jscoverage');

doc = jsdom('<html><body></body></html>');
window = doc.createWindow();

$ = require('jquery')(window);
jsc.require(module, '../static/js/achilles.js');

if (process.env.COVERAGE_REPORT) {
    process.on('exit', function () {
        jsc.coverage();
        jsc.coverageDetail();
    });
}


// mock helper function
function mock() {
    var res = function() {
        res.called += 1;
        res.args = Array.prototype.slice.call(arguments);;
    }
    res.called = 0;

    return res;
};

setup(function() {
    achilles = window.Achilles('/endpoint/');
});

teardown(function() {
    $('body').empty();
});


suite('Core', function() {
    suite('processResponse', function() {
        test('Ignores unknown controllers', function() {
            // Temporary disable error log
            old_error = console.error; console.error = function() {};

            achilles.processResponse({ 'foo': [] });

            console.error = old_error;
        });

        test('Calls registered controllers', function() {
            var controller = {
                process: function(achilles, data) {
                    assert.equal(data, 3);
                }
            };
            achilles.registerController('foo', controller);
            achilles.processResponse({ 'foo': 3 });
        });
    });

    suite('JSONTransport', function() {
    });
});


suite('Blocks', function() {
    // DOM lookup helpers
    suite('Lookup', function() {
        test('Find a block', function() {
            $('body').append($('<div data-ablock="test"></div>'));
            assert.equal(achilles.block('test').length, 1);
            assert.deepEqual(achilles.block('test')[0], $('[data-ablock=test]')[0]);
        });

        test('Find more than one block', function() {
            $('body').append($('<div data-ablock="test"></div>'));
            $('body').append($('<div data-ablock="test"></div>'));
            $('body').append($('<div data-ablock="test"></div>'));
            assert.equal(achilles.blocks('test').length, 3);
        });
    });


    // blocks:update remote action calling
    suite('Update', function() {
        test('Update one block', function() {
            $('body').append($('<div data-ablock="test"></div>'));

            achilles.action = mock();
            achilles.update('test');

            assert.equal(achilles.action.called, 1);
            assert.equal(achilles.action.args[0], 'blocks:update');
        });

        test('Update more than one block', function() {
            $('body').append($('<div data-ablock="test"></div>'));
            $('body').append($('<div data-ablock="test"></div>'));

            achilles.action = mock();
            achilles.update('test');

            assert.equal(achilles.action.called, 2);
        });
    });


    // Server response processing
    suite('Process response', function() {
        test('Simple block update', function() {
            $('body').append($('<div data-ablock="test"></div>'));
            achilles.processResponse({
                'blocks': [
                    {'name': 'test', 'args': [], 'kwargs': {}, 'data': 'Hello'},
                ]
            });

            assert.equal(achilles.block('test').html(), 'Hello');
        });
    });
});
