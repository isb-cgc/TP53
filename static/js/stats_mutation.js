/* stats_mutation.js */
'use strict';

$(document).ready(function () {
    var graph_configs = {
        'tumor_dist': {
            id: 'tumor_dist',
            title: 'Tumor Distribution',
            type: 'bar',
            horizontal: true,
            x_scale: null,
            y_scale: pecentile_scale
        },
        'somatic_tumor_dist': {
            id: 'somatic_tumor_dist',
            title: 'Somatic Mutations: Tumor Distributions',
            type: 'bar',
            horizontal: true,
            x_scale: null,
            y_scale: pecentile_scale
        },
        'germline_tumor_dist': {
            id: 'germline_tumor_dist',
            title: 'Germline Mutations: Tumor Distribution',
            type: 'bar',
            horizontal: true,
            x_scale: null,
            y_scale: pecentile_scale
        },
        'type': {
            id: 'type',
            title: 'Mutation Pattern',
            type: 'pie'
        },
        'effect': {

            id: 'effect',
            title: 'Mutation Effect',
            type: 'pie'
        },
        'codon_dist': {
            id: 'codon_dist',
            title: 'Codon Distribution',
            type: 'bar',
            horizontal: false,
            x_scale: codon_scale,
            y_scale: pecentile_scale
        },
        'exon_intron': {
            id: 'exon_intron',
            title: 'Exon/Intron Distribution',
            type: 'bar',
            horizontal: false,
            x_labels: get_exon_intron_labels(),
            x_scale: exon_scale,
            y_scale: pecentile_scale
        },
        'codon_no': {
            id: 'codon_no',
            title: 'Codon Distribution',
            type: 'bar',
            horizontal: false,
            x_scale: codon_scale,
            y_scale: pecentile_scale,
            graph3D_id: 'struct_3D'
        },
        'mut_pt': {
            id: 'mut_pt',
            title: 'Point Mutation',
            type: 'pie'
        },
        'sift_class': {
            id: 'sift_class',
            title: 'SIFT',
            type: 'pie'
        },
        'ta_class': {
            id: 'ta_class',
            title: 'Transactivation',
            type: 'pie'
        }
    };




    for (const graph_id in graph_configs) {
        draw_charts(graph_configs[graph_id], null, true, true);
    }

    $('button.d-data-btn').on('click', function () {
        var graph_id = $(this).parents('.btn-group').data('graph-id');
        var graph_data = graph_result['graph_data'][graph_id];
        var filename = graph_id+'_data.tsv';
        var downloadable_data = convert_chartdata(graph_data);
        trigger_file_download(filename, downloadable_data);
    });


    $('#expand-modal').on('shown.bs.modal', function (e) {
        var button = e.relatedTarget;
        var graph_id = $(button).parents('.btn-group').data('graph-id');
        if (graph_id === 'struct_3D') {
            $('#expanded-struct3D').parent('div').removeClass('col-5').addClass('col-10');
            var width = $('#expanded-struct3D').parent('div').width();
            var height = width * .65;
            var jsmol_Info = $('#struct_3D').data('jmol-info');
            jsmol_Info.width = width;
            jsmol_Info.height = height;
            Jmol.setDocument(false);
            Jmol.getApplet("tp53JSmolCopy", jsmol_Info);
            $('#expanded-struct3D').html(Jmol.getAppletHtml(tp53JSmolCopy));
        }
    });

    $('button.expand-btn').on('click', function () {
        var graph_id = $(this).parents('.btn-group').data('graph-id');
        var expanded_chart = Chart.getChart('expanded-canvas');
        if (expanded_chart)
            expanded_chart.destroy();

        if (graph_id === 'struct_3D'){
            $('#expanded-canvas').hide();
            $('.jsmol-content').show();
        }
        else{
            $('#expanded-struct3D').html('');
            $('.jsmol-content').hide();
            $('#expanded-canvas').show();
            draw_charts(graph_configs[graph_id], 'expanded-canvas', false, false);
        }
    });

    $('button.d-img-btn').on('click', function () {
        var graph_id = $(this).parents('.btn-group').data('graph-id');
        var filename = graph_id+'_data.png';
        const chart = Chart.getChart(graph_id+'_chart');
        trigger_file_download(filename, chart.toBase64Image());
    });

    $('button.d-jsmoldata-btn').on('click', function () {
        var graph_id = $(this).parents('.btn-group').data('graph-id');
        var jsmol_select_data = $('#'+graph_id).data('jmol');
        var downloadable_data = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(jsmol_select_data));
        var filename = graph_id+'_data.json';
        trigger_file_download(filename, downloadable_data);
    });
});

var draw_charts = function (graph_config, target_id, is_dimension_static, include_3d_graph) {
    var graph_id = graph_config.id;
    var canvas_id = target_id || graph_id + '_chart';
    var graph_type = graph_config.type;
    var graph_title = graph_config.title;
    var graph_data = graph_result['graph_data'][graph_id];
    if (graph_data) {
        if (graph_type === 'bar') {
            var horizontal = graph_config.horizontal;
            var x_scale = graph_config.x_scale;
            var y_scale = graph_config.y_scale;
            if (Object.keys(graph_config).includes('x_labels')) {
                var x_labels = graph_config.x_labels;
                var graph_x = graph_data.labels;
                var graph_y = graph_data.data;
                var temp_data = [];
                for (var j = 0; j < x_labels.length; j++) {
                    var ind = graph_x.indexOf(x_labels[j]);
                    temp_data.push(ind > -1 ? graph_y[ind] : 0);
                }
                graph_data.labels = x_labels;
                graph_data.data = temp_data;
            }
            $('#' + canvas_id).parent('div').filter('.small-chart').removeClass('col-5').addClass('col-10');
            build_bar_config(canvas_id, graph_title, graph_data, horizontal, x_scale, y_scale, true);
        }
        else { // pi chart
            if (!is_dimension_static)
                $('#' + canvas_id).parent('div').filter('.small-chart').removeClass('col-10').addClass('col-5');
            build_pie_config(canvas_id, graph_title, graph_data);
        }
        if (include_3d_graph && Object.keys(graph_config).includes('graph3D_id')) {
            var jmol_legend = $('#jmol-legend');
            var width = jmol_legend.width();
            var height = $('#codon_no_chart').height() - jmol_legend.height();
            build_3d_graph(graph_config['graph3D_id'], graph_data, width, height);
        }
    }
};
