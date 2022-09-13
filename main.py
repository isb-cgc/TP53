###
# Copyright 2022, ISB
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

import os
import logging
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from flask import Flask, render_template, request, send_from_directory, json, jsonify, make_response, abort, session, redirect
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
from flask_talisman import Talisman
import settings
import bq_builder
import concurrent.futures
import requests
import csv
import utils
import graphs
import filters
from io import StringIO

from jinja2 import TemplateNotFound


app = Flask(__name__)

# Configuration for GOOGLE OAUTH
GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
# GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

app.config['TESTING'] = settings.IS_TEST
app.config['ENV'] = 'development' if settings.IS_TEST else 'production'

# length of time (in seconds) the browser will respect the HSTS header
# production and UAT should be set to 31,536,000 seconds (by not setting any HSTS_MAX_age,
# else set to 3600 (test and dev)
hsts_max_age = int(os.environ.get('HSTS_MAX_AGE') or 3600)

Talisman(app, strict_transport_security_max_age=hsts_max_age, content_security_policy={
    'default-src': [
        "\'self\'",
        '*.googletagmanager.com',
        '*.gstatic.com',
        '*.google.com',
        '*.google-analytics.com',
        '*.googleapis.com',
        "*.fontawesome.com",
        "*.googleusercontent.com",
        "\'unsafe-inline\'",
        "\'unsafe-eval\'",
        'data:'
    ]
})

GOOGLE_APPLICATION_CREDENTIALS = os.path.join(app.root_path, 'privatekey.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
bq_builder.set_project_dataset(proj_id=settings.BQ_GCP, d_set=settings.BQ_DATASET)
bigquery_client = bigquery.Client()

client_secrets_file = os.path.join(app.root_path, 'client_secret.json')
#
# Flow is OAuth 2.0 class that stores all the information on how we want to authorize our users
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"], # specify what to get after the authorization
    redirect_uri=settings.OAUTH_CALLBACK  # where to redirect after the authorization
)

TITLE_BQVIEW_MAP = {
    "MutationView": "Functional / Structural Data in <em>TP53</em> with Annotations",
    "FunctionDownload": "Functional Assessment of <em>p53</em> Mutant Proteins in Various Experimental Assays",
    "FunctionIshiokaDownload": "Systematic Functional Assessment of <em>p53</em> Mutant Proteins in Yeast Assays",
    "TumorVariantDownload": "Tumor Variants in Human Tumor Samples (Data File)",
    "TumorVariantRefDownload": "Tumor Variants in Human Tumor Samples (References File)",
    "PrevalenceDownload": "Prevalence of Tumor Variants by Tumor Site",
    "PrevalenceDownloadR249S": "Prevalence of the R249S <em>TP53</em> Variants in Liver Cancer",
    "PrognosisDownload": "Prognostic Value of Tumor Variants",
    "GermlineDownload": "<em>TP53</em> Germline Variants and Family History (Data File)",
    "GermlineRefDownload": "<em>TP53</em> Germline Variants and Family History (References File)",
    "GermlinePrevalenceView": "<em>TP53</em> Germline Variants Prevalence in Selected Cohorts",
    "GermlineFrequencyDownload": "Frequency of Individual Variants in Case-Controls Series",
    "CellLineDownload": "<em>TP53</em> Variant Status of Human Cell-lines",
    "MouseModelView": "Mouse Models with Engineered <em>TP53</em>",
    "InducedMutationView": "Variants Induced in Experimental Models of Mutagenesis"

}

#########################################
# Functional / Structural Variant Search
#########################################

#
# by Gene Variants
#
@app.route("/search_gene_by_var")
def search_gene_by_var():
    return render_template("search_tp53_gene_variants.html", c_desc_list=settings.m_c_desc_list, p_desc_list=settings.m_p_desc_list,
                           g_desc_hg19_list=settings.m_g_desc_hg19_list, g_desc_hg38_list=settings.m_g_desc_hg38_list)

#
# by Variant Features
#
@app.route("/search_gene_by_mut")
def search_gene_by_mut():
    return render_template("search_tp53_gene_by_mut.html", type_list=settings.m_type_list, desc_list=settings.m_desc_list,
                           motif_list=settings.m_motif_list, effect_list=settings.m_effect_list,
                           exon_intron_list=settings.m_exon_intron_list, ta_class_list=settings.m_ta_class_list, sift_list=settings.m_sift_list)


#
# functional/structural variation search results
# prefix options ('gv': search by gene variant, 'gmut': search by variant features
#
@app.route("/results_gene_mut/<search_by>", methods=['GET', 'POST'])
def results_gene_mut(search_by=None):
    criteria = []
    if search_by == 'gv': # search by gene variants
        criteria = filters.get_gene_variant_criteria(search_by)
    elif search_by == 'gmut': # search by variant features
        criteria = filters.get_variant_feature_criteria(search_by)
    elif search_by == 'mut_id': # search by variant ID (MUT_ID)
        criteria = filters.get_mut_id_criteria()
    return render_template("results_gene_mutation.html", criteria=criteria)


@app.route("/get_distribution", methods=['GET', 'POST'])
def get_distribution():
    criteria = filters.get_param_val('criteria')
    if criteria:
        cri = json.loads(criteria)
        if type(cri) == list:
            criteria_map = {
                'include': cri,
                'exclude': []
            }
        else:
            criteria_map = cri
    else:

        criteria_map = {
            'include': filters.get_mut_id_criteria(),
            'exclude': []
        }

    action = filters.get_param_val('action')

    # query_dataset:
    # 'Mutation' for Functional/Structural Search,
    # 'Somatic' for Somatic Search,
    # 'Germline' for Germline Search
    query_dataset = filters.get_param_val('query_dataset')

    template = 'mutation_stats.html'
    if query_dataset == 'Mutation':
        title = 'Statistics on Functional/Structural Data'
    else:
        title = 'Search Results on {query_dataset} Variants'.format(query_dataset=('Tumor' if query_dataset == 'Somatic' else query_dataset))

    if action == 'get_mutation_dist':
        table = 'GermlineView_Carriers' if query_dataset == 'Germline' else '{query_dataset}View'.format(
            query_dataset=query_dataset)
        template = 'mutation_dist_stats.html'
        subtitle = 'Variant Distributions'
    elif action == 'get_gv_tumor_dist':
        subtitle = 'Tumor Site Distribution of Variants'
    elif action == 'get_tumor_dist':
        table = '{query_dataset}TumorStats'.format(query_dataset=query_dataset)
        subtitle = 'Tumor Site Distribution of Variants'
    elif action == 'get_tumor_dist_view':
        table = 'GermlineView_Carriers' if query_dataset == 'Germline' else '{query_dataset}View'.format(query_dataset=query_dataset)
        subtitle = 'Tumor Site Distribution of Variants'
    elif action == 'get_codon_dist':
        table = 'GermlineMutationStats'
        subtitle = 'Codon Distribution of Point Variants'
    else:
        return render_template('error.html', error_message='Unable to generate the plot: <em>Search criteria is missing.</em><br/>Please revisit the search page and re-run the query.')

    if action == 'get_gv_tumor_dist':
        gv_tumor_dist_tables = {
            'somatic_tumor_dist': 'SomaticView',
            'germline_tumor_dist': 'GermlineView'
        }
        graph_configs = {}
        sql_maps = {}
        graph_configs[action] = graphs.build_graph_configs(action)['tumor_dist']
        for dist_table in gv_tumor_dist_tables:
            sql_maps[dist_table] = (
                graphs.build_graph_sqls(graph_configs, criteria_map=criteria_map,
                                        table=gv_tumor_dist_tables[dist_table])[
                    action])
    else:
        graph_configs = graphs.build_graph_configs(action, table)

        sql_maps = graphs.build_graph_sqls(graph_configs, criteria_map=criteria_map, table=table)
    graph_result = graphs.build_graph_data(bigquery_client, sql_maps)

    return render_template(template, criteria_map=criteria_map, title=title,
                           subtitle=subtitle,
                           graph_result=graph_result)


def login_is_required(function):
    # a function to check if the user is authorized or not
    def wrapper(*args, **kwargs):
        if "user" not in session:  # authorization required
            return abort(401)
        else:
            return function()

    return wrapper


@app.route("/gdc_cases_query", methods=['POST'])
@login_is_required
def gdc_query():
    parameters = dict(request.form)
    mut_id = json.loads(parameters['mut_id'])
    if mut_id:
        column_filters = ['CaseUUID', 'CaseID', 'Program', 'ProjectShortName', 'g_description_GRCh38', 'MUT_ID']
        criteria = [{'column_name': 'MUT_ID', 'vals': [mut_id]}]
        table = 'Mutation_GDC'
        sql_stm = bq_builder.build_simple_query(criteria=criteria, table=table, column_filters=column_filters)
        result = run_bq_sql(sql_stm)
        result_list = [dict(row) for row in result]
        return jsonify({ "data": result_list })
    else:
        return abort(404)


@app.route("/mutation_query", methods=['GET', 'POST'])
def mutation_query():
    parameters = dict(request.form)
    draw = parameters['draw']
    order_col = int(parameters['order[0][column]'])
    order_dir = parameters['order[0][dir]']
    start = int(parameters['start'])
    length = int(parameters['length'])
    criteria_map = json.loads(parameters['criteria'])
    if len(criteria_map) == 0:
        criteria_map = {
            'include': [],
            'exclude': []
        }
    query_dataset = parameters['query_dataset']
    table = '{query_dataset}View'.format(query_dataset=query_dataset)
    distinct_col = '{query_dataset}View_ID'.format(query_dataset=query_dataset)
    if query_dataset == 'Somatic':
        column_filters = [
            "g_description",
            "g_description_GRCh38",
            "c_description",
            "ProtDescription",
            "hg19_Chr17_coordinates",
            "hg38_Chr17_coordinates",
            "Codon_number",
            "COSMIClink",
            "CLINVARlink",
            "TCGA_ICGC_GENIE_count",
            "cBioportalCount",
            "WT_codon",
            "Mutant_codon",
            "TransactivationClass",
            "DNEclass",
            "Hotspot",
            "Topography",
            "Morphology",
            "Sex",
            "Age",
            "Germline_mutation",
            "PubMed",
            "SpliceAI_DS_AG",
            "SpliceAI_DS_AL",
            "SpliceAI_DS_DG",
            "SpliceAI_DS_DL",
            "SpliceAI_DP_AG",
            "SpliceAI_DP_AL",
            "SpliceAI_DP_DG",
            "SpliceAI_DP_DL"
            ]
    elif query_dataset == 'Germline':
        column_filters = [
            "g_description",
            "g_description_GRCh38",
            "c_description",
            "ProtDescription",
            "hg19_Chr17_coordinates",
            "hg38_Chr17_coordinates",
            "Class",
            "Country",
            "WT_codon",
            "Mutant_codon",
            "TransactivationClass",
            "DNE_LOFclass",
            "CLINVARlink",
            "Hotspot",
            "Individual_code",
            "Sex",
            "Age_at_diagnosis",
            "Topography",
            "Morphology",
            "PubMed",
            "SpliceAI_DS_AG",
            "SpliceAI_DS_AL",
            "SpliceAI_DS_DG",
            "SpliceAI_DS_DL",
            "SpliceAI_DP_AG",
            "SpliceAI_DP_AL",
            "SpliceAI_DP_DG",
            "SpliceAI_DP_DL"
        ]
            # "Ref_ID"]
    elif query_dataset == 'Prevalence':
        if 'include' not in criteria_map:
            criteria_map = {
                'include': criteria_map,
                'exclude': []
            }
        distinct_col = 'Prevalence_ID'
        column_filters = [
            "Topography",
            "Short_topo",
            "Topo_code",
            "Morphology",
            "Morpho_code",
            "Sample_analyzed",
            "Sample_mutated",
            "Prevalence",
            "Country",
            "Region",
            "Comment",
            "PubMed",
            "Tissue_processing",
            "Start_material",
            "Prescreening",
            "exon2",
            "exon3",
            "exon4",
            "exon5",
            "exon6",
            "exon7",
            "exon8",
            "exon9",
            "exon10",
            "exon11"
        ]
    else:
        return abort(404)

    sql_stm = bq_builder.build_query_w_exclusion(criteria_map=criteria_map, table=table,
                                            ord_column_list=[column_filters[order_col-1], distinct_col], desc_ord=(order_dir == 'desc'),
                                            start=start, length=length)
    sql_cnt_stm = bq_builder.build_query_w_exclusion(criteria_map=criteria_map, table=table,
                                                do_counts=True, distinc_col=distinct_col)
    data = get_paginated_results(sql_stm, sql_cnt_stm)
    data['draw'] = draw
    return jsonify(data)



def get_paginated_results(sql_stm, sql_cnt_stm):
    page_result = run_bq_sql(sql_stm)
    count_result = run_bq_sql(sql_cnt_stm)
    page_result_list = [dict(row) for row in page_result]
    recordsTotal = list(count_result)[0].CNT
    return {
        "recordsTotal": recordsTotal,
        "recordsFiltered": recordsTotal,
        "data": page_result_list
    }


def run_bq_sql(sql_stm):
    query_job = bigquery_client.query(sql_stm)
    # error_msg = None

    try:
        query_result = query_job.result(timeout=30)
        return query_result
    except (concurrent.futures.TimeoutError, requests.exceptions.ReadTimeout):
        error_msg = "Sorry, query job has timed out."
        raise error_msg
    except (BadRequest, Exception):
        error_msg = "There was a problem while running the BigQuery job"
        raise error_msg


@app.route("/<prefix>_query", methods=['GET', 'POST'])
def simple_query(prefix):
    parameters = dict(request.form)
    draw = parameters['draw']
    order_col = int(parameters['order[0][column]'])
    order_dir = parameters['order[0][dir]']
    start = int(parameters['start'])
    length = int(parameters['length'])
    criteria = json.loads(parameters['criteria'])
    if prefix == 'gv':
        # table = 'MutationView'
        table = 'MutationView_gdc'
        distinct_col = 'MUT_ID'
        column_filters = ["MUT_ID", "g_description", "g_description_GRCh38", "c_description", "ProtDescription", "ExonIntron", "Effect",
                      "TransactivationClass", "DNE_LOFclass", "AGVGDClass", "Somatic_count", "Germline_count", "Cellline_count",
                      "TCGA_ICGC_GENIE_count", "GDC_case_count", "Polymorphism", "CLINVARlink", "COSMIClink", "SNPlink", "gnomADlink",
                          "SpliceAI_DS_AG", "SpliceAI_DS_AL", "SpliceAI_DS_DG",	"SpliceAI_DS_DL",
                          "SpliceAI_DP_AG", "SpliceAI_DP_AL", "SpliceAI_DP_DG", "SpliceAI_DP_DL"]
        order_col_name = column_filters[order_col-1]
    elif prefix == 'cl':
        table = 'CellLineView'
        distinct_col = 'CellLineView_ID'
        column_filters = ["CellLineView_ID", "Sample_Name", "Short_topo", "Morphology", "ATCC_ID", "Cosmic_ID",
                          "depmap_ID", "Sex", "Age", "TP53status", "ExonIntron", "c_description", "ProtDescription", "Pubmed"]
        order_col_name = column_filters[order_col]
    else:
        return abort(404)
    sql_stm = bq_builder.build_simple_query(criteria=criteria, table=table, column_filters=column_filters,
                                            distinct_col=distinct_col, ord_column=order_col_name, desc_ord=(order_dir == 'desc'),
                                            start=start, length=length)
    sql_cnt_stm = bq_builder.build_simple_query(criteria=criteria, table=table, column_filters=column_filters,
                                                do_counts=True, distinct_col=distinct_col)
    data = get_paginated_results(sql_stm, sql_cnt_stm)
    data['draw'] = draw
    return jsonify(data)


@app.route("/mut_details", methods=['GET'])
def mut_details():
    mut_id = filters.get_param_val('mut_id')

    simple_queries = {
        'mutation': {
            'column_filters': ['*'],
            'criteria': [{'column_name': 'MUT_ID', 'vals': [mut_id]}],
            'table': 'MutationView',
            'ord_column': 'MUT_ID'
        },
        'splice_pred': {
            'column_filters': ['Splice_Site_Type', 'p53SpliceSite', 'WT_score', 'Mutant_score', 'Variation',
                               'Source', 'MUT_ID'],
            'criteria': [{'column_name': 'MUT_ID', 'vals': [mut_id]}],
            'table': 'SPLICING_PREDICTION_VIEW',
            'ord_column': 'MUT_ID'
        },

        'p53_pred': {
            'column_filters': ['TAp53', 'TAp53beta', 'TAp53gamma', 'delta40p53', 'delta40p53beta', 'delta40p53gamma',
                               'delta133p53', 'delta133p53beta', 'delta133p53gamma', 'deltap53', 'MUT_ID'],
            'criteria': [{'column_name': 'MUT_ID', 'vals': [mut_id]}],
            'table': 'ISOFORMS_STATUS',
            'ord_column': 'MUT_ID'
        },
        'gdc_cases': {
            'column_filters': ['CaseUUID'],
            'criteria': [{'column_name': 'MUT_ID', 'vals': [mut_id]}],
            'table': 'Mutation_GDC',
            'ord_column': 'CaseUUID'
        }
    }
    join_queries = {
        'vars_act': {
            'mut_id': mut_id,
            'column_filters': ['Loss_of_Function', 'Conserved_WT_Function', 'Gain_of_Function',
                               'Dominant_Negative_Activity', 'Temperature_Sensitivity', 'Cell_lines', 'PubMed',
                               'AAchange_ID'],
            'table': 'FunctionView',
            'join_column': 'AAchange_ID',
            'ord_column': 'AAchange_ID'
        },
        'mouse': {
            'mut_id': mut_id,
            'column_filters': ['ModelDescription', 'TumorSites', 'caMOD_ID', 'PubMed', 'AAchange_ID'],
            'table': 'MouseModelView',
            'join_column': 'AAchange_ID',
            'ord_column': 'AAchange_ID'
        },
        'induced': {
            'mut_id': mut_id,
            'column_filters': ['Exposure', 'Model', 'PubMed', 'MUT_ID'],
            'table': 'InducedMutationView',
            'join_column': 'MUT_ID',
            'ord_column': 'MUT_ID'
        }
    }

    sql_stms = {}
    for t_id in simple_queries:
        sql_stms[t_id] = bq_builder.build_simple_query(criteria=simple_queries[t_id]['criteria'],
                                                       table=simple_queries[t_id]['table'],
                                                       column_filters=simple_queries[t_id]['column_filters'],
                                                       ord_column=simple_queries[t_id]['ord_column'])
    for t_id in join_queries:
        sql_stms[t_id] = bq_builder.build_mutation_view_join_query(mut_id=join_queries[t_id]['mut_id'],
                                                                   join_table=join_queries[t_id]['table'],
                                                                   column_filters=join_queries[t_id]['column_filters'],
                                                                   join_column=join_queries[t_id]['join_column'],
                                                                   ord_column=join_queries[t_id]['ord_column'])

    error_msg = None
    query_result = {}
    sys_assess = {}
    prot_desc = {}
    prot_pred = {}
    tsv_data = None
    try:
        query_job = bigquery_client.query(sql_stms['mutation'])
        query_result['mutation'] = list(query_job.result(timeout=30))
        del sql_stms['mutation']
        if query_result['mutation'] and query_result['mutation'][0]:
            mut_desc = query_result['mutation'][0]
            tsv_data = "data:text/tab-separated-values;charset=utf-8,"
            tsv_data += "\t".join(f'{k}' for k in list(mut_desc.keys()))
            tsv_data += "\n"
            tsv_data += "\t".join(f'{k}' for k in list(mut_desc.values()))
            if mut_desc['ProtDescription']:
                if mut_desc['ProtDescription'] == 'p.?':
                    del sql_stms['splice_pred']
                    del sql_stms['p53_pred']
                    del sql_stms['vars_act']
                    del sql_stms['mouse']
                else:
                    if mut_desc['WAF1nWT'] is not None:
                        sys_assess = {
                            'WAF1nWT': mut_desc['WAF1nWT'],
                            'MDM2nWT': mut_desc['MDM2nWT'],
                            'BAXnWT': mut_desc['BAXnWT'],
                            'h1433snWT': mut_desc['h1433snWT'],
                            'AIP1nWT': mut_desc['AIP1nWT'],
                            'GADD45nWT': mut_desc['GADD45nWT'],
                            'NOXAnWT': mut_desc['NOXAnWT'],
                            'P53R2nWT': mut_desc['P53R2nWT'],
                            'WAF1nWT_Saos2': mut_desc['WAF1nWT_Saos2'],
                            'MDM2nWT_Saos2': mut_desc['MDM2nWT_Saos2'],
                            'BAXnWT_Saos2': mut_desc['BAXnWT_Saos2'],
                            'h1433snWT_Saos2': mut_desc['h1433snWT_Saos2'],
                            'AIP1nWT_Saos2': mut_desc['AIP1nWT_Saos2'],
                            'PUMAnWT_Saos2': mut_desc['PUMAnWT_Saos2'],
                            'MUT_ID': mut_desc['MUT_ID'],
                        }

                    if mut_desc['TransactivationClass'] != 'NA' or\
                        mut_desc['DNEclass'] != 'NA' or\
                        mut_desc['DNE_LOFclass'] != 'NA' or\
                        mut_desc['AGVGDClass'] != 'NA' or\
                        mut_desc['BayesDel'] or\
                        mut_desc['REVEL'] or\
                        mut_desc['SIFTClass'] != 'NA' or\
                        mut_desc['Polyphen2'] != 'NA' or\
                        mut_desc['StructureFunctionClass'] != 'NA':

                        prot_pred = {
                            'TransactivationClass': mut_desc['TransactivationClass'],
                            'DNEclass': mut_desc['DNEclass'],
                            'DNE_LOFclass': mut_desc['DNE_LOFclass'],
                            'AGVGDClass': mut_desc['AGVGDClass'],
                            'BayesDel': mut_desc['BayesDel'],
                            'REVEL': mut_desc['REVEL'],
                            'SIFTClass': mut_desc['SIFTClass'],
                            'Polyphen2': mut_desc['Polyphen2'],
                            'StructureFunctionClass': mut_desc['StructureFunctionClass'],
                            'MUT_ID': mut_desc['MUT_ID']
                        }
                    prot_desc = {
                        'Structural_motif': mut_desc['Structural_motif'],
                        'Domain_function': mut_desc['Domain_function'],
                        'Residue_function': mut_desc['Residue_function'],
                        'Hotspot': mut_desc['Hotspot'],
                        'Mut_rate': mut_desc['Mut_rate'],
                        'SwissProtLink': mut_desc['SwissProtLink'],
                        'MUT_ID': mut_desc['MUT_ID']
                    }
        for t_id in sql_stms:
            query_job = bigquery_client.query(sql_stms[t_id])
            query_result[t_id] = list(query_job.result(timeout=30))
    except BadRequest:
        error_msg = "There was a problem while running the query: BadRequest"
    except (concurrent.futures.TimeoutError, requests.exceptions.ReadTimeout):
        error_msg = "Sorry, query job has timed out."

    return render_template("mut_details.html",
                           mut_id=mut_id,
                           query_result=query_result,
                           mut_desc=mut_desc,
                           sys_assess=sys_assess,
                           prot_desc=prot_desc,
                           prot_pred=prot_pred,
                           tsv_data=tsv_data,
                           error_msg=error_msg)


@app.route("/search_somatic_mut")
def search_somatic_mut():
    return render_template("search_somatic_mut.html",
                           cl_start_material_list=settings.sm_start_material_list,
                           country_list=settings.country_list,
                           c_desc_list=settings.sm_c_desc_list,
                           p_desc_list=settings.sm_p_desc_list,
                           g_desc_hg19_list=settings.sm_g_desc_hg19_list,
                           g_desc_hg38_list=settings.sm_g_desc_hg38_list,
                           type_list=settings.sm_type_list,
                           desc_list=settings.sm_desc_list,
                           motif_list=settings.sm_motif_list,
                           exon_intron_list=settings.sm_exon_intron_list,
                           effect_list=settings.sm_effect_list,
                           ta_class_list=settings.sm_ta_class_list,
                           sift_list=settings.sm_sift_list,
                           topo_list=settings.topo_list,
                           morph_list=settings.morph_list,
                           topo_morph_assc=settings.topo_morph_assc,
                           tumor_org_group_list=settings.sm_tumor_org_group_list,
                           sample_source_list=settings.sm_sample_source_list,
                           germ_mut_list=settings.sm_germ_mut_list,
                           tobacco_list=settings.sm_tobacco_list,
                           inf_agnt_list=settings.sm_inf_agnt_list,
                           exposure_list=settings.sm_exposure_list,
                           ref_data=settings.sm_ref_data
                           )


@app.route("/search_somatic_prevalence")
def search_somatic_prevalence():
    return render_template("search_somatic_prevalence.html",
                           morph_list=settings.morph_list,
                           topo_list=settings.topo_list,
                           topo_morph_assc=settings.topo_morph_assc,
                           cl_start_material_list=settings.sm_start_material_list,
                           country_list=settings.country_list
                           )


@app.route("/prevalence_somatic_stats")
def prevalence_somatic_stats():
    sql_stm = bq_builder.build_mutation_prevalence()
    result = run_bq_sql(sql_stm)
    labels = []
    data = []
    total_cnt = 0
    for row in list(result):
        topo = row.get('Topography')
        anal_cnt = row.get('Sample_analyzed')
        mut_cnt = row.get('Sample_mutated')
        label = "{topo} ({mut_cnt}/{anal_cnt})".format(topo=topo, anal_cnt=anal_cnt, mut_cnt=mut_cnt)
        labels.append(label)
        ratio = mut_cnt * 100 / anal_cnt
        data.append(ratio)
        total_cnt += mut_cnt
    graph_data = {
        'chart_type': 'ratio',
        'labels': labels,
        'data': data,
        'total': total_cnt
    }
    return render_template("prevalence_somatic_stats.html", criteria=[], graph_data=graph_data, title='Statistics on Tumor Variants', subtitle='Tumor Variant Prevalence by Tumor Site')


@app.route("/results_somatic_mutation_list", methods=['GET', 'POST'])
def results_somatic_mutation_list():
    criteria_map = {}
    if request.method == 'POST':
        criteria_type = ['include', 'exclude']
        for type in criteria_type:
            prefix = 'sm_{type}'.format(type=type)
            criteria_map[type] = filters.get_ref_criteria(prefix)
            criteria_map[type] += filters.get_method_criteria(prefix)
            criteria_map[type] += filters.get_ngs_criteria(prefix)
            criteria_map[type] += filters.get_gene_variant_criteria(prefix)
            criteria_map[type] += filters.get_variant_feature_criteria(prefix)
            criteria_map[type] += filters.get_topo_morph_criteria(prefix)
            criteria_map[type] += filters.get_tumor_origin_criteria(prefix)
            criteria_map[type] += filters.get_patient_criteria(prefix)
            criteria_map[type] += filters.get_country_criteria(prefix)
            criteria_map[type] += filters.get_sample_source_criteria(prefix)

    return render_template("results_somatic_mutation.html", criteria_map=criteria_map)


@app.route("/download_dataset", methods=['GET', 'POST'])
def download_dataset():
    filename = filters.get_param_val('filename')
    criteria_param = filters.get_param_val('criteria_map')
    criteria_map = {}
    if criteria_param:
        criteria_map = json.loads(criteria_param)

    query_datatable=filters.get_param_val('query_datatable')
    if not len(criteria_map.get('exclude', [])):
        sql_stm = bq_builder.build_simple_query(criteria=criteria_map.get('include', []), table=query_datatable, column_filters=['*'])
    else:
        sql_stm = bq_builder.build_query_w_exclusion(criteria_map=criteria_map, table=query_datatable, column_filters=['*'])

    query_job = bigquery_client.query(sql_stm)
    error_msg = None
    query_result=[]
    table_header = []
    try:
        result = query_job.result(timeout=30)
        query_result = list(result)
        table_header = [sf.name for sf in result.schema]
    except BadRequest:
        error_msg = "There was a problem with your search input. Please revise your search criteria and search again."
    except (concurrent.futures.TimeoutError, requests.exceptions.ReadTimeout):
        error_msg = "Sorry, query job has timed out."
    # query_result = {'data': data, 'msg': error_msg}
    filename_full='{filename}{version}.csv'.format(filename=filename, version=('_'+settings.DATA_VERSION if settings.DATA_VERSION else ''))
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(table_header)
    cw.writerows(query_result)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename={filename_full}".format(filename_full=filename_full)
    output.headers["Content-type"] = "text/csv"
    return output


@app.route("/results_somatic_prevalence_list", methods=['GET','POST'])
def results_somatic_prevalence_list():
    prefix = 'mut_prev'
    criteria = filters.get_topo_morph_criteria(prefix)
    criteria += filters.get_method_criteria(prefix)
    criteria += filters.get_ngs_criteria(prefix)
    criteria += filters.get_country_criteria(prefix)

    return render_template("results_somatic_prevalence.html", criteria=criteria)


@app.route("/get_prevalence_distribution", methods=['GET', 'POST'])
def get_prevalence_distribution():
    criteria = []
    action = filters.get_param_val('action')
    if request.method == 'POST':
        criteria = filters.get_param_val('criteria')
        if criteria:
            criteria = json.loads(filters.get_param_val('criteria'))
        title = 'Search Results'
    if action == 'get_country_graph':
        group_by = 'Country'
        subtitle = 'Tumor Variant Prevalence by Country'
    elif action == 'get_topo_graph':
        group_by = 'Short_topo'
        subtitle = 'Tumor Variant Prevalence by Topography'
    else:
        # get_morph_graph
        group_by = 'Morphogroup'
        subtitle = 'Tumor Variant Prevalence by Morphology'
    sql_stm = bq_builder.build_group_sum_graph_query(criteria=criteria, view='PrevalenceView', group_by=group_by)

    query_job = bigquery_client.query(sql_stm)
    data = []
    # error_msg = None
    try:
        result = query_job.result(timeout=30)
        rows = list(result)
        labels = []
        total_cnt = 0
        for row in rows:
            label = row.get('LABEL')
            anal_cnt = row.get('Sample_analyzed_SUM')
            mut_cnt = row.get('Sample_mutated_SUM')
            label = "{label} ({mut_cnt}/{anal_cnt})".format(label=label, anal_cnt=anal_cnt, mut_cnt=mut_cnt)
            labels.append(label)
            ratio = mut_cnt * 100 / anal_cnt
            data.append(ratio)
            total_cnt += mut_cnt
        graph_data = {
            'chart_type': 'ratio',
            'labels': labels,
            'data': data,
            'total': total_cnt
        }
    except BadRequest:
        error_msg = "There was a problem with your search input. Please revise your search criteria and search again."
    except (concurrent.futures.TimeoutError, requests.exceptions.ReadTimeout):
        error_msg = "Sorry, query job has timed out."
    return render_template("prevalence_somatic_stats.html", graph_data=graph_data, criteria=criteria, title=title, subtitle=subtitle)


@app.route("/search_germline_mut")
def search_germline_mut():
    return render_template("search_germline_mut.html",
                           topo_list=settings.topo_list,
                           morph_list=settings.morph_list,
                           topo_morph_assc=settings.topo_morph_assc,
                           c_desc_list=settings.gm_c_desc_list,
                           p_desc_list=settings.gm_p_desc_list,
                           g_desc_hg19_list=settings.gm_g_desc_hg19_list,
                           g_desc_hg38_list=settings.gm_g_desc_hg38_list,
                           type_list=settings.gm_type_list,
                           desc_list=settings.gm_desc_list,
                           motif_list=settings.gm_motif_list,
                           exon_intron_list=settings.gm_exon_intron_list,
                           effect_list=settings.gm_effect_list,
                           ta_class_list=settings.gm_ta_class_list,
                           sift_list=settings.gm_sift_list,
                           family_hist_list=settings.gm_family_hist_list,
                           inh_mode_list=settings.gm_inh_mode_list,
                           family_case_list=settings.gm_family_case_list,
                           country_list=settings.country_list,
                           ref_data=settings.gm_ref_data
                           )


@app.route("/view_germline_prevalence")
def view_germline_prevalence():
    column_filters = ['Diagnosis', 'Cohort', 'Cases_Analyzed', 'Cases_mutated', 'Mutation_prevalence', 'Remark',
                      'PubMed']
    criteria = []
    sql_stm = bq_builder.build_simple_query(criteria=criteria, table='GermlinePrevalenceView',
                                            column_filters=column_filters)
    query_job = bigquery_client.query(sql_stm)
    data = []
    error_msg = None
    try:
        result = query_job.result(timeout=30)
        data = list(result)
    except BadRequest:
        error_msg = "There was a problem with your search input. Please revise your search criteria and search again."
    except (concurrent.futures.TimeoutError, requests.exceptions.ReadTimeout):
        error_msg = "Sorry, query job has timed out."
    query_result = {'data': data, 'msg': error_msg}

    return render_template("view_germline_prevalence.html", criteria=criteria, query_result=query_result)


@app.route("/results_germline_mutation_list", methods=['GET', 'POST'])
def results_germline_mutation_list():
    criteria_map = {}
    if request.method == 'POST':
        criteria_type = ['include', 'exclude']
        for type in criteria_type:
            prefix = 'gm_{type}'.format(type=type)
            criteria_map[type] = filters.get_ref_criteria(prefix)
            criteria_map[type] += filters.get_topo_morph_criteria(prefix)
            criteria_map[type] += filters.get_gene_variant_criteria(prefix)
            criteria_map[type] += filters.get_variant_feature_criteria(prefix)
            criteria_map[type] += filters.get_germline_patient_criteria(prefix)
            criteria_map[type] += filters.get_country_criteria(prefix)
    return render_template("results_germline_mutation.html", criteria_map=criteria_map)


@app.route("/view_<dataset>")
def view_full_data(dataset):
    criteria = []
    if dataset == 'exp_ind_mut':
        column_filters = ['Exposure', 'g_description_GRCh38', 'c_description', 'ProtDescription', 'Model', 'Clone_ID',
                          'Add_Info', 'PubMed', 'MUT_ID', 'Induced_ID']
        table = 'InducedMutationView'
    elif dataset == 'mouse':
        column_filters = ['ModelDescription', 'TumorSites', 'AAchange', 'caMOD_ID', 'PubMed', 'MM_ID']
        table = 'MouseModelView'
    elif dataset == 'val_poly':
        column_filters = ['g_description_GRCh38', 'c_description', 'ProtDescription', 'ExonIntron', 'Effect',
                          'SNPlink', 'gnomADlink', 'CLINVARlink', 'PubMedlink', 'SourceDatabases']
        table = 'MutationView'
        criteria = [{'column_name': 'polymorphism', 'vals': ['validated'], 'wrap_with': '"'}]

    sql_stm = bq_builder.build_simple_query(criteria=criteria, table=table,
                                            column_filters=column_filters)
    query_job = bigquery_client.query(sql_stm)
    data = []
    error_msg = None
    try:
        result = query_job.result(timeout=30)
        data = list(result)
    except BadRequest:
        error_msg = "There was a problem with your search input. Please revise your search criteria and search again."
    except (concurrent.futures.TimeoutError, requests.exceptions.ReadTimeout):
        error_msg = "Sorry, query job has timed out."
    query_result = {'data': data, 'msg': error_msg}

    return render_template("view_{dataset}.html".format(dataset=dataset), criteria=criteria, query_result=query_result)



@app.route("/view_data", methods = ['GET'])
def view_data():
    bq_view_name = request.args.get('bq_view_name', None)
    title = TITLE_BQVIEW_MAP[bq_view_name]
    columns, data = utils.load_csv_file(settings.TP53_STATIC_URL, '{filename}_{version}.csv'.format(filename=bq_view_name, version=settings.DATA_VERSION))
    return render_template("view_data.html", title=title,  bq_view_name=bq_view_name, ver=settings.DATA_VERSION, columns=columns, data=data)


##
# cell lines search
##

@app.route("/search_cell_lines")
def search_cell_lines():
    return render_template("search_cell_lines.html",
                           c_desc_list=settings.cl_c_desc_list,
                           p_desc_list=settings.cl_p_desc_list,
                           g_desc_hg19_list=settings.cl_g_desc_hg19_list,
                           g_desc_hg38_list=settings.cl_g_desc_hg38_list,
                           cl_tp53stat_list=settings.cl_tp53stat_list,
                           topo_list=settings.topo_list,
                           morph_list=settings.morph_list,
                           topo_morph_assc=settings.topo_morph_assc,
                           tumor_org_group_list=settings.cl_tumor_org_group_list,
                           cl_start_material_list=settings.cl_start_material_list,
                           desc_list=settings.cl_desc_list,
                           effect_list=settings.cl_effect_list,
                           motif_list=settings.cl_motif_list,
                           type_list=settings.cl_type_list,
                           sift_list=settings.cl_sift_list,
                           exon_intron_list=settings.cl_exon_intron_list,
                           ta_class_list=settings.cl_ta_class_list,
                           germ_mut_list=settings.cl_germ_mut_list,
                           tobacco_list=settings.cl_tobacco_list,
                           inf_agnt_list=settings.cl_inf_agnt_list,
                           country_list=settings.country_list,
                           exposure_list=settings.cl_exposure_list
                           )


@app.route("/cell_lines_mutation_stats", methods=['GET', 'POST'])
def cell_lines_mutation_stats():
    action = filters.get_param_val('action')
    if action == 'get_mutation_type':
        table = 'CellLineView'
        subtitle='Type of Variants'
    elif action == 'get_tumor_dist':
        table = 'CellLineSiteStats'
        subtitle = 'Tumor Site Distribution of Variants'
    else: # action == 'get_codon_dist'
        table = 'CellLineMutationStats'
        subtitle = 'Codon Distribution of Point Variants'
    graph_configs = graphs.build_graph_configs(action, table)
    sql_maps = graphs.build_graph_sqls(graph_configs, {}, table)
    graph_result = graphs.build_graph_data(bigquery_client, sql_maps)
    return render_template("mutation_stats.html", criteria_map={}, title='Statistics on Cell Line Variants',
                           subtitle=subtitle,
                           graph_result=graph_result)


@app.route("/results_cell_line_mutation", methods=['GET', 'POST'])
def results_cell_line_mutation():
    criteria = []
    if request.method == 'POST':
        mut_id_criteria = filters.get_mut_id_criteria()
        if (len(mut_id_criteria)):
            criteria = mut_id_criteria
        else:
            prefix = 'cl'
            criteria += filters.get_cell_line_criteria(prefix)
            criteria += filters.get_method_criteria(prefix)
            criteria += filters.get_gene_variant_criteria(prefix)
            criteria += filters.get_variant_feature_criteria(prefix)
            criteria += filters.get_patient_criteria(prefix)
            criteria += filters.get_country_criteria(prefix)
            criteria += filters.get_mut_id_criteria()
    return render_template("results_cell_lines.html", criteria=criteria)


@app.route("/get_tp53data")
def get_tp53data():
    return render_template("get_tp53data.html", TP53_DATA_DIR_URL='{static_dir}/data'.format(static_dir=settings.TP53_STATIC_URL), ver=settings.DATA_VERSION)

#
# Events Page
#
@app.route("/events")
def events():
    upcoming_list = settings.event_list['upcoming_list']
    past_list = settings.event_list['past_list']

    print(upcoming_list)
    return render_template("events.html", upcoming_list=upcoming_list, past_list=past_list)

# single page rendering
@app.route('/', defaults={'page': 'home'})
@app.route('/<page>')
def show(page):
    try:
        return render_template('{page}.html'.format(page=page))
    except TemplateNotFound:
        abort(404)


# return sitemap file (urllist.txt or sitemap.xml)
@app.route('/<txt_url>.txt')
@app.route('/<xml_url>.xml')
@app.route('/<google_site_ver>.html')
def get_sitemap_file(txt_url=None, xml_url=None, google_site_ver=None):
    url_list_filename = None
    if txt_url and txt_url.lower() == 'urllist':
        url_list_filename = os.environ.get('SITEMAP_LIST_FILE', 'urllist.txt')
    elif xml_url and xml_url.lower() == 'sitemap':
        url_list_filename = os.environ.get('SITEMAP_XML_FILE', 'sitemap.xml')
    elif google_site_ver and google_site_ver.index('google')==0:
        return send_from_directory(app.root_path, 'templates/{filename}.html'.format(filename=google_site_ver))

    if url_list_filename:
        return send_from_directory(app.root_path, url_list_filename)
    else:
        return abort(404)


# view pdf files
@app.route('/pdf/<filename>') #the url you'll send the user to when he wants the pdf
def pdf_viewer(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/download'),
                               filename+'.pdf')


@app.route("/cse_search")
def cse_search():
    return render_template("cse_search.html", google_se_id=settings.GOOGLE_SE_ID)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/_ah/warmup')
def warmup():
    # Handle your warmup logic here, e.g. set up a database connection pool
    return '', 200, {}

#
# Log-in methods


@app.route("/login", methods=['GET','POST'])
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    session["request_referrer"] = request.referrer
    return redirect(authorization_url)


@app.route("/callback")
# Page after the authorization
def callback():
    flow.fetch_token(authorization_response=request.url)
    if not session["state"] == request.args["state"]:
        abort(500)  # state does not match!
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials.id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID,
        clock_skew_in_seconds=5
    )
    user = {
        'email': id_info.get("email"),
        'name': id_info.get("name"),
        'picture': id_info.get("picture")
    }
    session["user"] = user  # defining the results to show on the page
    request_referrer = session["request_referrer"]
    session.pop('request_referrer')
    logging.info('User {userid} has acknowledged the data agreement has logged in '.format(userid=user['email']))
    return redirect(request_referrer)  # the final page where the authorized users will end up


@app.route("/logout", methods=['GET', 'POST'])  # the logout page and function
def logout():
    session.clear()
    return redirect('/home')


settings.setup_app(app)
app.secret_key = settings.SECRET_KEY


if __name__ == '__main__':
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    # print("running locally")
    app.run(host='127.0.0.1', port=8080, debug=True)
