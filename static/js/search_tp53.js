/* search_tp53.js */
'use strict';


$(document).ready(function () {
    enableTooltip();


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

    $('.topo-morph-select').on('change', function () {
        var topo_morph_assc = $(this).data('topo-morph-assc');
        var topos = $(this).val();
        var morphs = [];
        for (var i=0; i < topos.length; i++){
            var topo = topos[i];
            morphs = morphs.concat(topo_morph_assc[topo]);
            console.log(morphs);
        }
        var morph_input_selector = $(this).data('morph-toggle');

        $(morph_input_selector).val(morphs);
        $(morph_input_selector).trigger("chosen:updated");

    });





});

// $(window).on("unload", function() {
//     console.log('unload called');
//     display_spinner(true);
// });

var enableTooltip = function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
};

//type can be cdna, p, hg19 or hg38
var displayGeneVariations = function (type, descrption) {
    var form = $("<form method='POST' action='gv_result' target='_blank'></form>");

    var input = $("<input type='hidden' name='type_input' value='type_"+type+"'/>");
    input.appendTo(form);
    input = $("<input type='hidden' name='gv_"+type+"_list' value='"+descrption+"'/>");
    input.appendTo(form);
    form.appendTo($("body"));
    form.submit();
    form.remove();
};

