/**
 * Created by beret on 13.05.16.
 */

$(document).ready(function() {
    $( ".date" ).datepicker($.datepicker.regional[ "pl" ],{
        defaultDate: 0
    });
    $( ".date_now" ).datepicker('setDate', Date.now());
});