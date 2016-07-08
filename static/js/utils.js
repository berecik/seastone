/**
 * Created by beret on 03.07.16.
 */



function get_templates(selector){
    if(!selector){
        selector = $(document);
    }
    selector.find('__tmp').each(function(){
        get_templates($(this));
        var id = $(this).attr('id');
        if(!(id in templates)){
            templates[id] = $(this).clone().attr('id', '').removeClass('__tmp').addClass('__dynamic');
        }
    });
    selector.find('.__tmp').remove();
}

function get_template(id, values){
    var template = templates[id].clone();
    return render_template(template, values);
}

function render_template(template, values){
    var html = null;
    var clicks = null;
    var events = null;
    var text = values;
    if(values){
        if("text" in values){
            var text = values.text;
            if("html" in values){
                html = values.html;
            }
            if("clicks" in values){
                clicks = values.clicks;
            }
            if("events" in values){
                events = values.events;
            }
        }
        $.each(text, function(key, value){
            $(template).find('.'+key).text(value)
        });
        if(html){
            $.each(html, function(key, value){
                if($.isArray(value)){
                    if($.isArray(value[1])){
                        var html_value  = '';
                        for(var _index in value[1]){
                            html_value += get_template(value[0], value[1][_index]);
                        }
                    }else if($.isFunction(value[1])){
                        var _value = null;
                        var html_value  = '';
                        do{
                            _value = value[1](_value);
                            if(_value){
                                html_value += get_template(value[0], _value);
                            }
                        }while(_value);
                    }else{
                        var html_value = get_template(value[0], value[1]);
                    }
                }else{
                    if(value in templates){
                        var html_value = get_template(value);
                    }else{
                        var html_value = value;
                    }
                }
                $(template).find('.'+key).html(html_value);
            });
        }
        if(clicks){
            $.each(clicks, function(key, value){
                $(template).find('.'+key).click(value)
            });
        }
        if(events){
            $.each(events, function(key, value){
                var item = $(template).find('.'+key);
                $.each(value, function(event, event_fun){
                    $(item).bind(event, event_fun);
                });
            });
        }
    }
    return template;
}

function sleep(milliseconds) {
    var start = new Date().getTime();
    for (var i = 0; i < 1e7; i++) {
        if ((new Date().getTime() - start) > milliseconds){
            break;
        }
    }
}

function append(obj, key, value){
    if(key in obj){

    }else{
        obj[key] = [];
    }
    obj[key].push(value);
}

jQuery.fn.reverse = function(fn) {
    var i = this.length;

    while(i--) {
        fn.call(this[i], i, this[i])
    }
};

Number.prototype.format = function(n, x, s, c) {
    var re = '\\d(?=(\\d{' + (x || 3) + '})+' + (n > 0 ? '\\D' : '$') + ')',
        num = this.toFixed(Math.max(0, ~~n));

    return (c ? num.replace('.', c) : num).replace(new RegExp(re, 'g'), '$&' + (s || ','));
};

String.prototype.hashCode = function(){
    if (Array.prototype.reduce){
        return this.split("").reduce(function(a,b){a=((a<<5)-a)+b.charCodeAt(0);return a&a},0);
    }
    var hash = 0;
    if (this.length === 0) return hash;
    for (var i = 0; i < this.length; i++) {
        var character  = this.charCodeAt(i);
        hash  = ((hash<<5)-hash)+character;
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash;
};


String.prototype.repeat = function( num )
{
    return new Array( num + 1 ).join( this );
};


String.prototype.capitalizeFirstLetter = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
};


function get_url(page, action){
    if(!page){
        page = '';
    }
    if(action){
        action = action + '&'
    }else{
        action = '';
    }
    var url =  page + "?" + action + serialize();
    return url
}


function goto(page, action) {
    var url = get_url(page, action);
    $(location).attr('href', url);
}

function datepicker_value(input, value){
    var date = input.datepicker('getDate');
    return date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate();
}

SERIALISE_TRANSLATION = {
    date: datepicker_value
};


function serialize(selector){
    if(!selector){
        selector = '.serial_form';
    }
    var form_data = $(selector).serialize();
    var inputs = $(".serial");
    for(i=0, len=inputs.length; i<len; i++)
    {
        var input = $(inputs[i]);
        var value = null;
        $.each(SERIALISE_TRANSLATION, function(key, trans_fun){
            if(input.hasClass(key)){
                value = trans_fun(input, value);
            }
        });
        if(!value){
            value = input.val();
        }
        form_data+="&"+input.attr('name')+"="+encodeURIComponent(value);
    }
    global_form_data = form_data;
    return form_data;
}
