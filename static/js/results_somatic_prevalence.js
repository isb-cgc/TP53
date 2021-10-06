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
                query_dataset: 'Prevalence' //somatic
            },
            dataType: "json",
            dataSrc: "data"
        },
        preDrawCallback: function(){
            $('.spinner').show();
        },
        drawCallback: function () {
            $('.spinner').hide();
            $('input.check-all').prop( "checked", false ); //reset 'Select All' checkbox
            enableTooltip();
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
            {data: "Short_topo"},
            {data: "Topo_code"},
            {data: "Morphology"},
            {data: "Morpho_code"},
            {
                data: "Sample_analyzed",
                class: 'text-end pe-3'
            },
            {
                data: "Sample_mutated",
                class: 'text-end pe-3'
            },
            {
                data: 'Prevalence',
                render: function (data) {
                    return data.toFixed(2);
                },
                class: 'text-end pe-3'
            },
            {data: "Country"},
            {data: "Region"},
            {data: "Comment"},
            {
                data: 'PubMed',
                render: function (data) {
                    if (data && data !== 'NA')
                        return '<a href="https://www.ncbi.nlm.nih.gov/pubmed/' + data + '" target="_blank" rel="noopener noreferrer">' + data + '</a>';
                    else
                        return ''
                }
            },
            {data: "Tissue_processing"},
            {data: "Start_material"},
            {data: "Prescreening"},
            {

                data: "exon2",
                render: function (data) {
                    var checkbox_class = data ? "fas fa-check-circle text-success":"fas fa-circle text-light";

                    return '<i data-bs-toggle="tooltip" data-bs-placement="right" title="'+data+'" class="'+checkbox_class+'"></i>';
                },
                class: 'text-center'

            },
            {
                data: "exon3",
                render: function (data) {
                    var checkbox_class = data ? "fas fa-check-circle text-success":"fas fa-circle text-light";
                    return '<i data-bs-toggle="tooltip" data-bs-placement="right" title="'+data+'" class="'+checkbox_class+'"></i>';
                },
                class: 'text-center'
            },
            {
                data: "exon4",
                render: function (data) {
                    var checkbox_class = data ? "fas fa-check-circle text-success":"fas fa-circle text-light";
                    return '<i data-bs-toggle="tooltip" data-bs-placement="right" title="'+data+'" class="'+checkbox_class+'"></i>';
                },
                class: 'text-center'
            },
            {
                data: "exon5",
                render: function (data) {
                    var checkbox_class = data ? "fas fa-check-circle text-success":"fas fa-circle text-light";
                    return '<i data-bs-toggle="tooltip" data-bs-placement="right" title="'+data+'" class="'+checkbox_class+'"></i>';
                },
                class: 'text-center'
            },
            {
                data: "exon6",
                render: function (data) {
                    var checkbox_class = data ? "fas fa-check-circle text-success":"fas fa-circle text-light";
                    return '<i data-bs-toggle="tooltip" data-bs-placement="right" title="'+data+'" class="'+checkbox_class+'"></i>';
                },
                class: 'text-center'
            },
            {
                data: "exon7",
                render: function (data) {
                    var checkbox_class = data ? "fas fa-check-circle text-success":"fas fa-circle text-light";
                    return '<i data-bs-toggle="tooltip" data-bs-placement="right" title="'+data+'" class="'+checkbox_class+'"></i>';
                },
                class: 'text-center'
            },
            {
                data: "exon8",
                render: function (data) {
                    var checkbox_class = data ? "fas fa-check-circle text-success":"fas fa-circle text-light";
                    return '<i data-bs-toggle="tooltip" data-bs-placement="right" title="'+data+'" class="'+checkbox_class+'"></i>';
                },
                class: 'text-center'
            },
            {
                data: "exon9",
                render: function (data) {
                    var checkbox_class = data ? "fas fa-check-circle text-success":"fas fa-circle text-light";
                    return '<i data-bs-toggle="tooltip" data-bs-placement="right" title="'+data+'" class="'+checkbox_class+'"></i>';
                },
                class: 'text-center'
            },
            {
                data: "exon10",
                render: function (data) {
                    var checkbox_class = data ? "fas fa-check-circle text-success":"fas fa-circle text-light";
                    return '<i data-bs-toggle="tooltip" data-bs-placement="right" title="'+data+'" class="'+checkbox_class+'"></i>';
                },
                class: 'text-center'
            },
            {
                data: "exon11",
                render: function (data) {
                    var checkbox_class = data ? "fas fa-check-circle text-success":"fas fa-circle text-light";
                    return '<i data-bs-toggle="tooltip" data-bs-placement="right" title="'+data+'" class="'+checkbox_class+'"></i>';
                },
                class: 'text-center'
            },
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
        $('.spinner').show();
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
