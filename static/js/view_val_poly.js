/* view_val_poly.js*/
'use strict';

$(document).ready(function () {
    var table = $('#val-poly-result-table').DataTable(
        {
            initComplete: function (settings, json) {
                $('.spinner').hide();
            },
            dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
            columns: [
                {
                    data: 'g_desc'
                },
                {
                    data: 'c_desc',
                    render: function(data){
                        if (data)
                            return '<a class="do-gvsearch" data-gv-type="cdna">' + data + '</a>';
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
                            return '<a href="https://www.ncbi.nlm.nih.gov/snp/rs'+data+'" target = "_blank" rel="noopener noreferrer" >'+data+'</a>';
                        else return '';
                    }
                },
                {
                    data: 'gnomAd',
                    render: function(data) {
                        if (data)
                            return ' <a href="http://gnomad.broadinstitute.org/variant/' + data + '" target = "_blank" rel="noopener noreferrer" >' + data + '</a>';
                        else return '';
                    }
                },
                {
                    data: 'clinvar',
                    render: function(data) {
                        if (data && data != 'None')
                            return '<a href="https://www.ncbi.nlm.nih.gov/clinvar/variation/'+data+'" target="_blank" rel="noopener noreferrer">' + data + '</a>';
                        else return '';
                    }
                },
                {
                    data: 'pubmed',
                    render: function (data) {
                        if (data && data.toLowerCase() != 'none')
                            return '<a href="https://www.ncbi.nlm.nih.gov/pubmed/' + data + '" target="_blank" rel="noopener noreferrer">' + data + '</a>';
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
        var criteria_map = {};
        var include_criteria = $('#criteria_div').data('criteria');
        if (include_criteria){
            criteria_map = {
                include: include_criteria,
                exclude: []
            }
        }
        download_csv('tp53db_validated_polymorphisms', 'MutationView', criteria_map);
    });

});


