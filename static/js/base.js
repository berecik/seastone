/**
 * Created by beret on 13.05.16.
 */

$(document).ready(function() {

    $("#date_range").daterangepicker({
        // "showDropdowns": true,
        // "timePicker": true,
        // "timePicker24Hour": true,
        // "timePickerIncrement": 30,
        "autoApply": true,
        // "ranges": {
        //     "Today": [
        //         moment(),
        //         moment()
        //     ],
        //     "Thomorrow": [
        //         "15-05-2016",
        //         "15-05-2016"
        //     ],
        //     "Next 7 Days": [
        //         "14-05-2016",
        //         "21-05-2016"
        //     ],
        // },
        "locale": {
            "format": "DD-MM-YYYY",
            "separator": " - ",
            "applyLabel": "Apply",
            "cancelLabel": "Cancel",
            "fromLabel": "From",
            "toLabel": "To",
            "customRangeLabel": "Custom",
            "daysOfWeek": [
                "Nd",
                "Pn",
                "Wt",
                "Śr",
                "Czw",
                "Pt",
                "So"
            ],
            "monthNames": [
                "Styczeń",
                "Luty",
                "Marzec",
                "Kwiecień",
                "Maj",
                "Czerwiec",
                "Lipiec",
                "Sierpień",
                "Wrzesień",
                "Październik",
                "Listopad",
                "Grudzień"
            ],
            "firstDay": 1
        },
        "startDate": "14-05-2016",
        "endDate": "21-05-2016",
        "opens": "left"
    }, function(start, end, label) {
        console.log("New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')");
    });

    $("#length").buttonset();

    var url = "?base=1";

    $( ".accordion" )
        .accordion({
            header: "> div > div.header",
            collapsible: true,
            heightStyle: "content"
        });
    $( ".piers_sort" )
        .sortable({
            axis: "y",
            handle: "div.header",
            stop: function( event, ui ) {
                // IE doesn't register the blur when sorting
                // so trigger focusout handlers to remove .ui-state-focus
                ui.item.children( "div.header" ).triggerHandler( "focusout" );
                var order = "";
                $('.pier_id').each(function (i, id) {
                    order+=i+","+$(id).val()+"|";
                });
                var _url = url + "&order_pier="+order;
                $.get(_url);
                // Refresh accordion to handle new order
                $( this ).accordion( "refresh" );
            }
        });
    $(".moorings_sort")
        .sortable({
            items: ".mooring_sort",
            stop: function( event, ui ) {
                var order = "";
                $('.mooring_id').each(function (i, id) {
                    order+=i+","+$(id).val()+"|";
                });
                var _url = url + "&order_mooring="+order;
                $.get(_url);
            }
        })
        .disableSelection();
    $( ".date" ).datepicker($.datepicker.regional[ "pl" ]);
    dialog = $( "#add_stay_form" ).dialog({
        autoOpen: false,
        height: 300,
        width: 350,
        modal: true,
        // buttons: {
        //   "Create an account": addUser,
        //   Cancel: function() {
        //     dialog.dialog( "close" );
        //   }
        // },
        close: function() {
            location.reload();
        }
    });
});

function create_stay(place_id) {
    $( "#place_id" ).val(place_id);
    $( "#ship_select" ).autocomplete({
        minLength: 0,
        source: ships,
        focus: function( event, ui ) {
            $( "#ship_select" ).val( ui.item.label );
            return false;
        },
        change: function( event, ui ) {
            $( "#ship_id" ).val("");
        },
        select: function( event, ui ) {
            $( "#ship_select" ).val( ui.item.label );
            $( "#ship_id" ).val( ui.item.value );
            $( "#ship_length" ).val( ui.item.length );
            // $( "#ship_length" ).disable();
            $( "#ship_flag_img" ).attr( "src", "/static/flags/" + ui.item.flag + ".png" );
            $( "#ship_flag option[value="+ui.item.flag+"]" ).attr('selected','selected');
            // $( "#ship_flag" ).disable();

            return false;
        }
    })
        .autocomplete( "instance" )._renderItem = function( ul, item ) {
        return $( "<li>" )
            .append( "<a>" + item.name + " <img src='/static/flags/" + item.flag + ".png'></a>" )
            .appendTo( ul );
    };
    $( "#ship_flag").change(function () {
        $( "#ship_flag_img" ).attr( "src", "/static/flags/" + $(this).val() + ".png" );
    });
    dialog.dialog( "open" );
};