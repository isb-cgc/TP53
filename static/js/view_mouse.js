/* view_mouse.js*/
'use strict';

$(document).ready(function () {
    var table = $('#mouse-result-table').DataTable(
        {
            dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
                "<'row d-none'<'col-sm-12 col-md-4'B>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
            buttons: ['csv'],

            columns: [
                {
                    data: 'model_description'
                },
                {
                    data: 'tumor_sites'
                },
                {
                    data: 'aa_change',
                    render: function (data, type, row, meta) {
                        if (data !== 'NA'){
                            return '<a href="javascript:displayGeneVariations(\'p\',\'' + data + '\');">' + data + '</a>';
                        }
                        else return data;
                    }
                },
                {
                    data: 'camod_id'
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


