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
        // jsc.coverageDetail();
    });
}


// mock helper function
function mock(return_value) {
    var res = function() {
        res.called += 1;
        res.args = Array.prototype.slice.call(arguments);;
        return return_value;
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


    // loadInto method
    suite('Load', function() {
        test('loadInto adds target attributes', function() {
            $('body').append($('<div id="test"></div>'));

            achilles.update = mock();
            achilles.loadInto($('#test'), 'blockname');

            assert.equal($('#test').attr('data-ablock'), 'blockname');
            assert.equal(achilles.update.called, 1);
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


suite('Actions', function() {

    // Action calling
    suite('Call', function() {
        test('Send an action', function() {
            achilles.transport.send = mock({error: function(){}});
            action = achilles.action('test', [2, 'args'], { kw: 'args'});

            assert.equal(achilles.transport.send.called, 1);
        });

        test('Process action results', function() {
            achilles.transport.send = mock({error: function(){}});
            action = achilles.action('test', [2, 'args'], { kw: 'args'});
            action_id = achilles._actions.pending.indexOf(action);

            var res = 0;
            action.done(function (data) {
                res = data;
            });

            actions = [];
            actions[action_id] = {'value': 3};
            achilles.processResponse({'actions': actions});

            assert.equal(res, 3);
        });

        test('Process action error result', function() {
            achilles.transport.send = mock({error: function(){}});
            action = achilles.action('test', [2, 'args'], { kw: 'args'});
            action_id = achilles._actions.pending.indexOf(action);

            var exception, message;
            action.fail(function (ex, msg) {
                exception = ex;
                message = msg;
            });

            actions = [];
            actions[action_id] = {error: 'IndexError', message: 'sorry'};
            achilles.processResponse({'actions': actions});

            assert.equal(exception, 'IndexError');
            assert.equal(message, 'sorry');
        });
    });
});



suite('Console', function() {
    // Server response processing
    test('Process server response', function() {
        m = mock();
        old_log = console.log; console.log = m;
        achilles.processResponse({
            'console': [
                'Miau miau miau',
            ]
        });
        console.log = old_log;

        assert.equal(m.called, 1);
        assert.equal(m.args[0], 'Miau miau miau');
    });
});
