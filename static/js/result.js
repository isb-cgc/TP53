/*result.js*/
'use strict';

$(document).ready(function () {
    $('.clientside-processed').DataTable(
        // {
        //     buttons: [
        //         {
        //             text: '<i class="fas fa-download" style="margin-right: 5px;"></i>Download Results',
        //             extend: 'csvHtml5',
        //             fieldSeparator: '\t',
        //             extension: '.tsv'
        //         }
        //     ]
        // }
    );

    // var criteria = $('#criteria_div').data('criteria');
    // console.log(criteria);




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