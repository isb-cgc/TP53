/* build_chart_config.js */
'use strict';
const color_scheme = ["#4e79a7", "#f28e2c", "#e15759", "#76b7b2", "#59a14f", "#edc949", "#af7aa1", "#ff9da7",
    "#9c755f", "#bab0ab", "#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
    "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f"];

const codon_scale = {
    min: 0,
    max: 393,
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

const exon_scale = {
    title: {
        text: 'Exon',
        display: true
    }
};

const pecentile_scale = {
    ticks: {
        callback: function (value) {
            return value + '%';
        }
    }
};

const get_exon_intron_labels = function () {
    var labels = [];
    for (var i = 1; i < 12; i++) {
        labels.push(i + '-exon');
        if (i === 11)
            break;
        labels.push(i + '-intron');
    }
    return labels;
};

var build_bar_config = function (chart_id, chart_title, data, is_horizontal, x_scale, y_scale, is_dist_chart) {

    var total_cnt = data['total'];

    var chart_data = {
        labels: data['labels'],
        datasets: [{
            data: is_dist_chart ? (data['data'].map(function (x) {
                return x * 100 / total_cnt;
            })) : data['data']
        }]
    };
    var scale_option = {};


    if (is_horizontal && y_scale) {
        scale_option.x = y_scale;
    } else {
        if (y_scale != null) {
            scale_option.y = y_scale;
        }
        if (x_scale != null) {
            scale_option.x = x_scale;
        }
    }

    var aspectRatio = function () {
        if (is_horizontal) {
            var no_of_bars = data['labels'].length;
            if (no_of_bars > 20)
                return (35 / no_of_bars);
            else if (no_of_bars > 5)
                return 2;
            else if (no_of_bars > 0)
                return 10 / no_of_bars;
            else //0
                return 4;
        } else
            return 2;
    };
    var config = {
        type: 'bar',
        data: chart_data,
        options: {
            indexAxis: is_horizontal ? 'y' : 'x',
            scales: scale_option,
            aspectRatio: aspectRatio(),
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
                            if (is_dist_chart) {
                                var percent = tooltipItem.raw;
                                var dataIndex = tooltipItem.dataIndex;
                                var count = data['data'][dataIndex];
                                return (percent).toFixed(2) + '% (' + formatNumbersByCommas(count) + ')';
                            } else {
                                return (tooltipItem.raw).toFixed(2) + '%';
                            }
                        }
                    }
                }
            }
        }
    };
    $('#' + chart_id).parent('div').filter('.small-chart').removeClass('col-5');
    // $('#'+chart_id).parent('div').filter('.small-chart').removeClass('col-5').addClass('col-10');
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
            backgroundColor: color_scheme
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
                            var tooltip_label = tooltipItem.label || 'null';
                            return tooltip_label + '  ' + (percent).toFixed(2) + '% (' + formatNumbersByCommas(count) + ')';
                        }
                    }
                },
                legend: {
                    position: 'bottom',
                    align: 'start'
                }
            }
        }
    };
    new Chart(
        document.getElementById(chart_id),
        config
    );
};

var build_scatter_plot = function (chart_id, chart_title, data) {
    var total_cnt = data['total'];
    var datasets = [];
    var labels = Object.keys(data.datasets);
    for (var i = 0; i < labels.length; i++) {
        var d_set = {
            label: labels[i],
            data: data.datasets[labels[i]].map(function (d) {
                if (d['rate'] != null) {
                    return {
                        x: d['count'] / total_cnt * 100,
                        y: d['rate'],
                        name: d['name'],
                        label: labels[i]
                    };
                }
            }),
            borderColor: color_scheme[i],
        };
        datasets.push(d_set);
    }
    var chart_data = {
        datasets: datasets,
    };

    var config = {
        type: 'scatter',
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
                            var mut_rate = tooltipItem.formattedValue; //y
                            var percent = tooltipItem.label; //x
                            var name = tooltipItem.raw.name; //aa_change
                            var d_set = tooltipItem.raw.label;  //
                            return name + ': ' + d_set + ' (' + percent + '%, ' + mut_rate + ')'
                        }
                    }
                },
                legend: {
                    position: 'bottom',
                    align: 'start'
                }
            },
            scales: {
                x: {
                    title: {
                        text: 'Variant Rate (%)',
                        // display: true,
                    },
                    ticks: {
                        // Include a dollar sign in the ticks
                        callback: function (value, index, values) {
                            return value + '%';
                        }
                    }
                },
                y: {
                    title: {
                        text: 'log(Nucleotide Substitute Rate)',
                        display: true,
                    }
                },
            },
            aspectRatio: 1

        }
    };

    new Chart(
        document.getElementById(chart_id),
        config
    );
};

var build_3d_graph = function (chart_id, data, width, height) {
    var total_cnt = data['total'];
    var y_data = data['data'];
    var x_data = data['labels'];
    var maxValue = Math.max.apply(Math, y_data);
    var maxPercent = maxValue * 100 / total_cnt;
    var highThreshold = maxPercent * .75;
    var mediumThreshold = maxPercent * .5;
    var lowThreshold = maxPercent * .25;
    var data_by_threshold = {
        high: [],
        mid: [],
        low: []
    };
    for (var i = 0; i < y_data.length; i++) {
        var percent = y_data[i] * 100 / total_cnt;
        if (percent >= highThreshold) {
            data_by_threshold.high.push(x_data[i]);
        } else if (percent >= mediumThreshold) {
            data_by_threshold.mid.push(x_data[i]);
        } else if (percent >= lowThreshold) {
            data_by_threshold.low.push(x_data[i]);
        }
    }

    var color_by_threshold = {
        high: 'red',
        mid: 'orange',
        low: 'yellow'
    };

    var jsmolQueries = '';

    for (const threshold in data_by_threshold) {
        if (data_by_threshold[threshold].length > 0)
            jsmolQueries += "Select " + data_by_threshold[threshold].join() + "; colour atoms " + color_by_threshold[threshold] + " ; wireframe 0.25; ";

    }
    var jsmol_script = "load " + pdb_filepath + "; rotate x 30; translate x 0.43; translate y 1.14; wireframe off; colour atoms [255,255,255]; spacefill off; select (*:E); wireframe on; select(*:F); wireframe on; select(*:B); cartoons on;" + jsmolQueries + " select (*:E); colour atoms [255,255,255]; select (*:F); colour atoms [255,255,255];";

    var jsmol_Info = {
        width: width,
        height: height,
        debug: false,
        color: "black",
        use: "HTML5",
        j2sPath: j2s_path,
        isSigned: true,
        disableJ2SLoadMonitor: true,
        allowJavaScript: true,
        script: jsmol_script,
        zIndexBase: 100
    };

    Jmol.setDocument(false);
    Jmol.getApplet("tp53JSmol", jsmol_Info);

    $('#' + chart_id).data('jmol', data_by_threshold);
    $('#' + chart_id).data('jmol-info', jsmol_Info);
    $('#' + chart_id).html(Jmol.getAppletHtml(tp53JSmol));
};


var formatNumbersByCommas = function (num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

let convert_chartdata = function (chartjs_data) {
    let tsv_data = '';
    let total_count = chartjs_data.total;
    let chart_type = chartjs_data.chart_type; //'scatter', 'ratio' or 'count'
    if (chart_type === 'scatter' && 'datasets' in chartjs_data) {
        let chart_datasets = chartjs_data.datasets;
        let datasets = Object.keys(chart_datasets);
        if (datasets.length) {
            tsv_data += "Label\tAAchange\tlog(Mut_rateAA)\tCount (N=" + formatNumbersByCommas(total_count) + ")\t%\n";
            for (let i = 0; i < datasets.length; i++) {
                let ds = datasets[i];
                for (let j = 0; j < chart_datasets[ds].length; j++) {
                    tsv_data += ds + '\t';
                    tsv_data += chart_datasets[ds][j].name + '\t';
                    let rate = (chart_datasets[ds][j].rate ? chart_datasets[ds][j].rate.toFixed(3) : '');
                    tsv_data += rate + '\t';
                    tsv_data += chart_datasets[ds][j].count + '\t';
                    tsv_data += (chart_datasets[ds][j].count * 100 / total_count).toFixed(3) + '\n';
                }
            }
        }
    }

    if (tsv_data === '' && chartjs_data.data.length) {
        if (chart_type === 'ratio') {
            tsv_data += 'Label\t% (N=' + formatNumbersByCommas(total_count) + ')\n';
        } else {
            tsv_data += 'Label\tCount (N=' + formatNumbersByCommas(total_count) + ')\t%\n';
        }
        for (let k = 0; k < chartjs_data.data.length; k++) {
            let label = chartjs_data.labels[k];
            let val = chartjs_data.data[k];
            tsv_data += label + '\t';
            if (chart_type === 'ratio') {
                tsv_data += val.toFixed(2) + '\n';
            } else {
                tsv_data += val + '\t' + (val * 100 / total_count).toFixed(2) + '\n';
            }
        }
    }

    tsv_data = 'data:text/tab-separated-values;charset=utf-8,' + tsv_data;
    return encodeURI(tsv_data);
};

// var trigger_file_download = function(filename, data){
//     var d_link = document.createElement('a');
//     d_link.setAttribute('href', data);
//     d_link.setAttribute('download', filename);
//     document.body.appendChild(d_link); // Required for FF
//     d_link.click();
//     document.body.removeChild(d_link);
// };

