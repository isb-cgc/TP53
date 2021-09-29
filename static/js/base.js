'use strict';
var active_menu;
var active_submenu;
var scrollSpy;
$(document).ready(function () {

    function set_active_menu(menu_id) {
        if (!menu_id) {
            menu_id = 'home_menu';
        }
        $('#' + menu_id).parent().addClass("active");
    }

    function set_active_submenu(submenu_id) {
        if (!submenu_id)
            return;
        toggle_collapse_jQSel($(".collapsible-sidebar #"+submenu_id+".sub-navitem").parents('.collapse'), false);

        $(".sidebar, .collapsible-sidebar").find(".active").removeClass("active");
        $('#' + submenu_id).addClass("active");

    }

    function set_data_bs_target(enableScrollspy) {
        if (enableScrollspy) {
            scrollSpy = new bootstrap.ScrollSpy(document.body, {
                target: '.sidebar',
                offset: 150
            });
        }
        else {
            scrollSpy = null;
        }
    }



    set_active_menu(active_menu);
    set_active_submenu(active_submenu);

    set_data_bs_target(['help', 'resources', 'about'].indexOf(active_menu) >= 0);
    // set_data_bs_target(['help', 'resources', 'refs_corner', 'ppl_events', 'about'].indexOf(active_menu) >= 0);

    $(".back-button").click(function () {
        window.history.back();
    });
    if (navigator.userAgent.search("Chrome") < 0 && navigator.userAgent.search("Firefox") < 0 || navigator.userAgent.search("Edge") > 0) {
        $('#browser-alert').show();
    }

});



// var reset_spinner_dimension = function () {
//     var main_height = $('.main-panel').height() ? $('.main-panel').height() : 0;
//     var win_height = $(window).height();
//     $('.spinner').height(main_height < win_height ? '100vh' : $('.main-panel').css('height'));
//     // $('.spinner').height('100vh');
// };
//
// var display_spinner = function (show) {
//     console.log('display_spinner show'+ show);
//     if (show) {
//         $('.spinner').show();
//     }
//     else {
//         $('.spinner').hide();
//     }
// };

var toggle_collapse_jQSel = function (selections, triggerHide) {
    $.each(selections, function (index, value) {
        var div_ids = $(value).prop('id');
        var divCollapse = document.getElementById(div_ids);
        new bootstrap.Collapse(divCollapse,
            triggerHide ? {hide: true, show: false} : {hide: false, show: true}
        );
    });
};

var copy_to_clipboard = function (el) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($(el).text()).select();
    document.execCommand("copy");
    $temp.remove();
};

var open_sidebar = function(){
    $('div.collapsible-sidebar').addClass('hover');
};

var download_csv = function (filename, table, criteria_map) {
    var input;
    var form = $("<form method='POST' action='download_dataset'></form>");

    if (criteria_map) {
        $("<input>", { value: JSON.stringify(criteria_map), name: 'criteria_map', type: 'hidden' }).appendTo(form);
    }
    input = $("<input type='hidden' name='filename' value='"+filename+"'/>");
    input.appendTo(form);

    input = $("<input type='hidden' name='query_datatable' value='"+table+"'/>");
    input.appendTo(form);

    form.appendTo($("body"));
    form.submit();
    form.remove();
};

