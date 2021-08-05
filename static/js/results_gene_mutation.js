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
            action:
                function (e, dt, node, config) {
                    if (selectedRowSet.size) {
                        download_selected_dataset(this, selectedRowSet, e, dt, node, config);
                    }
                    else {
                        download_dataset(this, e, dt, node, config);
                    }
                },
            exportOptions: {
                columns: ':not(:first-child):not(:nth-child(2))',
                orthogonal: 'export'
            }
        }],
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
        order: [[ 2, "asc" ]],
        scrollX: true,
        columns: [
            {
                data: "MUT_ID",
                orderable: false,
                render: function (data) {
                    return '<input class="form-check-input row-check" type="checkbox" aria-label="Select Row" value="' + data + '"/>';
                },
            },
            {
                data: "MUT_ID",
                orderable: false,
                render: function(data){
                    return '<a title="View Mutation Details" class="rounded-circle btn btn-tiny turquoise-btn" href="mut_details?mut_id='+data+'"><i class="fas fa-arrow-right"></i></a>';
                    // return '<a type="button" title="View Mutation Details" class="rounded-circle btn btn-tiny-round turquoise-btn" href="mut_details?mut_id='+data+'"><i class="fas fa-arrow-right"></i></a>';
                }
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
                            return '<a href="https://www.ncbi.nlm.nih.gov/clinvar/variation/' + data + '" target="_blank" title="Go to ClinVar ' + data + '"><i class="far fa-arrow-alt-circle-right"></i></a>';
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
                            return '<a href="https://cancer.sanger.ac.uk/cosmic/mutation/overview?id=' + data + '" target="_blank" title="Go to COSMIC ' + data + '"><i class="far fa-arrow-alt-circle-right"></i></a>';
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
                            return '<a href=\"https://www.ncbi.nlm.nih.gov/snp/rs' + data + '" target="_blank" title="Go to dbSNP ' + data + '"><i class="far fa-arrow-alt-circle-right"></i></a>';
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
                            return '<a href="https://gnomad.broadinstitute.org/variant/' + data + '" target="_blank" title="Go to gnomAd ' + data + '"><i class="far fa-arrow-alt-circle-right"></i></a>';
                        else
                            return data;
                    }
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

var download_selected_dataset = function (self, selectedRowSet, e, dt, button, config) {
        var old_ajax_criteria = dt.settings()[0].ajax.data.criteria;
        var oldStart = dt.settings()[0]._iDisplayStart;

        dt.one('preXhr', function (e, s, data) {
            // Just this once, load all data from the server...
            data.start = 0;
            data.length = 2147483647;
            console.log(data.criteria);
            var new_criteria = [{
                "column_name": "MUT_ID",
                "vals": Array.from(selectedRowSet),
            }];
            data.criteria = JSON.stringify(new_criteria);

            dt.one('preDraw', function (e, settings) {
                $.fn.dataTable.ext.buttons.csvHtml5.available(dt, config) ?
                    $.fn.dataTable.ext.buttons.csvHtml5.action.call(self, e, dt, button, config) :
                    dt.one('preXhr', function (e, s, data) {
                        // DataTables thinks the first item displayed is index 0, but we're not drawing that.
                        // Set the property to what it was before exporting.
                        settings._iDisplayStart = oldStart;
                        settings.ajax.data.criteria = old_ajax_criteria;
                        data.start = oldStart;
                        data.criteria = old_ajax_criteria;
                    });

                // Reload the grid with the original page. Otherwise, API functions like table.cell(this) don't work properly.
                setTimeout(dt.ajax.reload, 0);
                // Prevent rendering of the full data to the DOM
                return false;
            });
        });
        // // Requery the server with the new one-time export settings
        dt.ajax.reload();
    };

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

