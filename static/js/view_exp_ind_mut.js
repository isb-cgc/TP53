/*result.js*/
'use strict';

const CHECKBOX_COL_ORD = 0;
const EXPOSURE_COL_ORD = 1;
const MUT_ID_COL_ORD = 9;

$(document).ready(function () {
    const selectedRowSet = new Set();
    var table = $('#eim-result-table').DataTable(
        {
            order: [[EXPOSURE_COL_ORD, "asc"]],
            columnDefs: [{
                orderable: false,
                // data: 'MUT_ID',
                targets: CHECKBOX_COL_ORD
            },{
                visible: false,
                targets: MUT_ID_COL_ORD
            }
            ],
            select: {
                style: 'multi',
                selector: '.row-check'
            },
            rowCallback: function (row, data) {
                // console.log(row);
                // console.log(data);
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
        .on( 'select', function ( e, dt, type, indexes ) {
            var rows_data = table.rows(indexes).data().toArray();
            for(var i=0; i< rows_data.length; i++) {
                if (!selectedRowSet.has(rows_data[i][MUT_ID_COL_ORD])){
                    selectedRowSet.add(rows_data[i][MUT_ID_COL_ORD]);
                }
            }
            console.log(selectedRowSet);
            updateActionButtonGroups(selectedRowSet.size);

        })
        .on( 'deselect', function ( e, dt, type, indexes ) {
            var rows_data = table.rows(indexes).data().toArray();
            for(var i=0; i< rows_data.length; i++) {
                selectedRowSet.delete(rows_data[i][MUT_ID_COL_ORD]);
            }
            console.log(selectedRowSet);
            updateActionButtonGroups(selectedRowSet.size);
        } );

    var selectRow = function(r){
        table.row(r).select();
    };

    $('button.action-button').on('click', function(){
        displayGeneVariations_by_mutids(selectedRowSet);
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
