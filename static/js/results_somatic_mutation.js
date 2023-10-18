/* result_somatic_mutation.js */
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
                query_dataset: 'Somatic' //somatic
            },
            error: function (result) {
                let msg = 'There has been an error while running the search. Please try again.';
                if (result.responseJSON && result.responseJSON.error_message) {
                    msg = result.responseJSON.error_message;
                }
                $('.spinner').hide();
                $('.dataTables_info').parents('.row').append(
                    '<div class="col-sm-12 text-center fw-bold"><i class="fas fa-exclamation-triangle me-2"></i>'+msg+'</div>');
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
        },
        order: [[ show_hg19 ? 1:2, "asc" ]],
        scrollX: true,

        columns: [
            {
                data: "MUT_ID",
                orderable: false,
                render: function (data, type, row) {
                    return '<input class="form-check-input row-check" type="checkbox" aria-label="Select Row" value="' + data+":"+ row.SomaticView_ID + '"/>';
                },
            },
            {
                data: "g_description",
                visible: show_hg19
            },
            {
                data: "g_description_GRCh38",
            },
            {data: "c_description"},
            {
                data: "ProtDescription",
                render: function (data, type, row) {
                    if (type === 'export'){
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
            {data: "hg19_Chr17_coordinates"},
            {data: "hg38_Chr17_coordinates"},
            {data: "Codon_number"},
            {
                data: "COSMIClink",
                className: "text-end pe-2",
                render: function (data, type) {
                    if (data != null)
                        return '<a href="https://cancer.sanger.ac.uk/cosmic/mutation/overview?id=' + data + '" target="_blank" rel="noopener noreferrer" title="Go to COSMIC ' + data + '">' + data + '</a>';
                    return data;
                }
            },
            {
                data: "CLINVARlink",
                className: "text-end pe-2",
                render: function (data, type) {
                    if (data != null)
                        return '<a href="https://www.ncbi.nlm.nih.gov/clinvar/variation/' + data + '" target="_blank" rel="noopener noreferrer" title="Go to ClinVar ' + data + '">' + data + '</a>';
                    else
                        return data;
                }
            },
            {data: "TCGA_ICGC_GENIE_count"},
            {data: "cBioportalCount"},
            {data: "WT_codon"},
            {data: "Mutant_codon"},
            {data: "TransactivationClass"},
            {data: "DNEclass"},
            {data: "Hotspot"},
            {data: "Topography"},
            {data: "Morphology"},
            {data: "Sex"},
            {data: "Age"},
            {data: "Germline_mutation"},
            {
                data: "PubMed",
                render: function (data, type, row, meta) {
                    if (data) {
                        if (data.toLowerCase() === 'na') {
                            return 'NA';
                        }
                        else {
                            return '<a href="https://www.ncbi.nlm.nih.gov/pubmed/' + data + '" target="_blank" rel="noopener noreferrer">' + data + '</a>';
                        }
                    }
                    else
                        return '';
                }
            },
            {
                data: "SpliceAI_DS_AG",
                className: "text-end pe-2"
            },
            {
                data: "SpliceAI_DS_AL",
                className: "text-end pe-2"
            },
            {
                data: "SpliceAI_DS_DG",
                className: "text-end pe-2"
            },
            {
                data: "SpliceAI_DS_DL",
                className: "text-end pe-2"
            },
            {
                data: "SpliceAI_DP_AG",
                className: "text-end pe-2"
            },
            {
                data: "SpliceAI_DP_AL",
                className: "text-end pe-2"
            },
            {
                data: "SpliceAI_DP_DG",
                className: "text-end pe-2"
            },
            {
                data: "SpliceAI_DP_DL",
                className: "text-end pe-2"
            }
        ],
        select: {
            style: 'multi',
            selector: '.row-check'
        },
        rowCallback: function(row, data ) {
            if (selectedRowSet.has(data.MUT_ID+':'+data.SomaticView_ID)) {
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
                if (!selectedRowSet.has(rows_data[i].MUT_ID+':'+rows_data[i].SomaticView_ID)){
                    selectedRowSet.add(rows_data[i].MUT_ID+':'+rows_data[i].SomaticView_ID);
                }
            }
            updateActionButtonGroups(selectedRowSet.size);

        })
        .on( 'deselect', function ( e, dt, type, indexes ) {
            var rows_data = table.rows(indexes).data().toArray();
            for(var i=0; i< rows_data.length; i++) {
                selectedRowSet.delete(rows_data[i].MUT_ID+':'+rows_data[i].SomaticView_ID);
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
            var distinct_ids = $.map(rowIds, function (item) {
                var indx = item.indexOf(':');
                return item.substring(indx+1);
            });
            var include_criteria = [{'column_name': 'SomaticView_ID', 'vals': distinct_ids}];
            if (include_criteria){
                criteria_map = {
                    include: include_criteria,
                    exclude: []
                }
            }

        }
        else{
            criteria_map = $('#criteria_div').data('criteria');
        }
        download_csv('tp53db_somatic_mutations', 'SomaticView', criteria_map);
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
    var form = $("<form method='POST' action='get_distribution'></form>");
    var input;
    if (selectedRowSet.size){
        var rowIds = Array.from(selectedRowSet);
        var mutIds = $.map(rowIds, function (item) {
            var indx = item.indexOf(':');
            return item.substring(0,indx);
        });

        var criteria = { include: [{'column_name': 'MUT_ID', 'vals': mutIds}], exclude:[]};
        $("<input>", { value: JSON.stringify(criteria), name: 'criteria', type: 'hidden' }).appendTo(form);

    }
    else{
        $("<input>", { value: JSON.stringify($('#criteria_div').data('criteria')), name: 'criteria', type: 'hidden' }).appendTo(form);
    }

    input = $("<input type='hidden' name='action' value='" + action + "'/>");
    input.appendTo(form);

    input = $("<input type='hidden' name='query_dataset' value='Somatic'/>");
    input.appendTo(form);

    form.appendTo($("body"));
    form.submit();
    form.remove();
};
