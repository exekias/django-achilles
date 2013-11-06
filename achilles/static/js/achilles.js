/*
 * Achilles - Django AJAX framework
 *
 * This file provides the javascript framework to communicate with
 * Django Achilles backend
 *
 */
(function(window) {


    /* CORE */

    // Main constructor
    var achilles = function(endpoint) {
        return new achilles.fn.init(endpoint);
    };

    achilles.fn = achilles.prototype = {

        // Init achilles instance, set the server endpoint URL
        init: function(endpoint) {
            this.transport = new JSONTransport(this, endpoint);
            this.controllers = {};

            this.registerController('blocks', blocks_controller);
            this.registerController('actions', actions_controller);

            // Register default controllers
            return this;
        },

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
                    console.log("Unknown controller " + c);
                    continue;
                }

                // Let the controller process its data
                var controller = this.controllers[c];
                controller(this, data[c]);
            }
        },
    };

    achilles.fn.init.prototype = achilles.fn;


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
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }



    /* BLOCKS */

    // Register the response controller
    function blocks_controller(achilles, data) {
        for (b in data) {
            var block = data[b];
            var updater = achilles.block_updaters[block.updater || 'HTML'];
            var blocks = achilles.blocks(block.name, block.args, block.kwargs);
            updater(blocks, block.data);
        }
    };

    // Available block updaters TODO: move to instance var
    achilles.fn.block_updaters = {
        HTML: function (block, data) {
            block.html(data)
        },
    };

    // Look for blocks matching the given criteria
    achilles.fn.blocks = function(name, args, kwargs) {
        return $('[data-ablock="'+name+'"]');
    };



    /* ACTIONS */

    // Register the response controller
    function actions_controller(achilles, actions) {
        for (id in actions) {
            var ret = actions[id];
            achilles._actions[id].resolve(ret);
        }
    };

    // Remote action call
    achilles.fn.action = function(name, args, kwargs) {
        // Create actions metadata on first call
        if (!this._actions) {
            this._actions = {
                count: 0,
                pending: {},
            }
        }

        // Save action deferred to trigger it when the response comes
        var action_id = this._actions.count++;
        var action_deferred = $.Deferred();
        this._actions[action_id] = action_deferred;

        // Launch the action
        this.transport.send({
            name: name,
            id: action_id,
            args: args,
            kwargs: kwargs
        });

        return action_deferred;
    };


    // Expose achilles
    window.achilles = achilles;
})(window);

