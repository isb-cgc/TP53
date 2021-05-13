/* build_chart_config.js */
'use strict';
const color_scheme = ["#4e79a7", "#f28e2c", "#e15759", "#76b7b2", "#59a14f", "#edc949", "#af7aa1", "#ff9da7",
    "#9c755f", "#bab0ab", "#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
    "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f"];

var codon_scale = {
    min: 0,
    max: 395,
    type: 'linear',
    offset: false,
    grid: {
        display: false
    },

    title: {
        text: 'Codon No.',
        display: true
    }
};

// var exon_scale = {
//     title: {
//         text: 'Exon',
//         display: true
//     }
// };

var pecentile_scale = {
    ticks: {
        callback: function (value) {
            return value + '%';
        }
    }
};

var build_bar_config = function (chart_id, chart_title, data, is_horizontal, x_scale, y_scale, is_dist_chart) {

    var total_cnt = data['total'];

    var chart_data = {
        labels: data['labels'],
        datasets: [{
            data: is_dist_chart ? (data['data'].map(function(x){
                    return x * 100/total_cnt;
                })): data['data']
        }]
    };
    var scale_option = {};


    if (is_horizontal && y_scale) {
        scale_option.x = y_scale;
    }
    else {
        if (y_scale != null){
            scale_option.y = y_scale;
        }
        if (x_scale != null) {
            scale_option.x = x_scale;
        }
    }

    var config = {
        type: 'bar',
        data: chart_data,
        options: {
            indexAxis: is_horizontal ? 'y' : 'x',
            scales: scale_option,
            plugins: {
                title: {
                    display: true,
                    align: 'start',
                    text: chart_title + ' ( N = ' + formatNumbersByCommas(total_cnt) + ' )'
                },
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (tooltipItem) {
                            if (is_dist_chart){
                                var percent = tooltipItem.raw;
                                var dataIndex = tooltipItem.dataIndex;
                                var count = data['data'][dataIndex];
                                return (percent).toFixed(2) + '% (' + formatNumbersByCommas(count) + ')';
                            }
                            else{
                                return (tooltipItem.raw).toFixed(2) + '%';
                            }

                        },
                    }
                }
            }
        }
    };
    // console.log(config);
    $('#'+chart_id).parent('div').removeClass('col-5').addClass('col-10');
    new Chart(
        document.getElementById(chart_id),
        config
    );
};
var build_pie_config = function (chart_id, chart_title, data) {
    var total_cnt = data['total'];
    var chart_data = {
        labels: data['labels'],
        datasets: [{
            data: data['data'],
            backgroundColor: color_scheme,
        }]
    };

    var config = {
        type: 'pie',
        data: chart_data,
        options: {
            plugins: {
                title: {
                    display: true,
                    align: 'start',
                    text: chart_title + ' ( N = ' + formatNumbersByCommas(total_cnt) + ' )'
                },
                tooltip: {
                    callbacks: {
                        label: function (tooltipItem) {
                            var count = tooltipItem.parsed;
                            var percent = count * 100 / total_cnt;
                            return tooltipItem.label + '  ' + (percent).toFixed(2) + '% (' + count + ')';
                        }
                    }
                },
                legend: {
                    position: 'bottom',
                    align: 'start'
                },
            }
        }
    };
    new Chart(
        document.getElementById(chart_id),
        config
    );
};

var formatNumbersByCommas = function(num){

    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};
