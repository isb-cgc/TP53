/* stats_mutation.js */
'use strict';

$(document).ready(function () {
    var graph_config = [
        {
            id: 'tumor_dist',
            title: 'Tumor Distribution',
            type: 'bar',
            horizontal: true,
            x_scale: null,
            y_scale: pecentile_scale
        },
        {
            id: 'somatic_tumor_dist',
            title: 'Somatic Mutations: Tumor Distributions',
            type: 'bar',
            horizontal: true,
            x_scale: null,
            y_scale: pecentile_scale
        },
        {
            id: 'germline_tumor_dist',
            title: 'Germline Mutations: Tumor Distribution',
            type: 'bar',
            horizontal: true,
            x_scale: null,
            y_scale: pecentile_scale
        },
        {
            id: 'type',
            title: 'Mutation Pattern',
            type: 'pie'
        },
        {
            id: 'effect',
            title: 'Mutation Effect',
            type: 'pie'
        },
        {
            id: 'codon_dist',
            title: 'Codon Distribution',
            type: 'bar',
            horizontal: false,
            x_scale: codon_scale,
            y_scale: pecentile_scale
        },
        {
            id: 'exon_intron',
            title: 'Exon/Intron Distribution',
            type: 'bar',
            horizontal: false,
            x_labels: get_exon_intron_labels(),
            x_scale: exon_scale,
            y_scale: pecentile_scale
        },
        {
            id: 'codon_no',
            title: 'Codon Distribution',
            type: 'bar',
            horizontal: false,
            x_scale: codon_scale,
            y_scale: pecentile_scale,
            graph3D_id: 'struct_3D'
        },
        {
            id: 'mut_pt',
            title: 'Point Mutation',
            type: 'pie'
        },
        {
            id: 'sift_class',
            title: 'SIFT',
            type: 'pie'
        },
        {
            id: 'ta_class',
            title: 'Transactivation',
            type: 'pie'
        }
    ];

    for (var i = 0; i < graph_config.length; i++) {
        var graph_id = graph_config[i].id;
        var canvas_id = graph_id + '_chart';
        var graph_type = graph_config[i].type;
        var graph_title = graph_config[i].title;
        var graph_data = graph_result['graph_data'][graph_id];

        if (graph_data) {
            if (graph_type === 'bar') {
                var horizontal = graph_config[i].horizontal;
                var x_scale = graph_config[i].x_scale;
                var y_scale = graph_config[i].y_scale;
                if (Object.keys(graph_config[i]).includes('x_labels')) {
                    var x_labels = graph_config[i].x_labels;
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
                build_bar_config(canvas_id, graph_title, graph_data, horizontal, x_scale, y_scale, true);
            }
            else { // pi chart
                build_pie_config(canvas_id, graph_title, graph_data);
            }

            if (Object.keys(graph_config[i]).includes('graph3D_id')) {

                build_3d_graph(graph_config[i]['graph3D_id'], graph_data);
            }
        }
    }





        // return "load Jmol/1tsr_B.pdb; background [0,0,0]; rotate x 30; translate x 0.43; translate y 1.14; wireframe off; zoom 125; colour atoms [255,255,255]; spacefill off; select (*:E); wireframe on; select(*:F); wireframe on; select(*:B); cartoons on; " + String.Join("", jmolQueries) + "select (*:E); colour atoms [255,255,255]; select (*:F); colour atoms [255,255,255]; move 0 -360 0 0 0 0 0 0 15 25;";





});