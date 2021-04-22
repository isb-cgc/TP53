/* help.js */
'use strict';


$(document).ready(function () {
    $("a.jump-link").on('click', function (e) {
        e.preventDefault();
        var section_id = $(this).attr('href');
        var collapsibles_to_hide = $(this).parents('.collapse');
        var collapsibles_to_show = $(section_id).parents('.collapse');
        toggle_collapse_jQSel(collapsibles_to_hide, true);
        toggle_collapse_jQSel(collapsibles_to_show, false);
        // $.each(collapsibles_to_hide, function(index, value) {
        //     var div_id_to_hide = $(value).prop('id');
        //
        //     var divCollapse = document.getElementById(div_id_to_hide);
        //     new bootstrap.Collapse(divCollapse, {
        //         hide: true
        //     });
        // });
        //
        // $.each(collapsibles_to_show, function(index, value) {
        //     var div_id_to_show = $(value).prop('id');
        //
        //     var divCollapse = document.getElementById(div_id_to_show);
        //     new bootstrap.Collapse(divCollapse, {
        //         show: true
        //     })
        // });




        $('html, body').animate({
                scrollTop: ($(section_id).offset().top-70)
            },
            300,
            'linear'
        )
    });
});
