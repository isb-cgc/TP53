/* search.js */
'use strict';
$(document).ready(function () {
    $(":reset").on('click', function(){
        $(".chosen-select").val('').trigger("chosen:updated");
        if (active_menu === 'case_search'){
            update_case_search_form(true);
        }
        else if (active_menu === 'recab_search'){
            update_recab_search_form(true);
        }
    });

    $(":submit").on('click', function () {
        display_spinner(true);
        // if (active_menu === 'case_search') {
        //     //disable collapsed inputs for non-advanced search
        //     $('.full-case-search.collapse').not('.show').find('input, select').prop('disabled', true);
        // }
        // else if(active_menu === 'mb_search'){
        //     $('#genes_mb').val($('#inputGeneMG').val());
        // }
    });

    $('.chosen-select:not(#inputGeneMG)').chosen({
        no_results_text: "Oops, nothing found!",
        width: "100%"
    });

    $('#inputGeneMG.chosen-select').chosen({
        no_results_text: "Oops, nothing found!",
        width: "100%",
        max_shown_results: 300
    });

    setTimeout(function(){ $(".chosen-select").trigger("chosen:updated"); }, 500);

    if (active_menu === 'case_search'){
        setTimeout(function(){ update_case_search_form(!$('.collapse-toggler').is(":checked")); }, 500);
    }
    else if (active_menu === 'recab_search'){
        setTimeout(function(){ update_recab_search_form( !$('#aberCheckboxStr').is(':checked') &&  !$('#aberCheckboxNum').is(':checked')); }, 500);
    }
    else if (active_menu === 'mb_search'){
        display_spinner(true);
        var inputGeneMG = $('#inputGeneMG');
        $.ajax({
            type: "GET",
            url: "/get_mglist",
            dataType: "json",
            success: function (data) {
                $.each(data, function (index, value) {
                    $('#inputGeneMG').append('<option>' + value.label + '</option>');
                });
            },
            complete: function () {
                inputGeneMG.val($('#genes_mb').val().split(','));
                inputGeneMG.trigger("chosen:updated");
                display_spinner(false);
            }
        });
    }
});
$(window).on("unload", function(e) {
    display_spinner(false);
});

function update_case_search_form(collapse){
    $('.full-case-search').collapse(collapse ? 'hide':'show');
    $('.full-case-search.collapse').find('input, select').prop('disabled', false);
}

function update_recab_search_form(collapse) {
    var structure_checked = $('#aberCheckboxStr').is(':checked');
    var numeric_checked = $('#aberCheckboxNum').is(':checked');
    var aber_type_selected = structure_checked || numeric_checked;
    $('.str-aberration').toggle(!collapse && structure_checked);
    $('.num-aberration').toggle(!collapse && numeric_checked);
    $('.tumor-ch').toggle(!collapse && aber_type_selected);
    $('#recab_submit').attr("disabled", collapse || !aber_type_selected);
}
