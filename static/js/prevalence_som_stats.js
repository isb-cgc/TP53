/* prevalence_som_stats.js */
'use strict';


$(document).ready(function () {

    //deep copy percentile scale and add axis label
    var y_scale = {};
    Object.assign(y_scale, pecentile_scale);
    y_scale.title = {
        text: 'Mutated Sample Ratio (%)',
        display: true
    };

    build_bar_config('som_prev_chart', 'Variant Prevalence', graph_data, true, null, y_scale, false);

    $('button.d-data-btn').on('click', function () {
        var graph_id = $(this).parents('.btn-group').data('graph-id');
        var filename = graph_id+'_data.tsv';
        var downloadable_data = convert_chartdata(graph_data);
        trigger_file_download(filename, downloadable_data);
    });

    $('button.d-img-btn').on('click', function () {
        var graph_id = $(this).parents('.btn-group').data('graph-id');
        var filename = graph_id+'_data.png';
        const chart = Chart.getChart(graph_id+'_chart');
        trigger_file_download(filename, chart.toBase64Image());
    });

});