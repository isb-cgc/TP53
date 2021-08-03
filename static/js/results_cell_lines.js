/* results_cell_lines.js */
'use strict';

$(document).ready(function () {
    console.log('datatables');
    $('.serverside-processed').DataTable({
        dom: "<'row'<'col-sm-12 col-md-6'l>>" +
                "<'row d-none'<'col-sm-12 col-md-4'B>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        buttons: [{
            extend: 'csv',
            filename: function () {
                var db_version;// default version;
                $.ajax({
                    method: "GET",
                    async: false,
                    url: "/get_db_version",
                    success: function (data) {
                        db_version = data;
                    }
                });
                return 'tp53db_cell_lines' + (db_version ? '_' + db_version : '');
            },
            action: function (e, dt, node, config) {
                download_dataset(this, e, dt, node, config);
            },
            exportOptions: {
                columns: ':visible',
                // orthogonal: 'export'
            }}],
        pageLength: 10,
        serverSide: true,
        ajax: {
            url: "/cl_query",
            type: "POST",
            data: {
                criteria: JSON.stringify($('#criteria_div').data('criteria'))
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
                        return '<a href="https://www.atcc.org/products/' + data +'"  target="_blank">' + data + '</a>';
                        // return '<a href="http://www.lgcstandards-atcc.org/Products/All/' + data + '.aspx" target="_blank">' + data + '</a>';
                    else
                        return '';
                }
            },
            {
                data: "Cosmic_ID",
                render: function (data) {
                    if (data)
                        return '<a href="http://cancer.sanger.ac.uk/cell_lines/sample/overview?id=' + data + '" target="_blank">' + data + '</a>';
                    else
                        return '';
                }

            },
            {
                data: "depmap_ID",
                render: function (data) {
                    if (data)
                        return '<a href="https://depmap.org/portal/cell_line/' + data + '" target="_blank">' + data + '</a>';
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
                        return '<a href="javascript:void(0);" class="do-gvsearch" data-gv-type="cdna">' + data + '</a>';
                    else
                        return data;
                }

            },

            {
                data: "ProtDescription",
                render: function(data){
                    if (data)
                        return '<a href="javascript:void(0);" class="do-gvsearch" data-gv-type="p">' + data + '</a>';
                    else
                        return data;
                }
            },
            {
                data: "Pubmed",
                render: function (data) {
                    return '<a href="https://www.ncbi.nlm.nih.gov/pubmed/' + data + '" target="_blank">' + data + '</a>';
                }
            }
        ]
    });
    $('.download-btn').on('click', function () {
        $('button.buttons-csv').trigger("click");
    });

});