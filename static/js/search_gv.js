/* search_gv.js */
'use strict';


$(document).ready(function () {
    // console.log($('#gv_type_collapse').length);
    //     if ($('#gv_type_collapse').length) {
    // display_spinner(false);
    $('.type-collapse').removeClass('show');
    $($('input[name="type_input"]:checked').data('bs-target')).addClass('show');
    $('#gv_type_collapse button').remove();
    // }


});
