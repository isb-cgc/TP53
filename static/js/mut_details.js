/* mut_details.js */
'use strict';

$(document).ready(function () {
    $('.clientside-processed').DataTable(
    );
    $('button.download-pdf-btn').on('click', function(){
        generatePDF();
    });
});

var generatePDF = function() {

    var element = document.getElementById('mut_details');

    var opt = {
        filename: 'mutation_details.pdf',
        margin: 8,
        pagebreak: { mode: 'avoid-all', before: '#page2el' }
    };

    var worker = html2pdf().from(element)
        .set(
            opt
        )
        .save();

};