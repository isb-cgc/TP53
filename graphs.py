###
# Copyright 2021, ISB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

from google.api_core.exceptions import BadRequest
import concurrent.futures
import requests
import copy
import bq_builder


def build_graph_configs(action, table=None):

    if action == 'get_mutation_dist':
        graph_configs = {
            'exon_intron': {
                'query_type': 'group_counts',
                'group_by': 'ExonIntron',
                # 'include_vals': exon_intron_labels,
                # 'exclude_vals': ['', 'NA']
            },
            'type': {
                'query_type': 'group_counts',
                'group_by': 'Type',
                'exclude_vals': ['']
            },
            'codon_no': {
                'query_type': 'group_counts',
                'group_by': 'Codon_number',
                'exclude_vals': [0]
            },
            'effect': {
                'query_type': 'group_counts',
                'group_by': 'Effect',
                'exclude_vals': ['']
            },
            'mut_pt': {
                'query_type': 'group_counts',
                'group_by': 'Effect',
                'exclude_vals': ['']
            },
            'mut_pt_s': {
                'query_type': 'mutation_rate',
                'exclude_vals': [''],
                'label_by': 'Effect'
            },
            'sift_class': {
                'query_type': 'group_counts',
                'group_by': 'SIFTClass',
                'exclude_vals': ['']
            },
            'sift_class_s': {
                'query_type': 'mutation_rate',
                'label_by': 'SIFTClass',
                'exclude_vals': ['']
            },
            'ta_class': {
                'query_type': 'group_counts',
                'group_by': 'TransactivationClass',
                'exclude_vals': ['']
            },
            'ta_class_s': {
                'query_type': 'mutation_rate',
                'label_by': 'TransactivationClass',
                'exclude_vals': ['']
            }
        }
    elif action == 'get_mutation_type':
        graph_configs = {
            'type': {
                'query_type': 'group_counts',
                'group_by': 'Type',
                'exclude_vals': ['']
            },
            'effect': {
                'query_type': 'group_counts',
                'group_by': 'Effect',
                'exclude_vals': ['']
            }
        }
    elif action == 'get_codon_dist':
        graph_configs = {
            'codon_dist': {
                'query_type': 'codon_counts',
                'codon_col': 'Codon_number'
            }
        }
    elif action == 'get_tumor_dist':
        stat_graph_col = 'StatisticGraphGermline' if table == 'GermlineTumorStats' else 'StatisticGraph'
        count_col = 'Count' if table == 'GermlineTumorStats' else 'DatasetRx'
        graph_configs = {
            'tumor_dist': {
                'query_type': 'group_sums',
                'group_by': stat_graph_col,
                'sum_col': count_col
            }
        }
    else:
        graph_configs = {
            'tumor_dist': {
                'query_type': 'group_counts',
                'group_by': 'Short_topo'
            }
        }
    return graph_configs

def build_graph_sqls(graph_configs, criteria_map, table):
    sql_maps = {}
    # build sql_maps
    for graph_id in graph_configs:
        if criteria_map:
            cri = copy.deepcopy(criteria_map)
        else:
            cri = {
                'include': [],
                'exclude': []
            }

        if graph_configs[graph_id].get('group_by') and graph_configs[graph_id].get('include_vals'):
            include_cri = {'column_name': graph_configs[graph_id]['group_by']}
            include_vals = graph_configs[graph_id].get('include_vals')
            if include_vals and len(include_vals) > 0:
                if type(include_vals[0]) == int:
                    include_cri['vals'] = include_vals
                    include_cri['wrap_with'] = ''
                else:
                    include_cri['vals'] = include_vals
                    include_cri['wrap_with'] = '"'
            cri['include'].append(include_cri)
        if graph_configs[graph_id].get('group_by') and graph_configs[graph_id].get('exclude_vals'):
            exclude_cri = {'column_name': graph_configs[graph_id]['group_by']}
            exclude_vals = graph_configs[graph_id].get('exclude_vals')
            if exclude_vals and len(exclude_vals) > 0:
                if type(exclude_vals[0]) == int:
                    exclude_cri['vals'] = exclude_vals
                    exclude_cri['wrap_with'] = ''
                else:
                    exclude_cri['vals'] = exclude_vals
                    exclude_cri['wrap_with'] = '"'
            cri['exclude'].append(exclude_cri)

        if graph_id == 'mut_pt' or graph_id == 'mut_pt_s':
            cri['include'].append(
                {'column_name': 'Effect', 'vals': ["missense", "nonsense", "silent"], 'wrap_with': '"'})
        elif graph_id == 'sift_class' or graph_id == 'sift_class_s' or graph_id == 'ta_class' or graph_id == 'ta_class_s':
            cri['include'].append({'column_name': 'Effect', 'vals': ["missense"], 'wrap_with': '"'})

        query_type = graph_configs[graph_id]['query_type']
        if query_type == 'group_sums':
            stm = bq_builder.build_mutation_dist_sum_query(criteria_map=cri, table=table,
                                                           group_by=graph_configs[graph_id]['group_by'],
                                                           sum_col=graph_configs[graph_id]['sum_col'])
        elif query_type == 'codon_counts':
            stm = bq_builder.build_codon_dist_query(column=graph_configs[graph_id]['codon_col'], table=table)
        elif query_type == 'mutation_rate':
            label_by=graph_configs[graph_id].get('label_by', 'effect')
            stm = bq_builder.build_mutation_rate_query(criteria_map=cri, table=table, label_by=label_by)
            print(stm)
        else:
            stm = bq_builder.build_mutation_query(criteria_map=cri, table=table, group_by=graph_configs[graph_id]['group_by'])
        sql_maps[graph_id] = stm
    return sql_maps

def build_graph_data(bq_client, sql_maps):
    query_jobs = {}
    for graph_id in sql_maps:
        job = bq_client.query(sql_maps[graph_id])
        query_jobs[graph_id] = job
    graph_data = {}
    error_msg = None
    try:
        for graph_id in query_jobs:
            result = query_jobs[graph_id].result(timeout=30)
            data = []
            total = 0
            is_scatter_chart = False
            for sf in result.schema:
                if sf.name == 'RATE':
                    is_scatter_chart = True
                    break
            rows = list(result)
            labels = []
            datasets = {}
            for row in rows:
                label = row.get('LABEL')
                labels.append(label)

                mut_rate = row.get('RATE', None)
                cnt = row.get('CNT')
                if is_scatter_chart:
                    name = row.get('NAME', None)
                    if not datasets.get(label):
                        datasets[label] = []
                    datasets[label].append(
                        {
                            'name': name,
                            'rate': mut_rate,
                            'count': cnt
                        }
                    )

                else:
                    data.append(cnt)
                total += cnt
            graph_data[graph_id] = {
                'chart_type': 'scatter' if is_scatter_chart else 'count',
                'labels': labels,
                'data': data,
                'datasets': datasets,
                'total': total
            }
    except BadRequest:
        error_msg = "There was a problem with your search input. Please revise your search criteria and search again."
    except (concurrent.futures.TimeoutError, requests.exceptions.ReadTimeout):
        error_msg = "Sorry, query job has timed out."

    graph_result = {'graph_data': graph_data, 'msg': error_msg}
    return graph_result
