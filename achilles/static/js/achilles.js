/*
 * Achilles - Django AJAX framework
 *
 * This file provides the javascript framework to communicate with
 * Django Achilles backend
 *
 */
(function(window) {

    // Make sure jquery is in the correct namespace
    var $ = window.jQuery;

    /* CORE */

    // Main constructor
    var Achilles = function(endpoint) {
        return new Achilles.fn.init(endpoint);
    };

    Achilles.fn = Achilles.prototype = {

        // Init achilles instance, set the server endpoint URL
        init: function(endpoint) {
            this.transport = new JSONTransport(this, endpoint);

            // Init controllers for this instance
            for (c in this.controllers) {
                controller = this.controllers[c];
                if (controller.init) controller.init(this);
            }
            return this;
        },


        // Response controllers
        controllers: {},

        // Register a response controller
        //     key - key from the response data to pass to this controller
        //     controller - the controller itself
        registerController: function(key, controller) {
            this.controllers[key] = controller;
        },


        // Process a message from the server
        processResponse: function(data) {
            for (c in data) {
                if (!(c in this.controllers)) {
                    console.error("Unknown controller " + c);
                    continue;
                }

                // Let the controller process its data
                var controller = this.controllers[c];
                controller.process(this, data[c]);
            }
        },
    };

    Achilles.fn.init.prototype = Achilles.fn;


    /* JSON TRANSPORT */
    /* Default messages transport, using JQuery.ajax */
    function JSONTransport(achilles, endpoint) {
        this.endpoint = endpoint;
        this.achilles = achilles;
    }

    JSONTransport.fn = JSONTransport.prototype = {
        // Send the given message to the server
        send: function(msg) {
            // Server processes array of dicts
            if (!(msg instanceof Array)) msg = [msg];

            var _achilles = this.achilles;
            return $.ajax({
                url: this.endpoint,
                crossDomain: false,
                type: 'POST',
                beforeSend: this.setCSRFHeader,
                data: JSON.stringify(msg),
            })
            // Send success data back to achilles
            .success(function(data) {
                _achilles.processResponse(data)
            });
        },

        setCSRFHeader: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
    };

    // getCookie helper
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }



    /* ACTIONS */

    // Register the response controller
    var actions_controller = {

        init: function(achilles) {
            // Actions metadata
            achilles._actions = {
                count: 0,
                pending: Array(),
                error_observers: Array(),
            }
        },

        process: function(achilles, actions) {
            for (action_id in actions) {
                var action_deferred = achilles._actions.pending[action_id];
                var result = actions[action_id];
                if (result.error) {
                    action_deferred.reject(result.error,
                                           result.message,
                                           result.trace);

                    for (cb in achilles._actions.error_observers) {
                        cb = achilles._actions.error_observers[cb];
                        cb(result.error, result.message, result.trace);
                    }
                }
                else {
                    action_deferred.resolve(result.value);
                }

                // Already processed, forget it:
                delete achilles._actions.pending[action_id];
            }
        },
    };

    // Register an error observer
    Achilles.fn.onError = function(callback) {
        this._actions.error_observers.push(callback);
    }

    // Remote action call
    Achilles.fn.action = function(name, args, kwargs) {
        // Save action deferred to trigger it when the response comes
        var action_id = this._actions.count++;
        var action_deferred = $.Deferred();
        this._actions.pending[action_id] = action_deferred;

        // Launch the action
        this.transport.send({
            name: name,
            id: action_id,
            args: args,
            kwargs: kwargs
        }).error(function(jqXHR, textStatus) {
            // Reject in case of ajax error
            action_deferred.reject('TransportError', textStatus);
            for (cb in achilles._actions.error_observers) {
                cb = achilles._actions.error_observers[cb];
                cb('TransportError', textStatus);
            }
        });

        return action_deferred;
    };

    // Register the controller
    Achilles.fn.registerController('actions', actions_controller);



    /* BLOCKS */

    // Register the response controller
    var blocks_controller = {
        init: function(achilles) {
            achilles.block_updaters = {
                HTML: function (block, data) {
                    block.html(data)
                },
            };

            // load lazy blocks
            var lazyblocks = $('[data-ablock][data-ablock-lazy]');
            achilles.update(lazyblocks);
        },

        process: function(achilles, data) {
            for (b in data) {
                var block = data[b];
                var updater = achilles.block_updaters[block.updater || 'HTML'];
                var blocks = achilles.blocks(block.name, block.args, block.kwargs);
                updater(blocks, block.data);
            }
        },
    };

    // Look for blocks matching the given criteria
    Achilles.fn.blocks = function(name, args, kwargs) {
        var blocks = $('[data-ablock]');

        if (name) blocks = blocks.filter('[data-ablock="'+name+'"]');

        if (args) {
            blocks = blocks.filter(function(index) {
                bargs = $.parseJSON(blocks.attr('data-ablock-args') || '[]');
                for (k in args) {
                    if (args[k] !== bargs[k]) return false;
                }
                return true;
            });
        }

        if (kwargs) {
            blocks = blocks.filter(function(index) {
                bkwargs = $.parseJSON(blocks.attr('data-ablock-kwargs') || '{}');
                for (k in kwargs) {
                    if (kwargs[k] !== bkwargs[k]) return false;
                }
                return true;
            });
        }

        return blocks;
    };

    // Look for the block matching the given criteria
    Achilles.fn.block = function(name, args, kwargs) {
        return this.blocks(name, args, kwargs).first();
    };

    // Update the given blocks
    Achilles.fn.update = function(blocks) {
        var _achilles = this;
        blocks.each(function(block) {
            var name = $(this).attr('data-ablock');
            var args = $.parseJSON($(this).attr('data-ablock-args') || '[]');
            var kwargs = $.parseJSON($(this).attr('data-ablock-kwargs') || '{}');
            _achilles.action('blocks:update', [name].concat(args), kwargs)
        });
    };

    // Load a block into the given element, if the given element is not a block,
    // this method will convert it to one
    Achilles.fn.loadInto = function(block, name, args, kwargs) {
        // Prepare the element wrapper
        block.attr('data-ablock', name);
        if (args) block.attr('data-ablock-args', JSON.stringify(args));
        if (kwargs) block.attr('data-ablock-kwargs', JSON.stringify(kwargs));

        // Call for update
        this.update(block);
    };

    // Register the controller
    Achilles.fn.registerController('blocks', blocks_controller);


    /* LOGS */

    var console_controller = {

        process: function(achilles, logs) {
            // Avoid unsupported browsers
            if (!window.console) return;

            for (i in logs) {
                console.log(logs[i]);
            }
        },
    };

    // Register the controller
    Achilles.fn.registerController('console', console_controller);


    /* REDIRECT */

    var redirect_controller = {

        process: function(achilles, redirect) {
            if (redirect.url) {
                window.location.href = redirect.url;
            }
        },
    };

    // Register the controller
    Achilles.fn.registerController('redirect', redirect_controller);


    /* MESSAGES */

    var messages_controller = {

        init: function(achilles) {

            // Default message implementation
            achilles.show_message = function(msg) {
                messages = $('#messages');
                if (messages) {
                    var li = '<li class="' + msg.tags + '">' + msg.message + '</li>';
                    messages.append(li);
                }
            };
        },

        process: function(achilles, messages) {
            for (msg in messages) {
                msg = messages[msg]
                achilles.show_message(msg);
            }
        },
    };

    // Register the controller
    Achilles.fn.registerController('messages', messages_controller);


    // Expose achilles
    window.Achilles = Achilles;
})(window);

