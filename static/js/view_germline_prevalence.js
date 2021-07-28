/* view_germline_prevalence.js*/
'use strict';

$(document).ready(function () {
    var table = $('#germline-prev-result-table').DataTable(
        {
            initComplete: function (settings, json) {
                $('.spinner').hide();
            },
            dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
                "<'row d-none'<'col-sm-12 col-md-4'B>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
            buttons: [{
                extend: 'csv',
                filename: function(){
                    var db_version;// default version;
                    $.ajax({
                        method: "GET",
                        async: false,
                        url: "/get_db_version",
                        success: function (data) {
                            db_version = data;
                        }
                    });
                    return 'tp53db_germline_prevalence'+ (db_version ? '_'+db_version: '');
                }
            }],

            columns: [
                {
                    data: 'diagnosis'
                },
                {
                    data: 'cohort'
                },
                {
                    data: 'cases_anal'
                },
                {
                    data: 'cases_mutated'
                },
                {
                    data: 'mut_prevalence'
                },
                {
                    data: 'remark'
                },
                {
                    data: 'pubmed',
                    render: function (data, type, row, meta) {
                        return '<a href="https://www.ncbi.nlm.nih.gov/pubmed/' + data + '" target="_blank">' + data + '</a>';
                    }
                }
            ]
        }
    );

    $('.download-btn').on('click', function () {
        $('button.buttons-csv').trigger("click");
    });

});


