/* search_tp53.js */
'use strict';


$(document).ready(function () {
    if ($('table.result-table').length === 0)
        $('.spinner').hide();
    enableTooltip();

    $(":reset").on('click', function () {
        $(".chosen-select").val('').trigger("chosen:updated");
        toggle_collapse_jQSel($("form.search-form .collapse.show"), true);
    });

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

    $('.paste-support').on('change', function(e){
        $(this).find('.warning_invalid_var').html('');
    });

    $('.paste-support .chosen-container-multi').find('.chosen-search-input').on('paste', function (e) {
        // implement paste into chosen multi input box
        // find the parent selector,
        // split out the separated input
        // and update the chosen input
        var invalid_items = [];
        var select_box = $('#' + $(e.currentTarget).parents('.chosen-container-multi').attr('id').replace('_chosen', ''));
        var current_val = select_box.val();
        var str_in = e.originalEvent.clipboardData.getData('text');
        var option_list = $.map(select_box.find('option'), function(item) {
            return item.value;
        });
        var lowercase_option_list = $.map(select_box.find('option'), function(item) {
            return item.value.toLowerCase();
        });


        var prefix = select_box.data('var-prefix');
        var split_arr = str_in.split(/[,\n]+/).map(function(item){
            var trimmed_item = item.trim();

            if (!trimmed_item.toLowerCase().startsWith(prefix)){
                trimmed_item = prefix+trimmed_item;
            }
            var list_index = lowercase_option_list.indexOf(trimmed_item.toLowerCase());

            if (list_index < 0){
                invalid_items.push(item);
            }
            else{
                return option_list[list_index];
            }
        });

        if (split_arr.length > 0) {
            select_box.val(current_val.concat(split_arr));
            select_box.trigger('chosen:updated');
        }

        var warning_div = select_box.parents('.paste-support').find('.warning_invalid_var');
        if (invalid_items.length > 0) {
            warning_div.html('<i class="fas fa-exclamation-triangle"></i> Found ' + invalid_items.length + ' invalid variant(s):<br><span class="badge rounded-pill bg-dark-purple">' + invalid_items.join('</span> <span class="badge rounded-pill bg-dark-purple">') + '</span>')
        }
        else {
            warning_div.html('');
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
       var fieldset = $(this).parents('fieldset')
       fieldset.find('select.chosen-select')
           .val('')
           .trigger('chosen:updated')
           .trigger('change');
       fieldset.find('.warning_invalid_var').html('');
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
    var form = $("<form method='POST' action='results_gene_mut_by_gv' target='_blank' rel='noopener noreferrer'></form>");
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