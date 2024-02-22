odoo.define('employee_dashboard.kitchen_request', function (require) {
    "use strict";
    console.log("inside")
    var publicWidget = require('web.public.widget');
    var Dialog = require('web.Dialog');

    publicWidget.registry.KitchenRequest = publicWidget.Widget.extend({
        selector: '.kitchen',
        events: {
            'click button#fetch':"_fetchData",
        },
        _fetchData: function (ev) {
            console.log("Fetch")
//            var days_of_week=document.getElementById('days_of_week')
//            console.log(days_of_week)
//            var maxI = 5; // Change this to the maximum value of 'i' you expect
//
//        // Array to store the values
//        var mealTimeValues = [];
//        var mealNameValues = [];
//        var checkboxValues = [];
//
//        // Loop through all possible values of 'i'
//        for (var i = 1; i <= maxI; i++) {
//        }
        },
    });

});