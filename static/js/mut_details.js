/* mut_details.js */
'use strict';

$(document).ready(function () {
    $('.clientside-processed').DataTable(
    );
    $('#gdc-cases-table').DataTable({
        dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6 d-flex justify-content-end' f B>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        buttons: [
            // 'csv'

        { extend: 'csv', text: '<i class="fas fa-download"></i> Download', className: 'btn-tiny ms-2' }

        ],
        pageLength: 10,
        ajax: {
            url: "/gdc_cases_query",
            type: "POST",
            data: {
                mut_id: $('#gdc-cases-table').data('mut-id')
            },
            dataType: "json",
            dataSrc: "data"
        },
        preDrawCallback: function(){
            $('.spinner').show();
        },
        drawCallback: function () {
            $('.spinner').hide();
            enableTooltip();
        },
        columns: [
            {
                data: "Program",
                orderData: [0,1]
            },
            {
                data: 'CaseBarcode',
                render: function (data, type, row) {
                    return '<a href="https://portal.gdc.cancer.gov/cases/'+ row['CaseUUID'] + '" target="_blank" rel="noopener noreferrer">' + data + '</a>';
                }
            },
            {
                data: "somatic_status"
            },{
                data: "somatic_p_value",
                render: function (data) {
                    return data.toExponential(1);
                }
            },{
                data: "variant_p_value",
                render: function (data) {
                    return data.toExponential(1);
                }
            }
        ]
    });

    $('button.download-btn').on('click', function(){
        var tsv_data = $(this).data('download');
        var downloadable_data =  encodeURI(tsv_data);
        var filename = 'mutation_details.tsv';
        trigger_file_download(filename, downloadable_data);
    });

});