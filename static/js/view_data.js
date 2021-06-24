/* view_data.js */
'use strict';

$(document).ready(function () {
    $('#view-data-table thead tr').clone(true).appendTo( '#view-data-table thead' );
    $('#view-data-table thead tr:eq(1) th').each(function(i) {
        if (i === 0) {
            $(this).html('');
        }
        else {
            var title = $(this).text();
            $(this).html('<input type="text" placeholder="' + title + '" />');
            $('input', this).on('keyup change', function () {
                if (table.column(i).search() !== this.value) {
                    table
                        .column(i)
                        .search(this.value)
                        .draw();
                }
            });
        }
    });

    var table = $('#view-data-table').DataTable(
        {
            data: dataSet,
            orderCellsTop: true,
            fixedHeader: true,
            deferRender: true,
            // deferRender: totalRows > 5000,
            // deferLoading: totalRows,
            initComplete: function (settings, json) {
                $('.spinner').hide();
            },
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
            columnDefs: [{
                targets: 0,
                data: null,
                render: function() {
                    return '<input class="form-check-input row-check" type="checkbox" aria-label="Select Row">';
                },
                orderable: false,
            }],
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
        selectAllRows(is_checked);
    });


    $('.download-btn').on('click', function () {
        $('button.buttons-csv').trigger("click");
    });

    // table.on('draw.dt', function () {
        // deselect/reset the .ref-check-all checkbox whenever the table is redrawn by column searches
        // console.log('panda');
        // var check_all = $(this).find('input.check-all');
        // if(check_all.is(':checked'))
        //     check_all.prop('checked', false).change();
    // });

    var selectAllRows = function (bool) {
        var selection = '';
        if (bool) {
            table.rows( {search:'applied'} ).select();
            selection = 'tr.selected';
        }
        else {
            table.rows().deselect();
            selection = 'tr'
        }
        table.$(selection).find('input.row-check').prop('checked', bool);
    };

});


