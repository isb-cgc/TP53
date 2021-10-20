/* help.js */
'use strict';


$(document).ready(function () {
    $("a.jump-link").on('click', function (e) {
        var section_id = $(this).attr('href');
        var collapsibles_to_show = $(section_id).parents('.collapse');
        if (collapsibles_to_show.length === 0)
            collapsibles_to_show = $(section_id);
        toggle_collapse_jQSel(collapsibles_to_show, false);
        collapsibles_to_show.on('shown.bs.collapse', function () {
            window.location = section_id;
        });
    });
});

