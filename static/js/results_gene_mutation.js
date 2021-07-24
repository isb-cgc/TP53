/* result_gene_mutation.js */
'use strict';

$(document).ready(function () {
    const selectedRowSet = new Set();
    var selectedRowCellLineCount = 0;
    var table = $('#gm-result-table').DataTable({
        dom: "<'row'<'col-sm-12 col-md-6'l>>" +
                "<'row d-none'<'col-sm-12 col-md-4'B>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        buttons: [{
                extend: 'csv',
                filename: function () {
                    var db_version;// default version;
                    $.ajax({
                        method: "GET",
                        async: false,
                        url: "/get_db_version",
                        success: function (data) {
                            db_version = data;
                        }
                    });
                    return 'tp53db_gene_mutations' + (db_version ? '_' + db_version : '');
                },
                exportOptions: {
                    columns: ':not(:first-child):not(:last-child)',
                    orthogonal: 'export'
                }}],
        pageLength: 10,
        serverSide: true,
        rowId: 'MUT_ID',
        ajax: {
            url: "/gv_query",
            type: "POST",
            data: {
                criteria: JSON.stringify($('#criteria_div').data('criteria'))
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
        columns: [
            {
                data: "MUT_ID",
                orderable: false,
                render: function (data) {
                    return '<input class="form-check-input row-check" type="checkbox" aria-label="Select Row" value="' + data + '"/>';
                },
            },
            {data: "g_description_GRCh38"},
            {data: "c_description"},
            {
                data: "ProtDescription",
                render: function (data, type, row) {
                    if (type == 'export'){
                        return data;
                    }
                    else{
                        if (data !== '' && row['Effect'] === 'missense')
                            return '<a data-bs-toggle=\"tooltip\" data-bs-placement=\"right\" title=\"Link to PHenotypic ANnotation of TP53 Mutations\" ' +
                                'href=\"http://mutantp53.broadinstitute.org/query=\'' + data + '\'\" target=\"_blank\">' + data + '</a>';
                        else
                            return data;
                    }
                }
            },
            {data: "ExonIntron"},
            {data: "Effect"},
            {data: "TransactivationClass"},
            {data: "DNE_LOFclass"},
            {data: "AGVGDClass"},
            {data: "Somatic_count"},
            {data: "Germline_count"},
            {data: "Cellline_count"},
            {data: "TCGA_ICGC_GENIE_count"},
            {data: "Polymorphism"},
            {
                data: "CLINVARlink",
                render: function (data, type) {
                    if (type == 'export'){
                        return data;
                    }
                    else {
                        if (data != null)
                            return '<a type="button" class="btn btn-tiny btn-sm btn-outline-secondary" href="https://www.ncbi.nlm.nih.gov/clinvar/variation/' + data + '" target="_blank" title="Go to ClinVar ' + data + '">ClinVar</a>';
                        else
                            return data;
                    }
                }
            },
            {
                data: "COSMIClink",
                render: function (data, type) {
                    if (type == 'export'){
                        return data;
                    }
                    else {
                        if (data != null)
                            return '<a type="button" class="btn btn-tiny btn-sm btn-outline-secondary" href="https://cancer.sanger.ac.uk/cosmic/mutation/overview?id=' + data + '" target="_blank" title="Go to COSMIC ' + data + '">COSMIC</a>';
                        else
                            return data;
                    }
                }
            },
            {
                data: "SNPlink",
                render: function (data, type) {
                    if (type == 'export'){
                        return data;
                    }
                    else {
                        if (data !== '')
                            return '<a type="button" class="btn btn-tiny btn-sm btn-outline-secondary" href=\"https://www.ncbi.nlm.nih.gov/snp/rs' + data + '" target="_blank" title="Go to dbSNP ' + data + '">dbSNP</a>';
                        else
                            return data;
                    }
                }
            },
            {
                data: "gnomADlink",
                render: function (data, type) {
                    if (type == 'export'){
                        return data;
                    }
                    else {
                        if (data !== '')
                            return '<a type="button" class="btn btn-tiny btn-sm btn-outline-secondary" href="https://gnomad.broadinstitute.org/variant/' + data + '" target="_blank" title="Go to gnomAd ' + data + '">gnomAD</a>';
                        else
                            return data;
                    }
                }
            },
            {
                data: "MUT_ID",
                orderable: false,
                render: function(data){
                    return '<a type="button" title="View Mutation Details" class="rounded-circle btn btn-sm btn-tiny-round btn-outline-primary" href="mut_details?mut_id='+data+'"><i class="fas fa-arrow-right"></i></a>';
                }
            }
        ],
        select: {
            style: 'multi',
            selector: '.row-check'
        },
        rowCallback: function( row, data ) {
            if (selectedRowSet.has(data.MUT_ID)) {
                selectRow(row);
                $(row).find('.row-check').prop('checked', true);
            }
        },
        // scrollX: true

    });

    $('input.check-all').on('change', function (e) {
        var is_checked = $(this).is(':checked');
        selectAllRows(table, is_checked);
    });

    table
        .on( 'select', function ( e, dt, type, indexes ) {
            var rows_data = table.rows(indexes).data().toArray();
            for(var i=0; i< rows_data.length; i++) {
                if (!selectedRowSet.has(rows_data[i].MUT_ID)){
                    selectedRowSet.add(rows_data[i].MUT_ID);
                    selectedRowCellLineCount += rows_data[i].Cellline_count;
                }
            }
            updateActionButtonGroups(selectedRowSet.size, selectedRowCellLineCount);

        })
        .on( 'deselect', function ( e, dt, type, indexes ) {
            var rows_data = table.rows(indexes).data().toArray();
            for(var i=0; i< rows_data.length; i++) {
                selectedRowSet.delete(rows_data[i].MUT_ID);
                selectedRowCellLineCount -= rows_data[i].Cellline_count;
            }
            updateActionButtonGroups(selectedRowSet.size, selectedRowCellLineCount);
        } );

    var selectRow = function(r){
        table.row(r).select();
    };

    $('button.action-button').on('click', function(){
        var action = $(this).val();
        displayGeneVariationDistributions(action, selectedRowSet);
    });

    $('button.cell-search-button').on('click', function(){
        displayCellLines(selectedRowSet);
    });

    $('.download-btn').on('click', function () {
        $('button.buttons-csv').trigger("click");
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

var updateActionButtonGroups = function (selectedRowCounts, selectedRowCellLineCounts) {
    $('.cart-count').html(selectedRowCounts);
    $('.cell-line-count-badge').html(selectedRowCellLineCounts);
    // $('.action-button').toggleClass('disabled', selectedRowCounts == 0);
    $('button.cell-search-button').toggleClass('disabled', selectedRowCellLineCounts == 0);
};


var displayGeneVariationDistributions = function (action, selectedRowSet) {
    var form = $("<form method='POST' action='results_gene_dist'></form>");
    if (selectedRowSet.size){
        var mutIds = Array.from(selectedRowSet);
        for (var i = 0; i < mutIds.length; i++) {
            var input = $("<input type='hidden' name='mut_id_list' value='" + mutIds[i] + "'/>");
            input.appendTo(form);
        }
    }
    else{
        var input = $("<input type='hidden' name='criteria' value='" + JSON.stringify($('#criteria_div').data('criteria')) + "'/>");
        input.appendTo(form);
        // console.log($('#criteria_div').data('criteria'));
    }

    input = $("<input type='hidden' name='action' value='" + action + "'/>");
    input.appendTo(form);
    form.appendTo($("body"));
    form.submit();
    form.remove();
};

var displayCellLines = function (selectedRowSet) {
    var mutIds = Array.from(selectedRowSet);
    var form = $("<form method='POST' action='results_cell_line_mutation'></form>");
    for (var i = 0; i < mutIds.length; i++) {
        var input = $("<input type='hidden' name='mut_id_list' value='" + mutIds[i] + "'/>");
        input.appendTo(form);
    }
    form.appendTo($("body"));
    form.submit();
    form.remove();
};

