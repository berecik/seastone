/**
 * Created by beret on 04.07.16.
 */
hubs = {};
places = {};
piers = {};
yboms = {};
map = null;

function _places(places, action){
    return function(){
        $.each(places, function (id) {
            action(places[id]);
        });
    }
}

function _remove(item) {
    if(map.hasLayer(item.icon)){
        map.removeLayer(item.icon);
    }
}

function _draw(item, color){
    if(!color){
        color = 'red';
    }
    item.icon.setStyle({
        color: color,
        fillColor: color,
        fillOpacity: 1
    });
    item.icon.addTo(map);
}

function _draw_place(item, color){
    if(!color){
        color = 'red';
    }
    item.icon.setStyle({
        color: color,
        fillColor: color
    });
    item.icon.addTo(map);
    item.connector.addTo(map);
}

draw_hubs =     _places(hubs,   function(item){
    _draw(item, 'blue');
});

draw_yboms =     _places(yboms,   function(item){
    _draw(item, 'blue');
});

draw_places =   _places(places, function(item){
    _draw(item, 'green');
});

STATE_COLORS = {
    "resident": "yellow",
    "free": "green",
    "booked": "red"
};

function draw_all() {
    $.get(get_url(null, 'get_places'), function (data) {
        _places(hubs, _remove)();
        _places(places, _remove)();
        if($('[name="show_hubs"]').is(':checked')){
            draw_hubs();
        }
        draw_yboms();
        $.each(data, function (state) {
            if($('[name="show_'+state+'"]').is(':checked')) {
                var color = STATE_COLORS[state];
                var ids = data[state];
                for (i in ids) {
                    var id = ids[i];
                    var item = places[id];
                    _draw(item, color);
                    item.icon.on('click', function(id, item){
                        $.get(get_url(null, 'place_state='+id), create_popup.bind(null, id, item));
                    }.bind(null, id, item));
                }
            }
        })
    });
}

function refresh() {
    draw_all();
}

function create_popup(place_id, item, content) {
    item.icon.bindPopup(content, {maxWidth: null, minWidth: 500, keepInView: true, closeButton: false});
    item.icon.openPopup();
    item.popup = item.icon._popup;
    var _call_txt = $("#_call_"+place_id).text();
    $("#_call_"+place_id).hide();
    eval(_call_txt);
}


function set_popup(place_id, content) {
    var item = places[place_id];
    item.icon._popup.setContent(content);
    var _call_txt = $("#_call_"+place_id).text();
    $("#_call_"+place_id).hide();
    eval(_call_txt);
}

function close_popup(place_id) {
    var item = places[place_id];
    item.icon.closePopup();
    refresh();
}


function set_action(place_id, action, action_id){
    if(!action_id){
        action_id = place_id;
    }
    $.get(
        get_url(null, action+'='+action_id),
        set_popup.bind(null, place_id)
    );
}


function set_stay(place_id) {
    $( "#date_start_"+place_id ).datepicker($.datepicker.regional[ "pl" ],{
        defaultDate: 0
    });
    $( "#date_start_"+place_id ).datepicker('setDate', $('#date_start').datepicker('getDate'));
    $( "#date_start_"+place_id ).prop('disabled', true);

    $( "#date_end_"+place_id ).datepicker($.datepicker.regional[ "pl" ],{
        defaultDate: 0
    });
    $( "#date_end_"+place_id ).datepicker('setDate', $('#date_end').datepicker('getDate'));
    $( "#date_end_"+place_id ).prop('disabled', true);

    $( "#ship_select_"+place_id ).autocomplete({
        minLength: 0,
        source: ships,
        focus: function( event, ui ) {
            $( "#ship_select_"+place_id ).val( ui.item.label );
            return false;
        },
        // change: function( event, ui ) {
        //     $( "#ship_id_"+place_id ).val("");
        // },
        select: function( event, ui ) {
            $( "#ship_select_"+place_id ).val( ui.item.label );
            $( "#ship_id_"+place_id ).val( ui.item.value );
            $( "#ship_length_"+place_id ).val( ui.item.length );
            $( "#ship_flag_img_"+place_id ).attr( "src", "/static/flags/" + ui.item.flag + ".png" );
            $( "#ship_flag_"+place_id+" option[value="+ui.item.flag+"]" ).attr('selected','selected');
            return false;
        }
    })
        .autocomplete( "instance" )._renderItem = function( ul, item ) {
        return $( "<li>" )
            .append( "<a>" + item.name + " <img src='/static/flags/" + item.flag + ".png'></a>" )
            .appendTo( ul );
    };
    $(".ship_fields").change(function (e) {
        $( "#ship_id_"+place_id ).val("");
    });
    $( "#ship_flag_"+place_id).change(function () {
        $( "#ship_flag_img_"+place_id ).attr( "src", "/static/flags/" + $(this).val() + ".png" );
    });

    $( "#type_stay_"+place_id).click(function () {
        $( "#date_end_span_"+place_id ).show();
        $("#submit_"+place_id).text("Dodaj postój");
    });

    $( "#type_resident_"+place_id).click(function () {
        $( "#date_end_span_"+place_id ).hide();
        $("#submit_"+place_id).text("Dodaj rezydenta");
    });

    var submit_stay = function(place_id, e){
        var url = get_url(null, 'place_state='+place_id);
        var data = $("#form_"+place_id).serialize();
        $.ajax({
               type: "POST",
               url: url,
               data: data,
               success: function(content)
               {
                   set_popup(place_id, content);
               }
             });
        if(e){
            e.preventDefault();
        }
    }.bind(null, place_id);
    $("#submit_"+place_id).click(submit_stay);
}

function edit_place(place_id) {
    var submit_place = function(place_id, e){
        var url = get_url(null, 'edit_place='+place_id);
        var data = $("#form_"+place_id).serialize();
        $.ajax({
               type: "POST",
               url: url,
               data: data,
               success: function(content)
               {
                   set_popup(place_id, content);
               }
             });
        if(e){
            e.preventDefault();
        }
    }.bind(null, place_id);
    $("#submit_"+place_id).click(submit_place);
}

