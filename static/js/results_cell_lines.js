/* results_cell_lines.js */
'use strict';

$(document).ready(function () {
    $('.serverside-processed').DataTable({
        dom: "<'row'<'col-sm-12 col-md-6'l>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        pageLength: 10,
        serverSide: true,
        ajax: {
            url: "/cl_query",
            type: "POST",
            data: {
                criteria: JSON.stringify($('#criteria_div').data('criteria'))
            },
            error: function (result) {
                let msg = 'There has been an error while running the search. Please try again.';
                if (result.responseJSON && result.responseJSON.error_message) {
                    msg = result.responseJSON.error_message;
                }
                $('.spinner').hide();
                $('.dataTables_info').parents('.row').append(
                    '<div class="col-sm-12 text-center fw-bold"><i class="fas fa-exclamation-triangle me-2"></i>'+msg+'</div>');
            },
            dataType: "json",
            dataSrc: "data"
        },
        preDrawCallback: function(){
            $('.spinner').show();
        },

        drawCallback: function () {
            $('.spinner').hide();
            $('a.do-gvsearch').on('click', function(e){
                e.preventDefault();
                displayGeneVariations($(this).data('gv-type'), $(this).text());
            });
        },
        order: [[1, "asc"]],
        columns: [
            {
                data: "CellLineView_ID",
                visible: false,
                searchable: false
            },
            {data: "Sample_Name"},
            {data: "Short_topo"},
            {data: "Morphology"},
            {
                data: "ATCC_ID",
                render: function (data) {
                    if (data)
                        return '<a href="https://www.atcc.org/products/' + data +'"  target="_blank" rel="noopener noreferrer">' + data + '</a>';
                    else
                        return '';
                }
            },
            {
                data: "Cosmic_ID",
                render: function (data) {
                    if (data)
                        return '<a href="http://cancer.sanger.ac.uk/cell_lines/sample/overview?id=' + data + '" target="_blank" rel="noopener noreferrer">' + data + '</a>';
                    else
                        return '';
                }

            },
            {
                data: "depmap_ID",
                render: function (data) {
                    if (data)
                        return '<a href="https://depmap.org/portal/cell_line/' + data + '" target="_blank" rel="noopener noreferrer">' + data + '</a>';
                    else
                        return '';
                }
            },
            {data: "Sex"},
            {data: "Age"},
            {data: "TP53status"},
            {data: "ExonIntron"},
            {
                data: "c_description",
                render: function(data){
                    if (data)
                        return '<a class="do-gvsearch" data-gv-type="cdna">' + data + '</a>';
                    else
                        return data;
                }

            },

            {
                data: "ProtDescription",
                render: function(data){
                    if (data)
                        return '<a class="do-gvsearch" data-gv-type="p">' + data + '</a>';
                    else
                        return data;
                }
            },
            {
                data: "Pubmed",
                render: function (data) {
                    return '<a href="https://www.ncbi.nlm.nih.gov/pubmed/' + data + '" target="_blank" rel="noopener noreferrer">' + data + '</a>';
                }
            }
        ]
    });
    $('.download-btn').on('click', function () {
        var criteria_map = {};
        var include_criteria = $('#criteria_div').data('criteria');
        if (include_criteria){
            criteria_map = {
                include: include_criteria,
                exclude: []
            }
        }
        download_csv('tp53db_cell_lines', 'CellLineView', criteria_map);
    });

});