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
        $('.browser-alert').show();
    }

});

var download_dataset = function (self, e, dt, button, config) {
    // var self = this;
    var oldStart = dt.settings()[0]._iDisplayStart;
    dt.one('preXhr', function (e, s, data) {
        // Just this once, load all data from the server...
        data.start = 0;
        data.length = 2147483647;
        dt.one('preDraw', function (e, settings) {
            $.fn.dataTable.ext.buttons.csvHtml5.available(dt, config) ?
                $.fn.dataTable.ext.buttons.csvHtml5.action.call(self, e, dt, button, config) :
                dt.one('preXhr', function (e, s, data) {
                    // DataTables thinks the first item displayed is index 0, but we're not drawing that.
                    // Set the property to what it was before exporting.
                    settings._iDisplayStart = oldStart;
                    data.start = oldStart;
                });
            // Reload the grid with the original page. Otherwise, API functions like table.cell(this) don't work properly.
            setTimeout(dt.ajax.reload, 0);
            // Prevent rendering of the full data to the DOM
            return false;
        });
    });
    // Requery the server with the new one-time export settings
    dt.ajax.reload();
};

var reset_spinner_dimension = function () {
    var main_height = $('.main-panel').height() ? $('.main-panel').height() : 0;
    var win_height = $(window).height();
    $('.spinner').height(main_height < win_height ? '100vh' : $('.main-panel').css('height'));
    // $('.spinner').height('100vh');
};

var display_spinner = function (show) {
    console.log('display_spinner show'+ show);
    if (show) {
        $('.spinner').show();
    }
    else {
        $('.spinner').hide();
    }
};

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