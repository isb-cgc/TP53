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
# KODER_GEO_FILE = 'KODER_GEO.json'
# KODER_HER_FILE = 'KODER_HER.json'
# KODER_RACE_FILE = 'KODER_RACE.json'
# KODER_TISSUE_FILE = 'KODER_TISSUE.json'
# KODER_TREAT_FILE = 'KODER_TREAT.json'
# KODER_MORPH_FILE = 'KODER_MORPH.json'
# KODER_TOP_FILE = 'KODER_TOP.json'
# MITELMAN_META_FILE = 'MITELMAN_META_FILE.json'
# JOUR_LIST_FILE = 'JOUR_LIST.TXT.LIST'
# S_HER_LIST_FILE = 'S_HER_LIST.TXT.LIST'
# S_MOR_LIST_FILE = 'S_MOR_LIST.TXT.LIST'
C_DESC_FILE = 'C_DESC.TXT.LIST'
P_DESC_FILE = 'P_DESC.TXT.LIST'
G_DESC_HG19_FILE = 'G_DESC_HG19.TXT.LIST'
G_DESC_HG38_FILE = 'G_DESC_HG38.TXT.LIST'
# CG_LIST_FILE = 'CG_LIST.TXT.LIST'
# MG_LIST_FILE = 'MG_LIST.TXT.LIST'
#
# global jour_table
# jour_table = None
# global sher_table
# sher_table = None
# global smor_table
# smor_table = None
#
# global rg_list
# rg_list = None
# global cg_list
# cg_list = None
# global mg_list
# mg_list = None
# global morph_list
# morph_list = None
# global topo_list
# topo_list = None
# global koder_options
# koder_options = None
#

app = Flask(__name__)

global c_desc_list
c_desc_list = None

global p_desc_list
p_desc_list = None

global g_desc_hg19_list
g_desc_hg19_list = None

global g_desc_hg38_list
g_desc_hg38_list = None

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


# # Search Menu
# @app.route("/search_menu")
# def search_menu():
#     return render_template("search_menu.html")
#
# # Cases Cytogenetics
# @app.route("/case_search")
# def case_search():
#     global jour_table
#     global koder_options
#     global sher_table
#     global smor_table
#     if not jour_table:
#         jour_table = create_html_table(JOUR_LIST_FILE, 'Journal Name')
#     if not sher_table:
#         sher_table = create_html_table(S_HER_LIST_FILE, 'Special Hereditary Disorder')
#     if not smor_table:
#         smor_table = create_html_table(S_MOR_LIST_FILE, 'Special Morphology')
#     if not koder_options:
#         koder_options = {}
#     if 'GEO' not in koder_options.keys():
#         koder_options['GEO'] = get_koder_options(KODER_GEO_FILE)
#     if 'HER' not in koder_options.keys():
#         koder_options['HER'] = get_koder_options(KODER_HER_FILE)
#     if 'MORPH' not in koder_options.keys():
#         koder_options['MORPH'] = get_koder_options(KODER_MORPH_FILE)
#     if 'RACE' not in koder_options.keys():
#         koder_options['RACE'] = get_koder_options(KODER_RACE_FILE)
#     if 'TISSUE' not in koder_options.keys():
#         koder_options['TISSUE'] = get_koder_options(KODER_TISSUE_FILE)
#     if 'TOP' not in koder_options.keys():
#         koder_options['TOP'] = get_koder_options(KODER_TOP_FILE)
#     if 'TREAT' not in koder_options.keys():
#         koder_options['TREAT'] = get_koder_options(KODER_TREAT_FILE)
#
#     return render_template("case_search.html", koder_options=koder_options, sher_table=sher_table,
#                            smor_table=smor_table, jour_table=jour_table)
#
# # Clinical Associations
# @app.route("/clinical_search")
# def clinical_search():
#     global jour_table
#     global cg_list
#     global morph_list
#     global topo_list
#     if not morph_list:
#         morph_list = load_list(KODER_MORPH_FILE, koder_options['MORPH'])
#     if not topo_list:
#         topo_list = load_list(KODER_TOP_FILE, koder_options['TOP'])
#     if not cg_list:
#         cg_list = load_list(CG_LIST_FILE)
#     if not jour_table:
#         jour_table = create_html_table(JOUR_LIST_FILE, 'Journal Name')
#     gene_table = create_html_table(CG_LIST_FILE, 'Gene Name')
#     return render_template("clinical_search.html", jour_table=jour_table, gene_list=cg_list, morph_list=morph_list,
#                            topo_list=topo_list, gene_table=gene_table)
#
# # Gene Fusions
# @app.route("/mb_search")
# def mb_search():
#     global jour_table
#     global morph_list
#     global topo_list
#
#     if not jour_table:
#         jour_table = create_html_table(JOUR_LIST_FILE, 'Journal Name')
#     if not morph_list:
#         morph_list = load_list(KODER_MORPH_FILE, koder_options['MORPH'])
#     if not topo_list:
#         topo_list = load_list(KODER_TOP_FILE, koder_options['TOP'])
#     gene_table = create_html_table(MG_LIST_FILE, 'Gene Name')
#     return render_template("mb_search.html", jour_table=jour_table, morph_list=morph_list, topo_list=topo_list, gene_table=gene_table)
#
# #
# @app.route("/get_mglist")
# def get_mglist():
#     global mg_list
#     if not mg_list:
#         mg_list = load_list(MG_LIST_FILE)
#     return jsonify(mg_list)
#
# # Recurrent Chromosome Aberrations
# @app.route("/recab_search")
# def recab_search():
#     global rg_list
#     global morph_list
#     global topo_list
#     if not rg_list:
#         rg_list = load_list(RG_LIST_FILE)
#     if not morph_list:
#         morph_list = load_list(KODER_MORPH_FILE, koder_options['MORPH'])
#     if not topo_list:
#         topo_list = load_list(KODER_TOP_FILE, koder_options['TOP'])
#     return render_template("recab_search.html", gene_list=rg_list, morph_list=morph_list, topo_list=topo_list)
#
# # References Search
# @app.route("/ref_search")
# def ref_search():
#     global jour_table
#
#     if not jour_table:
#         jour_table = create_html_table(JOUR_LIST_FILE, 'Journal Name')
#
#     return render_template("ref_search.html", jour_table=jour_table)
#
#
# @app.route("/case_details", methods=['GET'])
# def case_details():
#     global koder_options
#     error_msg = None
#     detail_info = {}
#
#     if request.method == 'GET':
#         refno = request.args.get('refno')
#         caseno = request.args.get('caseno')
#         sql_stm = bq_builder.build_get_case(refno, caseno)
#         query_job = bigquery_client.query(sql_stm)
#         template_page = "case_details.html"
#         kary_list = []
#         try:
#             # Set a timeout because queries could take longer than one minute.
#             result = query_job.result(timeout=30)
#             if result.total_rows == 0:
#                 raise Exception
#
#             rows = list(result)
#             for r in rows:
#                 kary = r.KaryLong if r.KaryLong else r.KaryShort
#                 if kary:
#                     kary_list.append(kary)
#             row_0 = rows[0]
#             detail_info = row_0
#         except concurrent.futures.TimeoutError:
#             error_msg = "Sorry, query job has timed out."
#         except Exception:
#             error_msg = "Unable to find the case"
#
#     return render_template(template_page, detail_info=detail_info, kary_list=kary_list, error_msg=error_msg)
#
#
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
                                            # sql_stm = bq_builder.build_simple_query(criteria=criteria, tables=[{'name':'MutationView'], column_filters=column_filters,
                                            ord_column=column_filters[order_col], desc_ord=(order_dir == 'desc'),
                                            start=start, length=length)
    # sql_cnt_stm = bq_builder.build_simple_query(criteria=criteria, tables=[{'name':'MutationView'], column_filters=column_filters,
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
    global c_desc_list
    if not c_desc_list:
        c_desc_list = load_list(C_DESC_FILE)

    global p_desc_list
    if not p_desc_list:
        p_desc_list = load_list(P_DESC_FILE)

    global g_desc_hg19_list
    if not g_desc_hg19_list:
        g_desc_hg19_list = load_list(G_DESC_HG19_FILE)

    global g_desc_hg38_list
    if not g_desc_hg38_list:
        g_desc_hg38_list = load_list(G_DESC_HG38_FILE)

    return render_template("search_tp53_gene_variants.html", c_desc_list=c_desc_list, p_desc_list=p_desc_list,
                           g_desc_hg19_list=g_desc_hg19_list, g_desc_hg38_list=g_desc_hg38_list)


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
    return render_template("search_tp53_gene_by_mut.html")


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

        for label in lines:
            option_list.append({'label': label})
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
    global c_desc_list
    if not c_desc_list:
        c_desc_list = load_list(C_DESC_FILE)

    global p_desc_list
    if not p_desc_list:
        p_desc_list = load_list(P_DESC_FILE)

    global g_desc_hg19_list
    if not g_desc_hg19_list:
        g_desc_hg19_list = load_list(G_DESC_HG19_FILE)

    global g_desc_hg38_list
    if not g_desc_hg38_list:
        g_desc_hg38_list = load_list(G_DESC_HG38_FILE)
    #     global jour_table
    #     global koder_options
    #     global sher_table
    #     global smor_table
    #     global rg_list
    #     global cg_list
    #     global mg_list
    #     global morph_list
    #     global topo_list
    #     if not jour_table:
    #         jour_table = create_html_table(JOUR_LIST_FILE, 'Journal Name')
    #     if not sher_table:
    #         sher_table = create_html_table(S_HER_LIST_FILE, 'Special Hereditary Disorder')
    #     if not smor_table:
    #         smor_table = create_html_table(S_MOR_LIST_FILE, 'Special Morphology')
    #     if not koder_options:
    #         koder_options = {}
    #     if 'GEO' not in koder_options.keys():
    #         koder_options['GEO'] = get_koder_options(KODER_GEO_FILE)
    #     if 'HER' not in koder_options.keys():
    #         koder_options['HER'] = get_koder_options(KODER_HER_FILE)
    #     if 'MORPH' not in koder_options.keys():
    #         koder_options['MORPH'] = get_koder_options(KODER_MORPH_FILE)
    #     if 'RACE' not in koder_options.keys():
    #         koder_options['RACE'] = get_koder_options(KODER_RACE_FILE)
    #     if 'TISSUE' not in koder_options.keys():
    #         koder_options['TISSUE'] = get_koder_options(KODER_TISSUE_FILE)
    #     if 'TOP' not in koder_options.keys():
    #         koder_options['TOP'] = get_koder_options(KODER_TOP_FILE)
    #     if 'TREAT' not in koder_options.keys():
    #         koder_options['TREAT'] = get_koder_options(KODER_TREAT_FILE)
    #     if not rg_list:
    #         rg_list = load_list(RG_LIST_FILE)
    #     if not cg_list:
    #         cg_list = load_list(CG_LIST_FILE)
    #     if not mg_list:
    #         mg_list = load_list(MG_LIST_FILE)
    #     if not morph_list:
    #         morph_list = load_list(KODER_MORPH_FILE, koder_options['MORPH'])
    #     if not topo_list:
    #         topo_list = load_list(KODER_TOP_FILE, koder_options['TOP'])
    return


setup_app(app)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        TIER = sys.argv[1]
        if TIER.lower() != 'test' and TIER.lower() != 'prod' and TIER.lower() != 'uat':
            TIER = 'test'  # default DATA SET
        bq_builder.set_project_dataset(proj_id=project_id, d_set=TIER)
    app.run(host='127.0.0.1', port=8080, debug=True)
