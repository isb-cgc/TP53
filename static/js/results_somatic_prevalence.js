/* result_gene_mutation.js */
'use strict';

$(document).ready(function () {
    const selectedRowSet = new Set();
    var table = $('#sm-result-table').DataTable({
        dom: "<'row'<'col-sm-12 col-md-6'l>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        pageLength: 10,
        serverSide: true,
        ajax: {
            url: "/mutation_query",
            type: "POST",
            data: {
                criteria: JSON.stringify($('#criteria_div').data('criteria')),
                query_dataset: 'PrevalenceView' //somatic
            },
            dataType: "json",
            dataSrc: "data"
        },
        preDrawCallback: function(){
            $('.spinner').show();
        },
        drawCallback: function () {
            $('.spinner').hide();
        },
        order: [[ 1, "asc" ]],
        scrollX: true,

        columns: [
            {
                data: "Prevalence_ID",
                orderable: false,
                render: function (data) {
                    return '<input class="form-check-input row-check" type="checkbox" aria-label="Select Row" value="' + data + '"/>';
                },
            },
            {data: "Topography"},
            {data: "Morphology"},
            {data: "Sample_analyzed"},
            {data: "Sample_mutated"},
            {
                data: 'Prevalence',
                render: function (data) {
                    if (data){
                        return data.toFixed(2);
                    }
                    else{
                        return '';
                    }

                }
            },
            {data: "Country"},
            {data: "Population"},
            {data: "Region"},
            {data: "Development"},
            // {data: "Comment"},
            // {data: "Ref_ID"},
            // {data: "Cross_Ref_ID"},
            // {data: "Title"},
            // {data: "Authors"},
            // {data: "Journal"},
            // {data: "Volume"},
            // {data: "Start_page"},
            // {data: "End_page"},
            {
                data: 'PubMed',
                render: function (data) {
                    if (data && data !== 'NA')
                        return '<a href="https://www.ncbi.nlm.nih.gov/pubmed/' + data + '" target="_blank">' + data + '</a>';
                    else
                        return ''
                }
            },
            // {data: "Ref_comment"},
            {data: "Tissue_processing"},
            {data: "Start_material"},
            {data: "Prescreening"},
            {data: "Material_sequenced"},
            // {data: "Short_topo"},
            // {data: "Morphogroup"},
            {data: "Exclude_analysis"},
            {data: "WGS_WXS"},
            //
            // {
            //     data: "COSMIClink",
            //     render: function (data, type) {
            //         if (type == 'export'){
            //             return data;
            //         }
            //         else {
            //             if (data != null)
            //                 return '<a href="https://cancer.sanger.ac.uk/cosmic/mutation/overview?id=' + data + '" target="_blank" title="Go to COSMIC ' + data + '"><i class="far fa-arrow-alt-circle-right"></i></a>';
            //             else
            //                 return data;
            //         }
            //     }
            // },
            // {
            //     data: "CLINVARlink",
            //     render: function (data, type) {
            //         if (type == 'export'){
            //             return data;
            //         }
            //         else {
            //             if (data != null)
            //                 return '<a href="https://www.ncbi.nlm.nih.gov/clinvar/variation/' + data + '" target="_blank" title="Go to ClinVar ' + data + '"><i class="far fa-arrow-alt-circle-right"></i></a>';
            //             else
            //                 return data;
            //         }
            //     }
            // },
            // {data: "TCGA_ICGC_GENIE_count"},
            // {data: "cBioportalCount"},
            // {data: "WT_codon"},
            // {data: "Mutant_codon"},
            // {data: "TransactivationClass"},
            // {data: "DNEclass"},
            // {data: "Hotspot"},
            // {data: "Topography"},
            // {data: "Morphology"},
            // {data: "Sex"},
            // {data: "Age"},
            // {data: "Germline_mutation"},
        ],
        select: {
            style: 'multi',
            selector: '.row-check'
        },
        rowCallback: function(row, data ) {
            if (selectedRowSet.has(data.Prevalence_ID)) {
                selectRow(row);
                $(row).find('.row-check').prop('checked', true);
            }
        },

    });

    $('input.check-all').on('change', function (e) {
        var is_checked = $(this).is(':checked');
        selectAllRows(table, is_checked);
    });

    table
        .on( 'select', function ( e, dt, type, indexes ) {
            var rows_data = table.rows(indexes).data().toArray();
            for(var i=0; i< rows_data.length; i++) {
                if (!selectedRowSet.has(rows_data[i].Prevalence_ID)){
                    selectedRowSet.add(rows_data[i].Prevalence_ID);
                }
            }
            updateActionButtonGroups(selectedRowSet.size);

        })
        .on( 'deselect', function ( e, dt, type, indexes ) {
            var rows_data = table.rows(indexes).data().toArray();
            for(var i=0; i< rows_data.length; i++) {
                selectedRowSet.delete(rows_data[i].Prevalence_ID);
            }
            updateActionButtonGroups(selectedRowSet.size);
        } );

    var selectRow = function(r){
        table.row(r).select();
    };

    $('button.action-button').on('click', function(){
        var action = $(this).val();
        displayDistributions(action, selectedRowSet);
    });

    $('.download-btn').on('click', function () {
        var criteria_map = {};
        if (selectedRowSet.size) {
            var rowIds = Array.from(selectedRowSet);
            var include_criteria = [{'column_name': 'Prevalence_ID', 'vals': rowIds}];
            if (include_criteria){
                criteria_map = {
                    include: include_criteria,
                    exclude: []
                }
            }

        }
        else{
            criteria_map = {
                    include: $('#criteria_div').data('criteria'),
                    exclude: []
            }
        }
        download_csv('tp53db_somatic_prevalence', 'PrevalenceView', criteria_map);

    });

});


var selectAllRows = function (t, bool) {
    if (bool) {
        t.rows().select();
    }
    else {
        t.rows().deselect();
    }
    $('.row-check').prop('checked', bool);

};

var updateActionButtonGroups = function (selectedRowCounts) {
    $('.cart-count').html(selectedRowCounts);
};


var displayDistributions = function (action, selectedRowSet) {
    var form = $("<form method='POST' action='get_prevalence_distribution'></form>");
    var input;
    var criteria;
    if (selectedRowSet.size){
        var rowIds = Array.from(selectedRowSet);
        criteria = [{'column_name': 'Prevalence_ID', 'vals': rowIds}];

    }
    else{
        criteria = $('#criteria_div').data('criteria');
    }

    $("<input>", { value: JSON.stringify(criteria), name: 'criteria', type: 'hidden' }).appendTo(form);
    input = $("<input type='hidden' name='action' value='" + action + "'/>");
    input.appendTo(form);

    form.appendTo($("body"));
    form.submit();
    form.remove();
};
