/* search_gv.js */
'use strict';


$(document).ready(function () {
    $('.type-collapse').removeClass('show');
    $($('input[name="type_input"]:checked').data('bs-target')).addClass('show');
    $('#gv_type_collapse button').remove();

});

