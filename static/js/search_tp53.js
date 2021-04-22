/* search_tp53.js */
'use strict';


$(document).ready(function () {

    console.log('hello');
    //enable bootstrap's tooltip
    enableTooltip();
    // var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    // var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    //     return new bootstrap.Tooltip(tooltipTriggerEl)
    // });


    $(":reset").on('click', function () {
        $(".chosen-select").val('').trigger("chosen:updated");
        toggle_collapse_jQSel($("form.search-form .collapse.show"), true);
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


    $('.chosen-select').chosen({
        no_results_text: "Oops, nothing found!",
        width: "100%",
        max_shown_results: 300
    });
});

var enableTooltip = function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
};

var displayGeneVariations = function (cDescription) {
    var form = $("<form method='POST' action='gv_result' target='_blank'></form>");
    var input = $("<input type='hidden' name='type_input' value='type_cdna'/>");
    input.appendTo(form);
    input = $("<input type='hidden' name='cdna_list' value='"+cDescription+"'/>");
    input.appendTo(form);
    form.appendTo($("body"));
    form.submit();
    form.remove();
};
