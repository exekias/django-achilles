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
            this.transport = new JSONTransport(endpoint);
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


    /* JSON TRANSPORT */
    /* Default messages transport, using JQuery.ajax */
    function JSONTransport(endpoint) {
        this.endpoint = endpoint;
    }

    JSONTransport.fn = JSONTransport.prototype = {
        // Send the given message to the server
        send: function(msg) {
            return $.ajax({
                url: this.endpoint,
                crossDomain: false,
                type: 'POST',
                beforeSend: this.setCSRFHeader,
                data: msg,
            });
        },

        setCSRFHeader: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) {
                var csrftoken = getCookie('csrftoken');
                alert(csrftoken);
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

