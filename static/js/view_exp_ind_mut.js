/* view_exp_ind_mut.js*/
'use strict';

// const CHECKBOX_COL_ORD = 0;
const EXPOSURE_COL_ORD = 1;
const MUT_ID_COL_ORD = 9;

$(document).ready(function () {
    const selectedRowSet = new Set();
    var table = $('#eim-result-table').DataTable(
        {
            dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
                "<'row d-none'<'col-sm-12 col-md-4'B>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
            buttons: [{
                extend: 'csv',
                exportOptions: {
                    columns: ':not(:first-child):not(:last-child)'
                }
            }],
            order: [[EXPOSURE_COL_ORD, "asc"]],
            columns: [
                {
                    data: 'mut_id',
                    render: function (data, type, row, meta) {
                        return '<input class="form-check-input row-check" type="checkbox" aria-label="Select Row" value="' + data + '">';
                    },
                    orderable: false
                },
                {
                    data: 'exposure'
                },
                {
                    data: 'g_desc'
                },
                {
                    data: 'c_desc',
                    render: function (data, type, row, meta) {
                        return '<a href="javascript:displayGeneVariations(\'cdna\',\'' + data + '\');">' + data + '</a>';
                    }
                },
                {
                    data: 'p_desc',
                    render: function (data, type, row, meta) {
                        return '<a href="javascript:displayGeneVariations(\'p\',\'' + data + '\');">' + data + '</a>';
                    }
                },
                {
                    data: 'model'
                },
                {
                    data: 'clone_id'
                },
                {
                    data: 'add_info'
                },
                {
                    data: 'pubmed',
                    render: function (data, type, row, meta) {
                        return '<a href="https://www.ncbi.nlm.nih.gov/pubmed/' + data + '" target="_blank">' + data + '</a>';
                    }
                },
                {
                    data: 'row_id',
                    visible: false
                }
            ],
            select: {
                style: 'multi',
                selector: '.row-check'
            },
            rowCallback: function (row, data) {
                if (selectedRowSet.has(data[MUT_ID_COL_ORD])) {
                    selectRow(row);
                    $(row).find('.row-check').prop('checked', true);
                }
            }
        }
    );
    $('input.check-all').on('change', function (e) {
        var is_checked = $(this).is(':checked');
        selectAllRows(table, is_checked);
    });

    table
        .on('select', function (e, dt, type, indexes) {
            var rows_data = table.rows(indexes).data().toArray();
            for (var i = 0; i < rows_data.length; i++) {
                if (!selectedRowSet.has(rows_data[i][MUT_ID_COL_ORD])) {
                    selectedRowSet.add(rows_data[i][MUT_ID_COL_ORD]);
                }
            }
            updateActionButtonGroups(selectedRowSet.size);

        })
        .on('deselect', function (e, dt, type, indexes) {
            var rows_data = table.rows(indexes).data().toArray();
            for (var i = 0; i < rows_data.length; i++) {
                selectedRowSet.delete(rows_data[i][MUT_ID_COL_ORD]);
            }
            updateActionButtonGroups(selectedRowSet.size);
        });

    var selectRow = function (r) {
        table.row(r).select();
    };

    $('button.action-button').on('click', function () {
        displayGeneVariations_by_mutids(selectedRowSet);
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

var updateActionButtonGroups = function (selectedRowCounts) {
    $('.cart-count').html(selectedRowCounts);
    $('.action-button').toggleClass('disabled', selectedRowCounts === 0);
};


var displayGeneVariations_by_mutids = function (selectedRowSet) {
    var rowIds = Array.from(selectedRowSet);
    var form = $("<form method='POST' action='results_gene_mut_by_mutids'></form>");
    for (var i = 0; i < rowIds.length; i++) {
        var indx = rowIds[i].indexOf(':');
        var input = $("<input type='hidden' name='mut_id_list' value='" + rowIds[i].substring(0, indx) + "'/>");
        input.appendTo(form);
    }
    form.appendTo($("body"));
    form.submit();
    form.remove();
};
