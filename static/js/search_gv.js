/* search_gv.js */
'use strict';


$(document).ready(function () {
    $('.type-collapse').removeClass('show');
    $($('input[name="type_input"]:checked').data('bs-target')).addClass('show');
    $('#gv_type_collapse button').remove();

    // $('.chosen-container-multi').find('.chosen-search-input').on('paste', function (e) {
    //     // implement paste in to chosen multi input box
    //     // find the parent selector,
    //     // split out the comma separated input
    //     // and update the chosen input
    //     var select_box = $('#' + $(e.currentTarget).parents('.chosen-container-multi').attr('id').replace('_chosen', ''));
    //     var str_in = e.originalEvent.clipboardData.getData('text');
    //     var split_arr = str_in.split(/[\s,]+/);
    //     if (split_arr.length > 0) {
    //         select_box.val(split_arr);
    //         select_box.trigger('chosen:updated');
    //     }
    //     return false;
    // });

});

