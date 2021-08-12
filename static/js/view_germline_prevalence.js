/* view_germline_prevalence.js*/
'use strict';

$(document).ready(function () {
    var table = $('#germline-prev-result-table').DataTable(
        {
            initComplete: function (settings, json) {
                $('.spinner').hide();
            },
            dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
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
        download_csv('tp53db_germline_prevalence', 'GermlinePrevalenceView');
    });

});


