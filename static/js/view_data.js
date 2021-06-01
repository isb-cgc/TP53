/* view_data.js*/
'use strict';

$(document).ready(function () {
    var table = $('#view-data-table').DataTable(
        {
            dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
                "<'row d-none'<'col-sm-12 col-md-4'B>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
            buttons: [{
                extend: 'csv',
                exportOptions: {
                    columns: ':not(:first-child)'
                }
            }],
            columnDefs: [
                {orderable: false, targets: 0}
            ],
            order: [[1, "asc"]],
            scrollX: true,
            select: {
                style: 'multi',
                selector: '.row-check'
            }
        }
    );

    $('input.check-all').on('change', function (e) {
        var is_checked = $(this).is(':checked');
        selectAllRows(table, is_checked);
    });


    $('.download-btn').on('click', function () {
        $('button.buttons-csv').trigger("click");
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

});


