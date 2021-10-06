/* result_gene_mutation.js */
'use strict';

$(document).ready(function () {
    const selectedRowSet = new Set();
    var selectedRowCellLineCount = 0;
    var table = $('#gm-result-table').DataTable({
        dom: "<'row'<'col-sm-12 col-md-6'l>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
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
            $('input.check-all').prop( "checked", false ); //reset 'Select All' checkbox
            $('.submit-link').on('click', function () {
                $('.spinner').show();
            });
        },
        order: [[ show_hg19? 2:3, "asc" ]],
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
                className: "text-center",
                render: function(data){
                    return '<a title="View Variant Details" class="rounded-circle btn sm-round-btn turquoise-btn submit-link" href="/mut_details?mut_id='+data+'"><i class="fas fa-arrow-right"></i></a>';
                }
            },
            {
                data: "g_description",
                visible: show_hg19
            },
            {
                data: "g_description_GRCh38",
                visible: !show_hg19
            },
            {data: "c_description"},
            {
                data: "ProtDescription",
                render: function (data, type, row) {
                    if (type == 'export'){
                        return data;
                    }
                    else{
                        if (data !== '' && row['Effect'] === 'missense')
                            return '<a data-bs-toggle="tooltip" data-bs-placement="right" title="Link to PHenotypic ANnotation of TP53 Mutations" ' +
                                'href="http://mutantp53.broadinstitute.org/?query=' + data + '" target="_blank" rel="noopener noreferrer">' + data + '</a>';
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
                className: "text-end pe-2",
                render: function (data) {
                    if(data == null || data === '')
                        return '';
                    else
                        return '<a href="https://www.ncbi.nlm.nih.gov/clinvar/variation/' + data + '" target="_blank" rel="noopener noreferrer" title="Go to ClinVar ' + data + '">' + data + '</a>';
                }
            },
            {
                data: "COSMIClink",
                className: "text-end pe-2",
                render: function (data) {
                    if(data == null || data === '')
                        return '';
                    else
                        return '<a href="https://cancer.sanger.ac.uk/cosmic/mutation/overview?id=' + data + '" target="_blank" rel="noopener noreferrer" title="Go to COSMIC ' + data + '">' + data + '</i></a>';
                }
            },
            {
                data: "SNPlink",
                className: "text-end pe-2",
                render: function (data) {
                    if(data == null || data === '')
                        return '';
                    else
                        return '<a href=\"https://www.ncbi.nlm.nih.gov/snp/rs' + data + '" target="_blank" rel="noopener noreferrer" title="Go to dbSNP ' + data + '">' + data + '</a>';
                }
            },
            {
                data: "gnomADlink",
                className: "text-nowrap text-end pe-2",
                render: function (data) {
                    if(data == null || data === '')
                        return '';
                    else
                        return '<a href="https://gnomad.broadinstitute.org/variant/' + data + '" target="_blank" rel="noopener noreferrer" title="Go to gnomAd ' + data + '">' + data + '</a>';
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
        $('.spinner').show();
        var action = $(this).val();
        displayGeneVariationDistributions(action, selectedRowSet);
    });

    $('button.cell-search-button').on('click', function(){
        $('.spinner').show();
        displayCellLines(selectedRowSet);
    });

    $('.download-btn').on('click', function () {
        var criteria_map = {};
        var include_criteria = $('#criteria_div').data('criteria');
        if (selectedRowSet.size) {
            var mutIds = Array.from(selectedRowSet);
            include_criteria = [{'column_name': 'MUT_ID', 'vals': mutIds}];

        }
        if(include_criteria){
            criteria_map = {
                include: include_criteria,
                exclude: []
            }
        }


        download_csv('tp53db_gene_mutations', 'MutationView', criteria_map);
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
    $('button.cell-search-button').toggleClass('disabled', selectedRowCellLineCounts == 0);
};


var displayGeneVariationDistributions = function (action, selectedRowSet) {
    var form = $("<form method='POST' action='/get_distribution'></form>");
    var input;
    if (selectedRowSet.size){
        var mutIds = Array.from(selectedRowSet);
        for (var i = 0; i < mutIds.length; i++) {
            input = $("<input type='hidden' name='mut_id_list' value='" + mutIds[i] + "'/>");
            input.appendTo(form);
        }
    }
    else{
        $("<input>", { value: JSON.stringify($('#criteria_div').data('criteria')), name: 'criteria', type: 'hidden' }).appendTo(form);
    }

    input = $("<input type='hidden' name='action' value='" + action + "'/>");
    input.appendTo(form);
    input = $("<input type='hidden' name='query_dataset' value='Mutation'/>");
    input.appendTo(form);
    form.appendTo($("body"));
    form.submit();
    form.remove();
};

var displayCellLines = function (selectedRowSet) {
    var mutIds = Array.from(selectedRowSet);
    var form = $("<form method='POST' action='/results_cell_line_mutation'></form>");
    for (var i = 0; i < mutIds.length; i++) {
        var input = $("<input type='hidden' name='mut_id_list' value='" + mutIds[i] + "'/>");
        input.appendTo(form);
    }
    form.appendTo($("body"));
    form.submit();
    form.remove();
};

