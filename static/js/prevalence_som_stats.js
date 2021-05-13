/* prevalence_som_stats.js */
'use strict';

// var codon_scale = {
//     min: 0,
//     max: 395,
//     type: 'linear',
//     offset: false,
//     grid: {
//         display: false
//     },
//
//     title: {
//         text: 'Codon No.',
//         display: true
//     }
// };

$(document).ready(function () {

    // var x_scale = {
    //     title: {
    //         text: 'Tumor Site',
    //         display: true
    //     }
    // };

    //deep copy percentile scale and add axis label
    var y_scale = {};
    Object.assign(y_scale, pecentile_scale);
    y_scale.title = {
        text: 'Mutated Sample Ratio (%)',
        display: true
    };

    build_bar_config('som_prev_chart', 'Mutation Prevalence', graph_data, true, null, y_scale, false);
     // function (chart_id, chart_title, data, horizontal, x_scale, y_scale) {

});