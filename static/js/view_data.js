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
            $(this).html('<input aria-label="' + title + '" class="form-control-sm form-control" type="text" placeholder="' + title + '" />');
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
            initComplete: function (settings, json) {
                $('.spinner').hide();

            },
            dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
                "<'row d-none'<'col-sm-12 col-md-4'B>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
            buttons: [{
                extend: 'csv',
                filename: function () {
                    return bq_view_name + '_' + db_version;
                },
                exportOptions: {
                    columns: ':not(:first-child)'
                }
            }],
            columnDefs: [{
                targets: 0,
                data: null,
                render: function() {
                    return '<input class="form-check-input row-check" type="checkbox" aria-label="Select Rows">';
                },
                orderable: false
            },{
                targets: 'external_link',
                render: function (data) {
                    return '<a href="'+data+'" target="_blank" rel="noopener noreferrer">'+data+'</a>';
                }
            }
            ,{
                targets: '_all',
                className: 'pe-5 text-nowrap'
            }
            ],
            rowCallback: function (row) {
                $(row).find('.row-check').prop('checked', $(row).hasClass('selected'));
            },
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


