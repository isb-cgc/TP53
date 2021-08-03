/* help.js */
'use strict';


$(document).ready(function () {
    $("a.jump-link").on('click', function (e) {
        // e.preventDefault();
        var section_id = $(this).attr('href');
        // $(this).parent('nav.sidebar').removeClass('active');
        // $(this).parents('.nav-item').find('a.nav-link').addClass('active');
        $(this).addClass('active');
        // var collapsibles_to_hide = $(this).parents('.collapse');
        var collapsibles_to_show = $(section_id).parents('.collapse');
        // toggle_collapse_jQSel(collapsibles_to_hide, true);
        toggle_collapse_jQSel(collapsibles_to_show, false);
        // $('html, body').animate({
        //         scrollTop: ($(section_id).offset().top-100)
        //     },
        //     300,
        //     'linear'
        // )
    });
});

