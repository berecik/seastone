/**
 * Created by beret on 22.05.15.
 */

var _filesadded=[];
var _globals={};

function get_globals(filename){
    $.getScript(filename, function(){_globals.update(_locals);});
}

function loadjs(filename){
    var fileref=document.createElement('script');
    fileref.setAttribute("type","text/javascript");
    fileref.setAttribute("src", filename);
    if(typeof fileref!="undefined")
        document.getElementsByTagName("head")[0].appendChild(fileref);
    else
        console.log("I can't load script:"+filename);
    return
}

function loadcss(filename){
    var fileref=document.createElement("link");
    fileref.setAttribute("rel", "stylesheet");
    fileref.setAttribute("type", "text/css");
    fileref.setAttribute("href", filename);
    if(typeof fileref!="undefined")
        document.getElementsByTagName("head")[0].appendChild(fileref);
    else
        console.log("I can't load stylesheet:"+filename)
}

function checkload(load_function){
    return function(filename) {
        if (filename in _filesadded){
            console.log("file " + filename + " already added!");
        }
        else{
            load_function(filename);
            _filesadded.push(filename);
        }
    }
}

function includejs(filename){
    checkload(loadjs)(filename);
}

function includecss(filename){
    checkload(loadcss)(filename);
}