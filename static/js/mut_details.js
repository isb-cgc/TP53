/* mut_details.js */
'use strict';

$(document).ready(function () {
    $('.clientside-processed').DataTable(
    );

    $('button.download-btn').on('click', function(){
        var tsv_data = $(this).data('download');
        var downloadable_data =  encodeURI(tsv_data);
        var filename = 'mutation_details.tsv'
        trigger_file_download(filename, downloadable_data);
        // generatePDF();
    });

    // $('button.download-pdf-btn').on('click', function(){
    //     generatePDF();
    // });
});


// var trigger_file_download = function(filename, data){
//     var d_link = document.createElement('a');
//     d_link.setAttribute('href', data);
//     d_link.setAttribute('download', filename);
//     document.body.appendChild(d_link); // Required for FF
//     d_link.click();
//     document.body.removeChild(d_link);
// };

// var generatePDF = function() {
//
//     var element = document.getElementById('mut_details');
//
//     var opt = {
//         filename: 'mutation_details.pdf',
//         margin: 8,
//         pagebreak: { mode: 'avoid-all', before: '#page2el' }
//     };
//
//     var worker = html2pdf().from(element)
//         .set(
//             opt
//         )
//         .save();
//
// };