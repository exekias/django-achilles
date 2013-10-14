/*
 * Achilles - Django AJAX framework
 *
 * This file provides the javascript framework to communicate with
 * Django Achilles backend
 *
 */
(function(window) {

    // Main constructor
    var achilles = function(endpoint) {
        return new achilles.fn.init(endpoint);
    };

    achilles.fn = achilles.prototype = {

        // Init achilles instance, set the server endpoint URL
        init: function(endpoint) {
            this.endpoint = endpoint;
            return this;
        },


    };

    achilles.fn.init.prototype = achilles.fn;

    // Expose achilles
    window.achilles = achilles;

})(window);

