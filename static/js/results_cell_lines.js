/*results_cell_lines.js*/
'use strict';

$(document).ready(function () {
    $('.serverside-processed').DataTable({
        "pageLength": 10,
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/cl_query",
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
        "order": [[1, "asc"]],
        "columns": [
            {
                "data": "CellLineView_ID",
                "visible": false,
                "searchable": false
            },
            {"data": "Sample_Name"},
            {"data": "Short_topo"},
            {"data": "Morphology"},
            {
                "data": "ATCC_ID",
                "render": function (data) {
                    if (data)
                        return '<a href="http://www.lgcstandards-atcc.org/Products/All/' + data + '.aspx" target="_blank">' + data + '</a>';
                    else
                        return '';
                }
            },
            {
                "data": "Cosmic_ID",
                "render": function (data) {
                    if (data)
                        return '<a href="http://cancer.sanger.ac.uk/cell_lines/sample/overview?id=' + data + '" target="_blank">' + data + '</a>';
                    else
                        return '';
                }

            },
            {
                "data": "depmap_ID",
                "render": function (data) {
                    if (data)
                        return '<a href="https://depmap.org/portal/cell_line/' + data + '" target="_blank">' + data + '</a>';
                    else
                        return '';
                }
            },
            {"data": "Sex"},
            {"data": "Age"},
            {"data": "TP53status"},
            {"data": "ExonIntron"},
            {
                "data": "c_description",
                "render": function (data) {
                    return '<a href="javascript:displayGeneVariations(\'cdna\', \'' + data + '\');">' + data + '</a>';
                }
            },

            {
                "data": "ProtDescription",
                "render": function (data) {
                    return '<a href="javascript:displayGeneVariations(\'p\', \'' + data + '\');">' + data + '</a>';
                }
            },
            {
                "data": "Pubmed",
                "render": function (data) {
                    return '<a href="https://www.ncbi.nlm.nih.gov/pubmed/' + data + '" target="_blank">' + data + '</a>';
                }
            }
        ]
    });
});