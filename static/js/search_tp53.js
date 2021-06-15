/* search_tp53.js */
'use strict';


$(document).ready(function () {
    enableTooltip();

    $(":reset").on('click', function () {
        $(".chosen-select").val('').trigger("chosen:updated");
        toggle_collapse_jQSel($("form.search-form .collapse.show"), true);
    });

    // $(":submit").on('click', function () {
    //     console.log('submit clicked');
    //     display_spinner(true);
    // });

    $('.chosen-select').chosen({
        no_results_text: "Oops, nothing found!",
        width: "100%",
        search_contains: true,
        max_shown_results: 300
    });

    $('.topo-morph-select').on('change', function () {
        var topo_morph_assc = $(this).data('topo-morph-assc');
        var topos = $(this).val();
        var morphs = [];
        for (var i=0; i < topos.length; i++){
            var topo = topos[i];
            morphs = morphs.concat(topo_morph_assc[topo]);
        }
        var morph_input_selector = $(this).data('morph-toggle');
        $(morph_input_selector).val(morphs);
        $(morph_input_selector).trigger("chosen:updated");
    });

    $('.paste-support .chosen-container-multi').find('.chosen-search-input').on('paste', function (e) {
        // implement paste into chosen multi input box
        // find the parent selector,
        // split out the separated input
        // and update the chosen input
        var select_box = $('#' + $(e.currentTarget).parents('.chosen-container-multi').attr('id').replace('_chosen', ''));
        var str_in = e.originalEvent.clipboardData.getData('text');
        var split_arr = str_in.split(/[,\n]+/).map(function(item){
            return item.trim();
        });
        if (split_arr.length > 0) {
            select_box.val(split_arr);
            select_box.trigger('chosen:updated');
        }
        return false;
    });

   if($('.form-switch input').prop('checked')){
       var collapsible_class = $('.form-switch input').data('bs-target');
       var shown_id = $(collapsible_class+'.show').attr('id');
       var hidden_id = $(collapsible_class +':not(.show)').attr('id');
       var shown_collapse = document.getElementById(shown_id);
       var hidden_collapse = document.getElementById(hidden_id);
       new bootstrap.Collapse(shown_collapse, {
           show: false,
           hide: true
       });
       new bootstrap.Collapse(hidden_collapse, {
           show: true,
           hide: false
       });
   }

   $('a.clear-all-select').on('click', function (e) {
       e.preventDefault();
       $(this).parents('fieldset').find('select.chosen-select')
           .val('')
           .trigger('chosen:updated')
           .trigger('change');
   });

   $('a.add-all-select').on('click', function (e) {
       e.preventDefault();
       var select_box = $(this).parents('fieldset').find('select.chosen-select');
       select_box
           .find('option')
           .prop('selected', true);
       select_box
           .trigger('chosen:updated')
           .trigger('change');
   });

});

var enableTooltip = function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
};

//type can be cdna, p, hg19 or hg38
var displayGeneVariations = function (type, descrption) {
    var form = $("<form method='POST' action='results_gene_mut_by_gv' target='_blank'></form>");
    var input = $("<input type='hidden' name='type_input' value='type_"+type+"'/>");
    input.appendTo(form);
    input = $("<input type='hidden' name='gv_"+type+"_list' value='"+descrption+"'/>");
    input.appendTo(form);
    form.appendTo($("body"));
    form.submit();
    form.remove();
};

var trigger_file_download = function(filename, data){
    var d_link = document.createElement('a');
    d_link.setAttribute('href', data);
    d_link.setAttribute('download', filename);
    document.body.appendChild(d_link); // Required for FF
    d_link.click();
    document.body.removeChild(d_link);
};