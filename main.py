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
import os
from flask import Flask, render_template, request, send_from_directory, json, jsonify
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
# from flask_talisman import Talisman
import bq_builder
import concurrent.futures
import requests
# import datetime
import sys

# import json
TP53_STATIC_URL = os.environ.get('TP53_STATIC_URL', 'https://storage.googleapis.com/tp53-static-files-dev')
M_C_DESC_FILE = 'M_C_DESC.TXT.LIST'
M_P_DESC_FILE = 'M_P_DESC.TXT.LIST'
M_G_DESC_HG19_FILE = 'M_G_DESC_HG19.TXT.LIST'
M_G_DESC_HG38_FILE = 'M_G_DESC_HG38.TXT.LIST'
M_TYPE_FILE = 'M_TYPE.TXT.LIST'
M_DESC_FILE = 'M_DESC.TXT.LIST'
M_MOTIF_FILE = 'M_MOTIF.TXT.LIST'
M_EXON_INTRON_FILE = 'M_EXON_INTRON.TXT.LIST'
M_EFFECT_FILE = 'M_EFFECT.TXT.LIST'
M_TA_CLASS_FILE = 'M_TA_CLASS.TXT.LIST'
M_SIFT_FILE = 'M_SIFT.TXT.LIST'

CL_C_DESC_FILE = 'CL_C_DESC.TXT.LIST'
CL_P_DESC_FILE = 'CL_P_DESC.TXT.LIST'
CL_G_DESC_HG19_FILE = 'CL_G_DESC_HG19.TXT.LIST'
CL_G_DESC_HG38_FILE = 'CL_G_DESC_HG38.TXT.LIST'
CL_TOPO_FILE = 'CL_TOPO.TXT.LIST'
CL_MORPH_FILE = 'CL_MORPH.TXT.LIST'
CL_TUMOR_ORG_GROUP_FILE = 'CL_TUMOR_ORG_GROUP.TXT.LIST'
CL_TP53STAT_FILE = 'CL_TP53STAT.TXT.LIST'
CL_DESC_FILE = 'CL_DESC.TXT.LIST'
CL_EFFECT_FILE = 'CL_EFFECT.TXT.LIST'
CL_MOTIF_FILE = 'CL_MOTIF.TXT.LIST'
CL_START_MATERIAL_FILE = 'CL_START_MATERIAL.TXT.LIST'
CL_TA_CLASS_FILE = 'CL_TA_CLASS.TXT.LIST'
CL_TYPE_FILE = 'CL_TYPE.TXT.LIST'
CL_SIFT_FILE = 'CL_SIFT.TXT.LIST'
CL_EXON_INTRON_FILE = 'CL_EXON_INTRON.TXT.LIST'

CL_GERM_MUT_FILE = 'CL_GERM_MUT.TXT.LIST'
CL_INF_AGNT_FILE = 'CL_INF_AGNT.TXT.LIST'
CL_EXPOSURE_FILE = 'CL_EXPOSURE.TXT.LIST'
COUNTRY_FILE = 'COUNTRY.TXT.LIST'

app = Flask(__name__)

global m_c_desc_list
m_c_desc_list = None

global m_p_desc_list
m_p_desc_list = None

global m_g_desc_hg19_list
m_g_desc_hg19_list = None

global m_g_desc_hg38_list
m_g_desc_hg38_list = None

global m_type_list
m_type_list = None

global m_desc_list
m_desc_list = None

global m_motif_list
m_motif_list = None

global m_exon_intron_list
m_exon_intron_list = None

global m_effect_list
m_effect_list = None

global m_ta_class_list
m_ta_class_list = None

global m_sift_list
m_sift_list = None

global cl_c_desc_list
cl_c_desc_list = None

global cl_p_desc_list
cl_p_desc_list = None

global cl_g_desc_hg19_list
cl_g_desc_hg19_list = None

global cl_g_desc_hg38_list
cl_g_desc_hg38_list = None

global cl_topo_list
cl_topo_list = None

global cl_morph_list
cl_morph_list = None

global cl_tumor_org_group_list
cl_tumor_org_group_list = None

global cl_tp53stat_list
cl_tp53stat_list = None

global cl_desc_list
cl_desc_list = None

global cl_effect_list
cl_effect_list = None

global cl_motif_list
cl_motif_list = None

global cl_start_material_list
cl_start_material_list = None

global cl_ta_class_list
cl_ta_class_list = None

global cl_type_list
cl_type_list = None

global cl_sift_list
cl_sift_list = None

global cl_exon_intron_list
cl_exon_intron_list = None

global cl_inf_agnt_list
cl_inf_agnt_list = None

global cl_germ_mut_list
cl_germ_mut_list = None

global country_list
country_list = None

global cl_exposure_list
cl_exposure_list = None


IS_TEST = True
BQ_DATASET = 'P53_data'

# hsts_max_age = 3600 if IS_TEST else 31536000
#
# Talisman(app, strict_transport_security_max_age=hsts_max_age, content_security_policy={
#     'default-src': [
#         '\'self\'',
#         '*.googletagmanager.com',
#         '*.google-analytics.com',
#         '*.googleapis.com',
#         "*.fontawesome.com",
#         '\'unsafe-inline\'',
#         'data:'
#     ]
# })

#
# MAX_RESULT_SIZE=50000
GOOGLE_APPLICATION_CREDENTIALS = os.path.join(app.root_path, 'tp53devBQ.key.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

project_id = os.environ.get('DEPLOYMENT_PROJECT_ID', 'isb-cgc-tp53-dev')
bq_builder.set_project_dataset(proj_id=project_id, d_set=BQ_DATASET)

bigquery_client = bigquery.Client()


@app.route("/")
def home():
    return render_template("home.html")

def get_param_val(request, input_name):
    if request.method == 'POST':
        method_request = request.form
    else:
        method_request = request.args

    return method_request.get(input_name)


def list_param_val(request, input_name):
    if request.method == 'POST':
        method_request = request.form
    else:
        method_request = request.args
    return method_request.getlist(input_name)


@app.route("/gv_result", methods=['GET', 'POST'])
def gv_result():
    result_title = 'Gene Variations'
    criteria = []
    column_name = None
    variations = None

    type_input = get_param_val(request, 'type_input')
    if type_input == 'type_cdna':
        column_name = 'c_description'
        variations = list_param_val(request, 'cdna_list')
    elif type_input == 'type_p':
        column_name = 'ProtDescription'
        variations = list_param_val(request, 'p_list')
    elif type_input == 'type_hg19':
        column_name = 'g_description'
        variations = list_param_val(request, 'hg19_list')
    elif type_input == 'type_hg38':
        column_name = 'g_description_GRCh38'
        variations = list_param_val(request, 'hg38_list')

    if column_name and variations and len(variations):
        criteria.append({'column_name': column_name, 'vals': variations, 'wrap_with': '"'})
    return render_template("gv_result.html", criteria=criteria, result_title=result_title)


@app.route("/gmut_result", methods=['GET', 'POST'])
def gmut_result():

    result_title = 'Gene Variations'
    criteria = []
    chrpos_type = get_param_val(request, 'chrpos_type') or 'hg38'
    codon_range = (get_param_val(request, 'codon_range') == 'checked')

    param_col_name_map = {
        'type_list': {
            'multi_val': True,
            'col_name':'Type'
        },
        'description_list':{
            'multi_val': True,
            'col_name': 'Description'
        },
        'motif_list': {
            'multi_val': True,
            'col_name':'Structural_motif'
        },
        'exonintron_list': {
            'multi_val': True,
            'col_name': 'ExonIntron'
        },
        'effect_list': {
            'multi_val': True,
            'col_name': 'Effect'
        },
        'ta_class_list': {
            'multi_val': True,
            'col_name': 'TransactivationClass'
        },
        'sift_list': {
            'multi_val': True,
            'col_name': 'SIFTClass'
        },
        'chrpos': {
            'multi_val': False,
            'col_name': '{chrpos_type}_Chr17_coordinates'.format(chrpos_type=chrpos_type),
            'wrap': False
        },
        'mut_base': {
            'multi_val': False,
            'col_name': 'Mutant_nucleotide',
        },
        'codon_no': {
            'multi_val': False,
            'col_name': 'Codon_number',
            'wrap': False
        },
        'codon_range': {
            'between_op': True,
            'max_val': 394,
            'min_val': 1,
            'start_param': 'codon_start',
            'end_param': 'codon_end',
            'col_name': 'Codon_number',
            'wrap': False
        },
        'wild_codon': {
            'multi_val': False,
            'col_name': 'WT_codon'
        },
        'mut_codon': {
            'multi_val': False,
            'col_name': 'Mutant_codon'
        },
        'wild_aa': {
            'multi_val': False,
            'col_name': 'WT_AA'
        },
        'mut_aa': {
            'multi_val': False,
            'col_name': 'Mutant_AA'
        }


    }
    if codon_range:
        del param_col_name_map['codon_no']
    else:
        del param_col_name_map['codon_range']

    for param in param_col_name_map:
        between_op = False
        if param_col_name_map[param].get('between_op', False):
            between_op = True
            start_param = get_param_val(request, param_col_name_map[param]['start_param']) or param_col_name_map[param]['min_val']
            end_param = get_param_val(request, param_col_name_map[param]['end_param']) or param_col_name_map[param]['max_val']
            vals = [start_param, end_param]
        elif param_col_name_map[param]['multi_val']:
            vals = list_param_val(request, param)
        else:
            val = get_param_val(request, param)
            vals = [val] if val else []

        if vals and len(vals):
            wrap_with = '"' if param_col_name_map[param].get('wrap', True) else ''
            criteria.append({'column_name': param_col_name_map[param]['col_name'], 'vals': vals, 'wrap_with': wrap_with, 'between_op': between_op})

    return render_template("gv_result.html", criteria=criteria, result_title=result_title)

@app.route("/gv_query", methods=['GET', 'POST'])
def gv_query():
    parameters = dict(request.form)
    draw = parameters['draw']
    order_col = int(parameters['order[0][column]'])
    order_dir = parameters['order[0][dir]']
    start = int(parameters['start'])
    length = int(parameters['length'])
    criteria = json.loads(parameters['criteria'])
    column_filters = ["MUT_ID", "g_description_GRCh38", "c_description", "ProtDescription", "ExonIntron", "Effect",
                      "TransactivationClass", "AGVGDClass", "Somatic_count", "Germline_count", "Cellline_count",
                      "TCGA_ICGC_GENIE_count", "CLINVARlink", "COSMIClink",
                      "Polymorphism", "SNPlink", "gnomADlink"]
    sql_stm = bq_builder.build_simple_query(criteria=criteria, table='MutationView', column_filters=column_filters,
                                            ord_column=column_filters[order_col], desc_ord=(order_dir == 'desc'),
                                            start=start, length=length)
    sql_cnt_stm = bq_builder.build_simple_query(criteria=criteria, table='MutationView', column_filters=column_filters,
                                                do_counts=True, distinct_col='MUT_ID')

    query_page_job = bigquery_client.query(sql_stm)
    query_count_job = bigquery_client.query(sql_cnt_stm)
    page_result_list = []
    recordsTotal = 0
    try:
        page_result = query_page_job.result(timeout=30)

        count_result = query_count_job.result(timeout=30)
        page_result_list = [dict(row) for row in page_result]
        recordsTotal = list(count_result)[0].CNT
    except BadRequest:
        error_msg = "There was a problem with your search input. Please revise your search criteria and search again."
    except (concurrent.futures.TimeoutError, requests.exceptions.ReadTimeout):
        error_msg = "Sorry, query job has timed out."

    data = {
        "draw": draw,
        "recordsTotal": recordsTotal,
        "recordsFiltered": recordsTotal,
        "data": page_result_list
    }

    return jsonify(data)


@app.route("/search_tp53data")
def search_tp53data():
    return render_template("search_tp53data.html")


@app.route("/search_gv")
def search_gv():
    global m_c_desc_list
    if not m_c_desc_list:
        m_c_desc_list = load_list(M_C_DESC_FILE)

    global m_p_desc_list
    if not m_p_desc_list:
        m_p_desc_list = load_list(M_P_DESC_FILE)

    global m_g_desc_hg19_list
    if not m_g_desc_hg19_list:
        m_g_desc_hg19_list = load_list(M_G_DESC_HG19_FILE)

    global m_g_desc_hg38_list
    if not m_g_desc_hg38_list:
        m_g_desc_hg38_list = load_list(M_G_DESC_HG38_FILE)

    return render_template("search_tp53_gene_variants.html", c_desc_list=m_c_desc_list, p_desc_list=m_p_desc_list,
                           g_desc_hg19_list=m_g_desc_hg19_list, g_desc_hg38_list=m_g_desc_hg38_list)


@app.route("/mut_details", methods=['GET'])
def mut_details():
    mut_id = get_param_val(request, 'mut_id')

    simple_queries = {
        'mut_desc': {
            'column_filters': ['g_description_GRCh38', 'c_description', 'ProtDescription', 'ExonIntron', 'CpG_site',
                               'Splice_site', 'Context_coding_3', 'WT_codon', 'Mutant_codon', 'Effect',
                               'EffectGroup3', 'MUT_ID'],
            'criteria': [{'column_name': 'MUT_ID', 'vals': [mut_id]}],
            'table': 'MutationView',
            'ord_column': 'MUT_ID'
        },
        'splice_pred': {
            'column_filters': ['Splice_Site_Type', 'p53SpliceSite', 'WT_score', 'Mutant_score', 'Variation',
                               'Source', 'MUT_ID'],
            'criteria': [{'column_name': 'MUT_ID', 'vals': [mut_id]}],
            'table': 'SPLICING_PREDICTION',
            'ord_column': 'MUT_ID'
        },
        'prot_desc': {
            'column_filters': ['Structural_motif', 'Domain_function', 'Residue_function', 'Hotspot', 'Mut_rate',
                               'SwissProtLink', 'MUT_ID'],
            'criteria': [{'column_name': 'MUT_ID', 'vals': [mut_id]}],
            'table': 'MutationView',
            'ord_column': 'MUT_ID'
        },
        'sys_assess': {
            'column_filters': ['WAF1nWT', 'MDM2nWT', 'BAXnWT', 'h1433snWT', 'AIP1nWT',
                               'GADD45nWT', 'NOXAnWT', 'P53R2nWT', 'WAF1nWT_Saos2', 'MDM2nWT_Saos2', 'BAXnWT_Saos2',
                               'h1433snWT_Saos2', 'AIP1nWT_Saos2', 'PUMAnWT_Saos2', 'MUT_ID'],
            'criteria': [{'column_name': 'MUT_ID', 'vals': [mut_id]}],
            'table': 'MutationView',
            'ord_column': 'MUT_ID'
        },
        'prot_pred': {
            'column_filters': ['TransactivationClass', 'DNEclass', 'DNE_LOFclass', 'AGVGDClass', 'BayesDel', 'REVEL',
                               'SIFTClass', 'Polyphen2', 'StructureFunctionClass', 'MUT_ID'],
            'criteria': [{'column_name': 'MUT_ID', 'vals': [mut_id]}],
            'table': 'MutationView',
            'ord_column': 'MUT_ID'
        },
        'p53_pred': {
            'column_filters': ['TAp53', 'TAp53beta', 'TAp53gamma', 'delta40p53', 'delta40p53beta', 'delta40p53gamma',
                               'delta133p53', 'delta133p53beta', 'delta133p53gamma', 'deltap53', 'MUT_ID'],
            'criteria': [{'column_name': 'MUT_ID', 'vals': [mut_id]}],
            'table': 'ISOFORMS_STATUS',
            'ord_column': 'MUT_ID'
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
        # 'induced': {
        #     'mut_id': mut_id,
        #     'column_filters': ['Exposure', 'Model', 'PubMed', 'MUT_ID'],
        #     'table': 'InducedMutationView',
        #     'join_column': 'MUT_ID',
        #     'ord_column': 'MUT_ID'
        # }
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

    error_msg = {}
    query_result = {}
    for t_id in sql_stms:
        try:
            query_jobs = bigquery_client.query(sql_stms[t_id])
            query_result[t_id] = list(query_jobs.result(timeout=30))
        except BadRequest:
            error_msg[
                t_id] = "There was a problem with your search input. Please revise your search criteria and search again."
        except (concurrent.futures.TimeoutError, requests.exceptions.ReadTimeout):
            error_msg[t_id] = "Sorry, query job has timed out."
    if query_result['mut_desc'] and query_result['mut_desc'][0] and query_result['mut_desc'][0]['ProtDescription']:
        p_desc = query_result['mut_desc'][0]['ProtDescription']
        if p_desc == 'p.?':
            query_result['sys_assess'] = []
            query_result['prot_desc'] = []
            query_result['prot_pred'] = []
            query_result['p53_pred'] = []
            query_result['vars_act'] = []
            query_result['mouse'] = []
    if query_result['sys_assess'] and query_result['sys_assess'][0] and not query_result['sys_assess'][0]['WAF1nWT']:
        query_result['sys_assess'] = []
    if query_result['prot_pred'] and query_result['prot_pred'][0]:
        data_is_null = True
        for i in range(len(query_result['prot_pred'][0]) - 1):
            if query_result['prot_pred'][0][i] and query_result['prot_pred'][0][i].lower() != 'na':
                data_is_null = False
                break
        if data_is_null:
            query_result['prot_pred'] = []

    return render_template("mut_details.html", query_result=query_result, error_msg=error_msg)


# def is_data_null(row_data):
#     data_is_null = True
#     for i in range(len(row_data) - 1):
#         if row_data[i] and row_data[i].lower() != 'na':
#             data_is_null = False
#             break
#     return data_is_null
@app.route("/search_gmut")
def search_gmut():
    # global m_type_list
    # if not m_type_list:
    #     m_type_list = load_list(M_TYPE_FILE)
    #
    # global m_desc_list
    # if not m_desc_list:
    #     m_desc_list = load_list(M_DESC_FILE)
    #
    # global m_motif_list
    # if not m_motif_list:
    #     m_motif_list = load_list(M_MOTIF_FILE)

    # global m_exon_intron_list
    # if not m_exon_intron_list:
    #     m_exon_intron_list = load_list(M_EXON_INTRON_FILE)

    # global m_effect_list
    # if not m_effect_list:
    #     m_effect_list = load_list(M_EFFECT_FILE)
    #
    # global m_ta_class_list
    # if not m_ta_class_list:
    #     m_ta_class_list = load_list(M_TA_CLASS_FILE)
    #
    # global m_sift_list
    # if not m_sift_list:
    #     m_sift_list = load_list(M_SIFT_FILE)

    return render_template("search_tp53_gene_by_mut.html", type_list=m_type_list, desc_list=m_desc_list,
                           motif_list=m_motif_list, effect_list=m_effect_list,
                           exon_intron_list=m_exon_intron_list, ta_class_list=m_ta_class_list, sift_list=m_sift_list)


@app.route("/view_exp_ind_mut")
def view_exp_ind_mut():

    column_filters = ['Exposure', 'g_description_GRCh38', 'c_description', 'ProtDescription', 'Model', 'Clone_ID', 'Add_Info', 'PubMed', 'MUT_ID']
    criteria = []

    sql_stm = bq_builder.build_simple_query(criteria=criteria, table='InducedMutationView', column_filters=column_filters)
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

    return render_template("view_exp_ind_mut.html", criteria=criteria, query_result=query_result)


@app.route("/view_mouse")
def view_mouse():
    column_filters = ['ModelDescription', 'TumorSites', 'AAchange', 'caMOD_ID', 'PubMed', 'MM_ID']
    criteria = []
    # criteria = [{'column_name': 'polymorphism', 'vals': ['validated'], 'wrap_with': '"'}]

    sql_stm = bq_builder.build_simple_query(criteria=criteria, table='MouseModelView', column_filters=column_filters)
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

    return render_template("view_mouse.html", criteria=criteria, query_result=query_result)


@app.route("/view_val_poly")
def view_val_poly():
    column_filters = ['g_description_GRCh38', 'c_description', 'ProtDescription', 'ExonIntron', 'Effect',
                      'SNPlink', 'gnomADlink', 'CLINVARlink', 'PubMedlink', 'SourceDatabases']
    criteria = [{'column_name': 'polymorphism', 'vals': ['validated'], 'wrap_with': '"'}]

    sql_stm = bq_builder.build_simple_query(criteria=criteria, table='MutationView', column_filters=column_filters)
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

    return render_template("view_val_poly.html", criteria=criteria, query_result=query_result)

@app.route("/search_cell_lines")
def search_cell_lines():
    # global cl_tp53stat_list
    # if not cl_tp53stat_list:
    #     cl_tp53stat_list = load_list(CL_TP53STAT_FILE)
    # global cl_tumor_org_group_list
    # if not cl_tumor_org_group_list:
    #     cl_tumor_org_group_list = load_list(CL_TUMOR_ORG_GROUP_FILE)
    # global cl_topo_list
    # if not cl_topo_list:
    #     cl_topo_list = load_list(CL_TOPO_FILE)
    # global cl_morph_list
    # if not cl_morph_list:
    #     cl_morph_list = load_list(CL_MORPH_FILE)



    return render_template("search_cell_lines.html",
                           c_desc_list=cl_c_desc_list,
                           p_desc_list=cl_p_desc_list,
                           g_desc_hg19_list=cl_g_desc_hg19_list,
                           g_desc_hg38_list=cl_g_desc_hg38_list,
                           cl_tp53stat_list=cl_tp53stat_list,
                           cl_tumor_org_group_list=cl_tumor_org_group_list,
                           cl_morph_list=cl_morph_list,
                           cl_topo_list=cl_topo_list,
                           cl_start_material_list=cl_start_material_list,
                           desc_list=cl_desc_list,
                           effect_list=cl_effect_list,
                           motif_list=cl_motif_list,
                           type_list=cl_type_list,
                           sift_list=cl_sift_list,
                           exon_intron_list=cl_exon_intron_list,
                           ta_class_list=cl_ta_class_list,
                           germ_mut_list=cl_germ_mut_list,
                           inf_agnt_list=cl_inf_agnt_list,
                           country_list=country_list,
                           exposure_list=cl_exposure_list

                           )

# @app.route("/mutation_search_form")
# def mutation_search_form():
#     return render_template("mutation_search_form.html")

@app.route("/get_tp53data")
def get_tp53data():
    return render_template("get_tp53data.html")


@app.route("/help")
def help():
    return render_template("help.html")


@app.route("/hg38seq")
def hg38seq():
    return render_template("hg38seq.html")


@app.route("/tp53seq")
def tp53seq():
    return render_template("tp53seq.html")


@app.route("/p53isoforms")
def p53isoforms():
    return render_template("p53isoforms.html")


@app.route("/seq_align")
def seq_align():
    return render_template("seq_align.html")


@app.route("/aa_codes")
def aa_codes():
    return render_template("aa_codes.html")


@app.route("/genetic_code")
def genetic_code():
    return render_template("genetic_code.html")


@app.route("/dt_method")
def dt_method():
    return render_template("dt_method.html")


@app.route("/stability")
def stability():
    return render_template("stability.html")


@app.route("/tnm_class")
def tnm_class():
    return render_template("tnm_class.html")


@app.route("/country")
def country():
    return render_template("country.html")


@app.route("/topo")
def topo():
    return render_template("topo.html")


@app.route("/morph")
def morph():
    return render_template("morph.html")


@app.route("/target_genes")
def target_genes():
    return render_template("target_genes.html")


@app.route("/ts_annotations")
def ts_annotations():
    return render_template("ts_annotations.html")


@app.route("/resources")
def resources():
    return render_template("resources.html")


@app.route("/refs_corner")
def refs_corner():
    return render_template("refs_corner.html")


@app.route("/ppl_events")
def ppl_events():
    return render_template("ppl_events.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/tp53book")
def tp53book():
    return render_template("tp53book.html")


@app.route("/tp53book2013")
def tp53book2013():
    return render_template("tp53book2013.html")


@app.route("/p53IsoformsPredictions")
def p53IsoformsPredictions():
    return render_template("p53IsoformsPredictions.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# @app.route('/get_cdesc')
# def get_cdesc():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/_ah/warmup')
def warmup():
    # Handle your warmup logic here, e.g. set up a database connection pool
    return '', 200, {}


# def create_html_table(list_file, title):
#     try:
#         file_path = TP53_STATIC_URL + TIER + '/list-files/' + list_file
#         file_data = requests.get(file_path)
#         lines = file_data.text.splitlines()
#         html_table = "<table class='table table-sm table-striped table-in-modal'><thead><tr><th>"
#         html_table += title
#         html_table += "</th></tr></thead><tbody>"
#         for line in lines:
#             html_table += '<tr><td>'
#             html_table += line
#             html_table += '</td></tr>'
#         html_table += "</tbody></table>"
#     except:
#         html_table = ''
#     return html_table
#
#


def load_list(list_file, limit=None):
    option_list = []
    # if list_file.endswith('json'):

    # options = get_koder_options(list_file)
    # else:
    #     options = koder_op
    # for item in list_items:
    #     print(item)
    # value = options[label]
    #     option_list.append({'label': label, 'value': value})
    # else:
    try:
        file_path = TP53_STATIC_URL + '/list-files/' + list_file
        file_data = requests.get(file_path)
        lines = file_data.text.splitlines()
        if limit:
            lines = lines[0:limit]
        for line in lines:
            option_list.append({'label': line })
        # for item in lines:
        #     option_list.append({'label': item, 'value': item.replace(' ', '_')})
    except:
        option_list = []
    return option_list


#
#
# def get_koder_options(filename):
#     options = None
#     try:
#         file_path = TP53_STATIC_URL + TIER + '/list-files/'+filename
#         data = requests.get(file_path).json()
#         if filename == KODER_RACE_FILE:
#             # move 'Other' option to the end
#             if 'Other' in data.keys():
#                 value = data.pop('Other')
#                 data['Other'] = value
#         options = data
#     except:
#         print('Unable to open ' + filename)
#     return options
#
def setup_app(app):
    global m_c_desc_list
    if not m_c_desc_list:
        m_c_desc_list = load_list(M_C_DESC_FILE)

    global m_p_desc_list
    if not m_p_desc_list:
        m_p_desc_list = load_list(M_P_DESC_FILE)

    global m_g_desc_hg19_list
    if not m_g_desc_hg19_list:
        m_g_desc_hg19_list = load_list(M_G_DESC_HG19_FILE)

    global m_g_desc_hg38_list
    if not m_g_desc_hg38_list:
        m_g_desc_hg38_list = load_list(M_G_DESC_HG38_FILE)

    global m_type_list
    if not m_type_list:
        m_type_list = load_list(M_TYPE_FILE)

    global m_desc_list
    if not m_desc_list:
        m_desc_list = load_list(M_DESC_FILE)

    global m_motif_list
    if not m_motif_list:
        m_motif_list = load_list(M_MOTIF_FILE)

    global m_exon_intron_list
    if not m_exon_intron_list:
        m_exon_intron_list = load_list(M_EXON_INTRON_FILE)

    global m_effect_list
    if not m_effect_list:
        m_effect_list = load_list(M_EFFECT_FILE)

    global m_ta_class_list
    if not m_ta_class_list:
        m_ta_class_list = load_list(M_TA_CLASS_FILE)

    global m_sift_list
    if not m_sift_list:
        m_sift_list = load_list(M_SIFT_FILE)


    global cl_c_desc_list
    if not cl_c_desc_list:
        cl_c_desc_list = load_list(CL_C_DESC_FILE)
    global cl_p_desc_list
    if not cl_p_desc_list:
        cl_p_desc_list = load_list(CL_P_DESC_FILE)
    global cl_g_desc_hg19_list
    if not cl_g_desc_hg19_list:
        cl_g_desc_hg19_list = load_list(CL_G_DESC_HG19_FILE)
    global cl_g_desc_hg38_list
    if not cl_g_desc_hg38_list:
        cl_g_desc_hg38_list = load_list(CL_G_DESC_HG38_FILE)

    global cl_topo_list
    if not cl_topo_list:
        cl_topo_list = load_list(CL_TOPO_FILE)

    global cl_morph_list
    if not cl_morph_list:
        cl_morph_list = load_list(CL_MORPH_FILE)

    global cl_tp53stat_list
    if not cl_tp53stat_list:
        cl_tp53stat_list = load_list(CL_TP53STAT_FILE)

    global cl_tumor_org_group_list
    if not cl_tumor_org_group_list:
        cl_tumor_org_group_list = load_list(CL_TUMOR_ORG_GROUP_FILE)
        
    global cl_desc_list
    if not cl_desc_list:
        cl_desc_list = load_list(CL_DESC_FILE)
    global cl_effect_list
    if not cl_effect_list:
        cl_effect_list = load_list(CL_EFFECT_FILE)
    global cl_motif_list
    if not cl_motif_list:
        cl_motif_list = load_list(CL_MOTIF_FILE)
    global cl_start_material_list
    if not cl_start_material_list:
        cl_start_material_list = load_list(CL_START_MATERIAL_FILE)
    global cl_ta_class_list
    if not cl_ta_class_list:
        cl_ta_class_list = load_list(CL_TA_CLASS_FILE)
    global cl_type_list
    if not cl_type_list:
        cl_type_list = load_list(CL_TYPE_FILE)
    global cl_sift_list
    if not cl_sift_list:
        cl_sift_list = load_list(CL_SIFT_FILE)
    global cl_exon_intron_list
    if not cl_exon_intron_list:
        cl_exon_intron_list = load_list(CL_EXON_INTRON_FILE)
    global cl_germ_mut_list
    if not cl_germ_mut_list:
        cl_germ_mut_list = load_list(CL_GERM_MUT_FILE)
    global cl_inf_agnt_list
    if not cl_inf_agnt_list:
        cl_inf_agnt_list = load_list(CL_INF_AGNT_FILE)
    global country_list
    if not country_list:
        country_list = load_list(COUNTRY_FILE)
    global cl_exposure_list
    if not cl_exposure_list:
        cl_exposure_list = load_list(CL_EXPOSURE_FILE)
    return


setup_app(app)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        TIER = sys.argv[1]
        if TIER.lower() != 'test' and TIER.lower() != 'prod' and TIER.lower() != 'uat':
            TIER = 'test'  # default DATA SET
        bq_builder.set_project_dataset(proj_id=project_id, d_set=TIER)
    app.run(host='127.0.0.1', port=8080, debug=True)
