/*result.js*/
'use strict';

$(document).ready(function () {
    $('.serverside-processed').DataTable({
        "pageLength": 10,
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/gv_query",
            "type": "POST",
            "data": {
                "criteria": JSON.stringify($('#criteria_div').data('criteria'))
            },
            "dataType": "json",
            "dataSrc": "data"
        },
        "drawCallback": function () {
            enableTooltip();
        },
        "order": [[ 1, "asc" ]],
        "columns": [
            {
                "data": "MUT_ID",
                "orderable": false,
                "render": function (data) {
                    return '<input class="form-check-input" type="checkbox" aria-label="Select Row" value="' + data + '"/>';
                }
            },
            {"data": "g_description_GRCh38"},
            {"data": "c_description"},
            {
                "data": "ProtDescription",
                "render": function (data, type, row) {
                    if (data !== '' && row['Effect'] === 'missense')
                        return '<a data-bs-toggle=\"tooltip\" data-bs-placement=\"right\" title=\"Link to PHenotypic ANnotation of TP53 Mutations\" ' +
                            'href=\"https://mutantp53.broadinstitute.org/query=\'' + data + '\'\" target=\"_blank\">' + data + '</a>';
                    else
                        return data;
                }
            },
            {"data": "ExonIntron"},
            {"data": "Effect"},
            {"data": "TransactivationClass"},
            {"data": "AGVGDClass"},
            {"data": "Somatic_count"},
            {"data": "Germline_count"},
            {"data": "Cellline_count"},
            {"data": "TCGA_ICGC_GENIE_count"},
            {
                "data": "CLINVARlink",
                "render": function (data) {
                    if (data != null)
                        return '<a href=\"https://www.ncbi.nlm.nih.gov/clinvar/variation/' + data + '\" target=\"_blank\">' + data + '</a>';
                    else
                        return data;
                }
            },
            {
                "data": "COSMIClink",
                "render": function (data) {
                    if (data != null)
                        return '<a href=\"https://cancer.sanger.ac.uk/cosmic/mutation/overview?id=' + data + '\" target=\"_blank\">' + data + '</a>';
                    else
                        return data;
                }
            },
            {"data": "Polymorphism"},
            {
                "data": "SNPlink",
                "render": function (data) {
                    if (data !== '')
                        return '<a href=\"https://www.ncbi.nlm.nih.gov/snp/rs' + data + '\" target=\"_blank\">' + data + '</a>';
                    else
                        return data;
                }
            },
            {
                "data": "gnomADlink",
                "render": function (data) {
                    if (data !== '')
                        return '<a href=\"https://gnomad.broadinstitute.org/variant/' + data + '\" target=\"_blank\">yes</a>';
                    else
                        return data;
                }
            },
            {
                "data": "MUT_ID",
                "orderable": false,
                "render": function(data){
                    return '<a href="mut_details?mut_id='+data+'" type="button" style="text-decoration: none;" <i class="far fa-list-alt"></i></a>';
                }
            }
        ]

    });


    // "processing": true,
    // "serverSide": true,
    // ajax: {
    //     url: '/gv_query',
    //     dataSrc: ''
    // },
    // columns: [
    //     {data: 0},
    //     {data: 1},
    //     {data: 2},
    //     {data: 3},
    //     {data: 4},
    //     {data: 5}
    // ]
    // // "ajax": "/",
    // "dataSrc": ''
    // "ajax": {
    //     "url": "/gv_query",
    //     "type":"POST"
    // }
    //     buttons: [
    //         {
    //             text: '<i class="fas fa-download" style="margin-right: 5px;"></i>Download Results',
    //             extend: 'csvHtml5',
    //             fieldSeparator: '\t',
    //             extension: '.tsv'
    //         }
    //     ]
    //     }
    // );
    // var buttons = table.buttons().container();
    // var button_divs = $('.button-div');
    // for(var i = 0; i<buttons.length; i++){
    //     $(buttons[i]).appendTo($(button_divs[i]));
    // }
});