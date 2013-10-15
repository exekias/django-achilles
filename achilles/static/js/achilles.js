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

        // Map of response handlers
        controllers : {},

        // Init achilles instance, set the server endpoint URL
        init: function(endpoint) {
            this.endpoint = endpoint;
            return this;
        },

        // Register a response controller
        //     key - key from the response data to pass to this controller
        //     controller - the controller itself
        registerController: function(key, controller) {
            this.controllers[key] = controller;
        },

    };

    achilles.fn.init.prototype = achilles.fn;



    /* BLOCKS */

    BlockController = {

        updaters: {
            HTML: function (block, data) {
                block.html(data)
            },
        },

        get: function(name, args, kwargs) {
            return $('[data-ablock="'+name+'"]');
        },

        // Controller process function
        process: function(data) {
            for (b in data) {
                updater = updaters(b.updater || 'HTML');
                block = achilles.blocks.get(b.name, b.args, b.kwargs);
                updater(block, b.data);
            }
        },

    };

    // Expose blocks as part of achilles api
    achilles.fn.blocks = BlockController;

    // Register the response controller
    achilles.fn.registerController('blocks', BlockController);


    // Expose achilles
    window.achilles = achilles;
})(window);

