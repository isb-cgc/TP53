/* view_val_poly.js*/
'use strict';

$(document).ready(function () {
    var table = $('#val-poly-result-table').DataTable(
        {
            initComplete: function (settings, json) {
                $('.spinner').hide();
            },
            dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
                "<'row d-none'<'col-sm-12 col-md-4'B>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
            buttons: ['csv'],
            columns: [
                {
                    data: 'g_desc'
                },
                {
                    data: 'c_desc',
                    render: function(data){
                        if (data)
                            return '<a href="javascript:void(0);" class="do-gvsearch" data-gv-type="cdna">' + data + '</a>';
                        else return '';

                    }
                },
                {
                    data: 'p_desc'
                },
                {
                    data: 'exon'
                },
                {
                    data: 'effect'
                },
                {
                    data: 'snp',
                    render: function(data) {
                        if (data)
                            return '<a href = "https://www.ncbi.nlm.nih.gov/snp/rs'+data+'" target = "_blank" >'+data+'</a>';
                        else return '';
                    }
                },
                {
                    data: 'gnomAd',
                    render: function(data) {
                        if (data)
                            return ' <a href="http://gnomad.broadinstitute.org/variant/' + data + '" target = "_blank" >' + data + '</a>';
                        else return '';
                    }
                },
                {
                    data: 'clinvar',
                    render: function(data) {
                        if (data && data != 'None')
                            return '<a href="https://www.ncbi.nlm.nih.gov/clinvar/variation/'+data+'" target="_blank">' + data + '</a>';
                        else return '';
                    }
                },
                {
                    data: 'pubmed',
                    render: function (data) {
                        if (data)
                            return '<a href="https://www.ncbi.nlm.nih.gov/pubmed/' + data + '" target="_blank">' + data + '</a>';
                        else return '';
                    }
                },
                {
                    data: 'source'
                }
            ],
            drawCallback: function () {
                $('a.do-gvsearch').on('click', function(e){
                    e.preventDefault();
                    displayGeneVariations($(this).data('gv-type'), $(this).text());
                })
            },
        }
    );

    $('.download-btn').on('click', function () {
        $('button.buttons-csv').trigger("click");
    });

});


