/* mut_details.js */
'use strict';

$(document).ready(function () {
    $('.clientside-processed').DataTable(
    );

    $('button.download-btn').on('click', function(){
        var tsv_data = $(this).data('download');
        var downloadable_data =  encodeURI(tsv_data);
        var filename = 'mutation_details.tsv';
        trigger_file_download(filename, downloadable_data);
    });

});