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
import copy

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
TOPO_FILE = 'TOPO.TXT.LIST'
MORPH_FILE = 'MORPH.TXT.LIST'
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

SM_START_MATERIAL_FILE = 'SM_START_MATERIAL.TXT.LIST'

SM_C_DESC_FILE = 'SM_C_DESC.TXT.LIST'
SM_P_DESC_FILE = 'SM_P_DESC.TXT.LIST'
SM_G_DESC_HG19_FILE = 'SM_G_DESC_HG19.TXT.LIST'
SM_G_DESC_HG38_FILE = 'SM_G_DESC_HG38.TXT.LIST'

SM_TYPE_FILE = 'SM_TYPE.TXT.LIST'
SM_DESC_FILE = 'SM_DESC.TXT.LIST'
SM_MOTIF_FILE = 'SM_MOTIF.TXT.LIST'
SM_EXON_INTRON_FILE = 'SM_EXON_INTRON.TXT.LIST'
SM_EFFECT_FILE = 'SM_EFFECT.TXT.LIST'
SM_TA_CLASS_FILE = 'SM_TA_CLASS.TXT.LIST'
SM_SIFT_FILE = 'SM_SIFT.TXT.LIST'
SM_TUMOR_ORG_GROUP_FILE = 'SM_TUMOR_ORG_GROUP.TXT.LIST'
SM_SAMPLE_SOURCE_GROUP_FILE = 'SM_SAMPLE_SOURCE_GROUP.TXT.LIST'
SM_GERM_MUT_FILE = 'SM_GERM_MUT.TXT.LIST'
SM_INF_AGNT_FILE = 'SM_INF_AGNT.TXT.LIST'
SM_EXPOSURE_FILE = 'SM_EXPOSURE.TXT.LIST'
COUNTRY_FILE = 'COUNTRY.TXT.LIST'

GM_C_DESC_FILE = 'GM_C_DESC.TXT.LIST'
GM_P_DESC_FILE = 'GM_P_DESC.TXT.LIST'
GM_G_DESC_HG19_FILE = 'GM_G_DESC_HG19.TXT.LIST'
GM_G_DESC_HG38_FILE = 'GM_G_DESC_HG38.TXT.LIST'
GM_TYPE_FILE = 'GM_TYPE.TXT.LIST'
GM_DESC_FILE = 'GM_DESC.TXT.LIST'
GM_MOTIF_FILE = 'GM_MOTIF.TXT.LIST'
GM_EXON_INTRON_FILE = 'GM_EXON_INTRON.TXT.LIST'
GM_EFFECT_FILE = 'GM_EFFECT.TXT.LIST'
GM_TA_CLASS_FILE = 'GM_TA_CLASS.TXT.LIST'
GM_SIFT_FILE = 'GM_SIFT.TXT.LIST'
GM_FAMILY_HIST_FILE = 'GM_FAMILY_HIST.TXT.LIST'
GM_INH_MODE_FILE = 'GM_INH_MODE.TXT.LIST'
GM_FAMILY_CASE_FILE = 'GM_FAMILY_CASE.TXT.LIST'

TOPO_MORPH_JSON_FILE = 'TOPO_MORPH.json'
GM_REF_FILE = 'GM_REF.json'

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

global topo_list
topo_list = None

global morph_list
morph_list = None

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
global sm_c_desc_list
sm_c_desc_list = None
global sm_p_desc_list
sm_p_desc_list = None
global sm_g_desc_hg19_list
sm_g_desc_hg19_list = None
global sm_g_desc_hg38_list
sm_g_desc_hg38_list = None
global sm_morph_list
sm_morph_list = None
global sm_start_material_list
sm_start_material_list = None
global sm_type_list
sm_type_list = None
global sm_desc_list
sm_desc_list = None
global sm_motif_list
sm_motif_list = None
global sm_exon_intron_list
sm_exon_intron_list = None
global sm_effect_list
sm_effect_list = None
global sm_ta_class_list
sm_ta_class_list = None
global sm_sift_list
sm_sift_list = None
global sm_tumor_org_group_list
sm_tumor_org_group_list = None
global sm_sample_source_list
sm_sample_source_list = None
global sm_germ_mut_list
sm_germ_mut_list = None
global sm_inf_agnt_list
sm_inf_agnt_list = None
global sm_exposure_list
sm_exposure_list = None
global gm_c_desc_list
gm_c_desc_list = None
global gm_p_desc_list
gm_p_desc_list = None
global gm_g_desc_hg19_list
gm_g_desc_hg19_list = None
global gm_g_desc_hg38_list
gm_g_desc_hg38_list = None
global gm_type_list
gm_type_list = None
global gm_desc_list
gm_desc_list = None
global gm_motif_list
gm_motif_list = None
global gm_exon_intron_list
gm_exon_intron_list = None
global gm_effect_list
gm_effect_list = None
global gm_ta_class_list
gm_ta_class_list = None
global gm_sift_list
gm_sift_list = None
global gm_family_hist_list
gm_family_hist_list = None
global gm_inh_mode_list
gm_inh_mode_list = None
global gm_family_case_list
gm_family_case_list = None
global topo_morph_assc
topo_morph_assc = None
global gm_ref_data
gm_ref_data = None

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


@app.route("/results_gene_mutation", methods=['GET', 'POST'])
def results_gene_mutation():
    criteria = []
    column_name = None
    variations = None

    type_input = get_param_val(request, 'type_input')
    if type_input == 'type_cdna':
        column_name = 'c_description'
        variations = list_param_val(request, 'gv_cdna_list')
    elif type_input == 'type_p':
        column_name = 'ProtDescription'
        variations = list_param_val(request, 'gv_p_list')
    elif type_input == 'type_hg19':
        column_name = 'g_description'
        variations = list_param_val(request, 'gv_hg19_list')
    elif type_input == 'type_hg38':
        column_name = 'g_description_GRCh38'
        variations = list_param_val(request, 'gv_hg38_list')

    if column_name and variations and len(variations):
        criteria.append({'column_name': column_name, 'vals': variations, 'wrap_with': '"'})
    return render_template("results_gene_mutation.html", criteria=criteria,)


def build_criteria(param_col_name_map):
    criteria = []

    for param_key in param_col_name_map:
        or_group = ''
        between_op = False
        if param_col_name_map[param_key].get('or_group'):
            or_group = param_col_name_map[param_key].get('or_group')
        if param_col_name_map[param_key].get('multi_columns'):
            i = param_key.rindex('_')
            x = slice(i)
            param_name = param_key[x]
            or_group = param_name
        else:
            param_name = param_key
        print(param_name)
        if param_col_name_map[param_key].get('between_op', False):
            between_op = True
            start_param = get_param_val(request, param_col_name_map[param_key]['start_param'])
            end_param = get_param_val(request, param_col_name_map[param_key]['end_param'])
            if not start_param and not end_param:
                vals = []
            else:
                vals = [start_param or param_col_name_map[param_key]['min_val'],
                        end_param or param_col_name_map[param_key]['max_val']]
        elif param_col_name_map[param_key]['multi_val']:
            vals = list_param_val(request, param_name)

        else:
            val = get_param_val(request, param_name)
            vals = [val] if val else []
        print(vals)
        if vals and len(vals):
            wrap_with = '"' if param_col_name_map[param_key].get('wrap', True) else ''
            criteria.append(
                {'column_name': param_col_name_map[param_key]['col_name'], 'vals': vals, 'wrap_with': wrap_with,
                 'or_group': or_group, 'between_op': between_op})
    return criteria


def get_mut_id_criteria():
    param_col_name_map = {
        'mut_id_list':{
            'multi_val': True,
            'col_name': 'MUT_ID',
            'wrap': False
        }
    }
    return build_criteria(param_col_name_map)


def get_mutation_criteria(prefix):
    chrpos_type = get_param_val(request, '{prefix}_chrpos_type'.format(prefix=prefix)) or 'hg38'
    codon_range = (get_param_val(request, '{prefix}_codon_range'.format(prefix=prefix)) == 'checked')

    param_col_name_map = {
        '{prefix}_type_list'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Type'
        },
        '{prefix}_description_list'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Description'
        },
        '{prefix}_motif_list'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Structural_motif'
        },
        '{prefix}_exonintron_list'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'ExonIntron'
        },
        '{prefix}_effect_list'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Effect'
        },
        '{prefix}_ta_class_list'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'TransactivationClass'
        },
        '{prefix}_sift_list'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'SIFTClass'
        },
        '{prefix}_chrpos'.format(prefix=prefix): {
            'multi_val': False,
            'col_name': '{chrpos_type}_Chr17_coordinates'.format(chrpos_type=chrpos_type),
            'wrap': False
        },
        '{prefix}_mut_base'.format(prefix=prefix): {
            'multi_val': False,
            'col_name': 'Mutant_nucleotide',
        },
        '{prefix}_codon_no'.format(prefix=prefix): {
            'multi_val': False,
            'col_name': 'Codon_number',
            'wrap': False
        },
        '{prefix}_codon_range'.format(prefix=prefix): {
            'between_op': True,
            'max_val': 394,
            'min_val': 1,
            'start_param': 'codon_start',
            'end_param': 'codon_end',
            'col_name': 'Codon_number',
            'wrap': False
        },
        '{prefix}_wild_codon'.format(prefix=prefix): {
            'multi_val': False,
            'col_name': 'WT_codon'
        },
        '{prefix}_mut_codon'.format(prefix=prefix): {
            'multi_val': False,
            'col_name': 'Mutant_codon'
        },
        '{prefix}_wild_aa'.format(prefix=prefix): {
            'multi_val': False,
            'col_name': 'WT_AA'
        },
        '{prefix}_mut_aa'.format(prefix=prefix): {
            'multi_val': False,
            'col_name': 'Mutant_AA'
        }

    }
    if codon_range:
        del param_col_name_map['{prefix}_codon_no'.format(prefix=prefix)]
    else:
        del param_col_name_map['{prefix}_codon_range'.format(prefix=prefix)]
    return build_criteria(param_col_name_map)


def get_cell_line_criteria(prefix):
    param_col_name_map = {
        'cl_name': {
            'multi_val': False,
            'col_name': 'Sample_Name'
        },
        'atcc_id': {
            'multi_val': False,
            'col_name': 'ATCC_ID'
        },
        'cosmic_id': {
            'multi_val': False,
            'col_name': 'Cosmic_ID',
            'wrap': False
        },
        'tp53_status': {
            'multi_val': True,
            'col_name': 'TP53status'
        },
        '{prefix}_tumor_origin'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Tumor_origin_group'
        },
        '{prefix}_topo_list'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Short_topo'
        },
        '{prefix}_morph_list'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Morphology'
        }
    }

    return build_criteria(param_col_name_map)


def get_tumor_origin_criteria(prefix):
    param_col_name_map = {
        '{prefix}_tumor_origin'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Tumor_origin_group'
        }
    }
    return build_criteria(param_col_name_map)


def get_ref_criteria(prefix):
    param_col_name_map = {
        '{prefix}_refs_list'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Ref_ID',
            'wrap': False
        }
    }

    return build_criteria(param_col_name_map)


def get_topo_morph_criteria(prefix):
    param_col_name_map = {
        '{prefix}_topo_list'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Short_topo'
        },
        '{prefix}_morph_list'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Morphology'
        }
    }

    return build_criteria(param_col_name_map)


def get_method_criteria(prefix):
    param_col_name_map = {
        '{prefix}_start_material'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Start_material'
        }
    }
    criteria = build_criteria(param_col_name_map)
    exon_columns = list_param_val(request, '{prefix}_exon_analyzed'.format(prefix=prefix))
    for exon_col in exon_columns:
        criteria.append({'column_name': exon_col, 'vals': ['TRUE'], 'wrap_with': ''})

    return criteria


def get_variation_criteria(prefix):
    param_col_name_map = {
        '{prefix}_cdna_list'.format(prefix=prefix): {
            'multi_val': True,
            'or_group': 'variation',
            'col_name': 'c_description'
        },
        '{prefix}_p_list'.format(prefix=prefix): {
            'multi_val': True,
            'or_group': 'variation',
            'col_name': 'ProtDescription'
        },
        '{prefix}_hg19_list'.format(prefix=prefix): {
            'multi_val': True,
            'or_group': 'variation',
            'col_name': 'g_description'
        },
        '{prefix}_hg38_list'.format(prefix=prefix): {
            'multi_val': True,
            'or_group': 'variation',
            'col_name': 'g_description_GRCh38'
        }
    }
    return build_criteria(param_col_name_map)


def get_ngs_criteria(prefix):
    param_col_name_map = {
        '{prefix}_ngs'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'WGS_WXS'
        }
    }
    return build_criteria(param_col_name_map)


def get_sample_source_criteria(prefix):
    param_col_name_map = {
        '{prefix}_sample_source'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Sample_source_group'
        }
    }
    return build_criteria(param_col_name_map)


def get_country_criteria(prefix):
    param_col_name_map = {
        '{prefix}_country_list_0'.format(prefix=prefix): {
            'multi_val': True,
            'multi_columns': True,
            'col_name': 'Country'
        },
        '{prefix}_country_list_1'.format(prefix=prefix): {
            'multi_val': True,
            'multi_columns': True,
            'col_name': 'Population'
        },
        '{prefix}_country_list_2'.format(prefix=prefix): {
            'multi_val': True,
            'multi_columns': True,
            'col_name': 'Development'
        },
        '{prefix}_country_list_3'.format(prefix=prefix): {
            'multi_val': True,
            'multi_columns': True,
            'col_name': 'Region'
        }
    }
    return build_criteria(param_col_name_map)


def get_patient_criteria(prefix):
    param_col_name_map = {
        '{prefix}_age_range'.format(prefix=prefix): {
            'between_op': True,
            'max_val': 120,
            'min_val': 0,
            'start_param': '{prefix}_age_start'.format(prefix=prefix),
            'end_param': '{prefix}_age_end'.format(prefix=prefix),
            'col_name': 'Age',
            'wrap': False
        },
        '{prefix}_gender'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Sex'
        },
        '{prefix}_germ_mut'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Germline_mutation'
        },
        '{prefix}_tobacco'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Tobacco_search'
        },
        '{prefix}_alcohol'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Alcohol_search'
        },
        '{prefix}_inf_agnt_list'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Infectious_agent'
        },
        '{prefix}_exposure_list'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Exposure'
        }
    }

    criteria = build_criteria(param_col_name_map)
    return criteria


@app.route("/results_gene_mut_by_gv", methods=['GET', 'POST'])
def results_gene_mut_by_gv():
    prefix = 'gv'
    criteria = get_variation_criteria(prefix)
    return render_template("results_gene_mutation.html", criteria=criteria)

@app.route("/results_gene_mut_by_mutids", methods=['GET', 'POST'])
def results_gene_mut_by_mutids():
    criteria = get_mut_id_criteria()
    return render_template("results_gene_mutation.html", criteria=criteria)

@app.route("/results_gene_mut_by_mut", methods=['GET', 'POST'])
def results_gene_mut_by_mut():
    prefix = 'gmut'
    criteria = get_mutation_criteria(prefix)
    return render_template("results_gene_mutation.html", criteria=criteria)

@app.route("/results_gene_dist", methods=['GET', 'POST'])
def results_gene_dist():

    criteria_map = {
        'include': get_mut_id_criteria(),
        'exclude': []
    }
    action = get_param_val(request, 'action')
    if action == 'get_gv_tumor_dist':
        gv_tumor_dist_tables = {
            'somatic_tumor_dist': 'SomaticView',
            'germline_tumor_dist': 'GermlineView'
        }
        template = 'mutation_stats.html'
        graph_configs = {}
        sql_maps = {}
        graph_configs[action] = build_graph_configs(action)['tumor_dist']
        for dist_table in gv_tumor_dist_tables:
            sql_maps[dist_table] = (build_graph_sqls(graph_configs, criteria_map=criteria_map, table=gv_tumor_dist_tables[dist_table])[action])
        # print(sql_maps)
        # print(graph_configs)
    else:
    # elif action == 'get_mutation_dist':
        table = 'MutationView'
        template = 'mutation_dist_stats.html'
        graph_configs = build_graph_configs(action, table)
        sql_maps = build_graph_sqls(graph_configs, criteria_map=criteria_map, table=table)
    # else:
    #     # action = get_gv_tumor_dist
    #     table1 = 'SomaticView'
    #     table2 = 'GermlineView'
    #     template = 'mutation_stats.html'
    graph_result = build_graph_data(sql_maps)
    print(graph_result)
    return render_template(template, criteria_map=criteria_map, title='Statistics on Gene Variations',
                           graph_result=graph_result)


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


@app.route("/cl_query", methods=['GET', 'POST'])
def cl_query():
    parameters = dict(request.form)
    draw = parameters['draw']
    order_col = int(parameters['order[0][column]'])
    order_dir = parameters['order[0][dir]']
    start = int(parameters['start'])
    length = int(parameters['length'])
    criteria = json.loads(parameters['criteria'])

    column_filters = ["CellLineView_ID", "Sample_Name", "Short_topo", "Morphology", "ATCC_ID", "Cosmic_ID", "depmap_ID",
                      "Sex",
                      "Age", "TP53status", "ExonIntron", "c_description", "ProtDescription", "Pubmed"]
    sql_stm = bq_builder.build_simple_query(criteria=criteria, table='CellLineView', column_filters=column_filters,
                                            ord_column=column_filters[order_col], desc_ord=(order_dir == 'desc'),
                                            start=start, length=length)
    print(sql_stm)
    sql_cnt_stm = bq_builder.build_simple_query(criteria=criteria, table='CellLineView', column_filters=column_filters,
                                                do_counts=True, distinct_col='CellLineView_ID')

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


@app.route("/search_gene_by_var")
def search_gene_by_var():
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


@app.route("/search_gene_by_mut")
def search_gene_by_mut():
    return render_template("search_tp53_gene_by_mut.html", type_list=m_type_list, desc_list=m_desc_list,
                           motif_list=m_motif_list, effect_list=m_effect_list,
                           exon_intron_list=m_exon_intron_list, ta_class_list=m_ta_class_list, sift_list=m_sift_list)


@app.route("/search_somatic_mut")
def search_somatic_mut():
    return render_template("search_somatic_mut.html",

                           cl_start_material_list=sm_start_material_list,
                           country_list=country_list,
                           c_desc_list=sm_c_desc_list,
                           p_desc_list=sm_p_desc_list,
                           g_desc_hg19_list=sm_g_desc_hg19_list,
                           g_desc_hg38_list=sm_g_desc_hg38_list,
                           type_list=sm_type_list,
                           desc_list=sm_desc_list,
                           motif_list=sm_motif_list,
                           exon_intron_list=sm_exon_intron_list,
                           effect_list=sm_effect_list,
                           ta_class_list=sm_ta_class_list,
                           sift_list=sm_sift_list,
                           topo_list=topo_list,
                           morph_list=morph_list,
                           topo_morph_assc=topo_morph_assc,
                           tumor_org_group_list=sm_tumor_org_group_list,
                           sample_source_list=sm_sample_source_list,
                           germ_mut_list=sm_germ_mut_list,
                           inf_agnt_list=sm_inf_agnt_list,
                           exposure_list=sm_exposure_list,

                           )


@app.route("/prognosis_somatic_stats")
def prognosis_somatic_stats():
    return render_template("prognosis_somatic_stats.html")


@app.route("/db_dev_somatic_stats")
def db_dev_somatic_stats():
    return render_template("db_dev_somatic_stats.html")


@app.route("/search_somatic_prevalence")
def search_somatic_prevalence():
    return render_template("search_somatic_prevalence.html",
                           morph_list=morph_list,
                           topo_list=topo_list,
                           topo_morph_assc=topo_morph_assc,
                           cl_start_material_list=sm_start_material_list,
                           country_list=country_list
                           )


@app.route("/stats_somatic_mut")
def stats_somatic_mut():
    return render_template("stats_somatic_mut.html")


@app.route("/prevalence_somatic_stats")
def prevalence_somatic_stats():
    sql_stm = bq_builder.build_mutation_prevalence()
    query_job = bigquery_client.query(sql_stm)
    data = []
    error_msg = None
    graph_data = {}
    try:
        result = query_job.result(timeout=30)
        rows = list(result)
        labels = []
        total_cnt = 0
        for row in rows:
            topo = row.get('Topography')
            anal_cnt = row.get('Sample_analyzed')
            mut_cnt = row.get('Sample_mutated')
            label = "{topo} ({mut_cnt}/{anal_cnt})".format(topo=topo, anal_cnt=anal_cnt, mut_cnt=mut_cnt)
            labels.append(label)
            ratio = mut_cnt * 100 /anal_cnt
            data.append(ratio)
            total_cnt += mut_cnt
        graph_data = {
            'labels': labels,
            'data': data,
            'total': total_cnt
        }

    except BadRequest:
        error_msg = "There was a problem with your search input. Please revise your search criteria and search again."
    except (concurrent.futures.TimeoutError, requests.exceptions.ReadTimeout):
        error_msg = "Sorry, query job has timed out."
    # query_result = {'data': data, 'msg': error_msg}

    return render_template("prevalence_somatic_stats.html", graph_data=graph_data, subject='Tumor Site')


@app.route("/results_somatic_mutation", methods=['GET', 'POST'])
def results_somatic_mutation():
    action = get_param_val(request, 'action')
    template = "mutation_dist_stats.html" if action == 'get_mutation_dist' else "mutation_stats.html"

    if action == 'get_codon_dist':
        table = 'SomaticMutationStats'
    elif action == 'get_tumor_dist':
        table = 'SomaticTumorStats'
    else:
        table = 'SomaticView'

    criteria_map = {}
    if request.method == 'POST':
        criteria_type = ['include', 'exclude']
        for type in criteria_type:
            prefix = 'sm_{type}'.format(type=type)
            criteria_map[type] = get_ref_criteria(prefix)
            criteria_map[type] += get_method_criteria(prefix)
            criteria_map[type] += get_ngs_criteria(prefix)
            criteria_map[type] += get_variation_criteria(prefix)
            criteria_map[type] += get_mutation_criteria(prefix)
            criteria_map[type] += get_topo_morph_criteria(prefix)
            criteria_map[type] += get_tumor_origin_criteria(prefix)
            criteria_map[type] += get_patient_criteria(prefix)
            criteria_map[type] += get_country_criteria(prefix)
            criteria_map[type] += get_sample_source_criteria(prefix)
    graph_configs = build_graph_configs(action, table)
    sql_maps = build_graph_sqls(graph_configs, criteria_map=criteria_map, table=table)
    graph_result = build_graph_data(sql_maps)
    return render_template(template, criteria_map=criteria_map, title='Statistics on Somatic Mutations',
                           graph_result=graph_result)


@app.route("/results_somatic_prevalence", methods=['GET', 'POST'])
def results_somatic_prevalence():
    prefix = 'mut_prev'
    criteria = get_topo_morph_criteria(prefix)
    criteria += get_method_criteria(prefix)
    criteria += get_ngs_criteria(prefix)
    criteria += get_country_criteria(prefix)
    action = get_param_val(request, 'action')
    if action == 'get_country_graph':
        group_by = 'Country'
        subject = 'Country'
    elif action == 'get_topo_graph':
        group_by = 'Short_topo'
        subject = 'Topography'
    else:
        # get_morph_graph
        group_by = 'Morphogroup'
        subject = 'Morphography'
    sql_stm = bq_builder.build_group_sum_graph_query(criteria=criteria, view='PrevalenceView', group_by=group_by)
    print(sql_stm)

    query_job = bigquery_client.query(sql_stm)
    data = []
    error_msg = None
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
            'labels': labels,
            'data': data,
            'total': total_cnt
        }
    except BadRequest:
        error_msg = "There was a problem with your search input. Please revise your search criteria and search again."
    except (concurrent.futures.TimeoutError, requests.exceptions.ReadTimeout):
        error_msg = "Sorry, query job has timed out."
    query_result = {'data': data, 'msg': error_msg}
    return render_template("prevalence_somatic_stats.html", graph_data=graph_data, subject = subject)
    # return render_template("results_somatic_prevalence.html", query_result=query_result)


@app.route("/search_germline_mut")
def search_germline_mut():
    return render_template("search_germline_mut.html",
                           topo_list=topo_list,
                           morph_list=morph_list,
                           topo_morph_assc=topo_morph_assc,
                           c_desc_list=gm_c_desc_list,
                           p_desc_list=gm_p_desc_list,
                           g_desc_hg19_list=gm_g_desc_hg19_list,
                           g_desc_hg38_list=gm_g_desc_hg38_list,
                           type_list=gm_type_list,
                           desc_list=gm_desc_list,
                           motif_list=gm_motif_list,
                           exon_intron_list=gm_exon_intron_list,
                           effect_list=gm_effect_list,
                           ta_class_list=gm_ta_class_list,
                           sift_list=gm_sift_list,
                           family_hist_list=gm_family_hist_list,
                           inh_mode_list=gm_inh_mode_list,
                           family_case_list=gm_family_case_list,
                           country_list=country_list,
                           ref_data=gm_ref_data
                           )


@app.route("/stats_germline_mut")
def stats_germline_mut():
    return render_template("stats_germline_mut.html")


@app.route("/view_germline_prevalence")
def view_germline_prevalence():
    column_filters = ['Diagnosis', 'Cohort', 'Cases_Analyzed', 'Cases_mutated', 'Mutation_prevalence', 'Remark',
                      'PubMed']
    criteria = []
    sql_stm = bq_builder.build_simple_query(criteria=criteria, table='GermlinePrevalence',
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


@app.route("/db_dev_germline_stats")
def db_dev_germline_stats():
    return render_template("db_dev_germline_stats.html")


def get_germline_patient_criteria(prefix):
    param_col_name_map = {
        '{prefix}_age_range'.format(prefix=prefix): {
            'between_op': True,
            'max_val': 120,
            'min_val': 0,
            'start_param': '{prefix}_age_start'.format(prefix=prefix),
            'end_param': '{prefix}_age_end'.format(prefix=prefix),
            'col_name': 'Age',
            'wrap': False
        },
        '{prefix}_gender'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Sex'
        },
        '{prefix}_family_hist_list'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Class'
        },
        '{prefix}_inh_mode_list'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'Mode_of_inheritance'
        },
        '{prefix}_family_case_list'.format(prefix=prefix): {
            'multi_val': True,
            'col_name': 'FamilyCase_group'
        },

    }

    criteria = build_criteria(param_col_name_map)
    return criteria


@app.route("/results_germline_mutation", methods=['GET', 'POST'])
def results_germline_mutation():
    # template = "mutation_stats.html"
    action = get_param_val(request, 'action')
    template = "mutation_dist_stats.html" if action == 'get_mutation_dist' else "mutation_stats.html"
    if action == 'get_codon_dist':
        table = 'GermlineMutationStats'
    elif action == 'get_tumor_dist':
        table = 'GermlineTumorStats'

    else:
        # action == 'get_mutation_dist'
        # or 'get_tumor_dist_view'
        # template = "mutation_dist_stats.html"
        table = 'GermlineView'
    criteria_map = {}
    if request.method == 'POST':
        criteria_type = ['include', 'exclude']
        for type in criteria_type:
            prefix = 'gm_{type}'.format(type=type)
            criteria_map[type] = get_ref_criteria(prefix)
            criteria_map[type] += get_topo_morph_criteria(prefix)
            criteria_map[type] += get_variation_criteria(prefix)
            criteria_map[type] += get_mutation_criteria(prefix)
            criteria_map[type] += get_germline_patient_criteria(prefix)
            criteria_map[type] += get_country_criteria(prefix)
    graph_configs = build_graph_configs(action, table)
    sql_maps = build_graph_sqls(graph_configs, criteria_map, table)
    graph_result = build_graph_data(sql_maps)
    # print(graph_result)
    return render_template(template, criteria_map={}, title='Statistics on Germline Mutations',
                           graph_result=graph_result)

    # return render_template("results_germline_mutation.html", criteria_map=criteria_map, query_result=query_result)

def build_graph_configs(action, table=None):

    if action == 'get_mutation_dist':
        exon_intron_labels = []
        for n in range (1, 12):
            exon_intron_labels.append('{n}-exon'.format(n=n))
            if n == 12:
                break
            exon_intron_labels.append('{n}-intron'.format(n=n))

        # exon_intron_labels.append('11-exon')
        graph_configs = {
            'exon_intron': {
                'query_type': 'group_counts',
                'group_by': 'ExonIntron',
                'include_vals': exon_intron_labels,
                'exclude_vals': ['', 'NA']
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
            'sift_class': {
                'query_type': 'group_counts',
                'group_by': 'SIFTClass',
                'exclude_vals': ['']
            },
            'ta_class': {
                'query_type': 'group_counts',
                'group_by': 'TransactivationClass',
                'exclude_vals': ['NA', '']
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
    # elif action == 'get_gv_tumor_dist':
    #     graph_configs = {
    #         # 'topo_dist': {
    #         'tumor_dist_somatic': {
    #             'query_type': 'group_counts',
    #             'group_by': 'Short_topo'
    #         },
    #         'tumor_dist_germline': {
    #             'query_type': 'group_counts',
    #             'group_by': 'Short_topo'
    #         }
    #     }
    else:
        graph_configs = {
            # 'topo_dist': {
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

        if graph_id == 'mut_pt':
            cri['include'].append(
                {'column_name': 'Effect', 'vals': ["missense", "nonsense", "silent"], 'wrap_with': '"'})
        elif graph_id == 'sift_class' or graph_id == 'ta_class':
            cri['include'].append({'column_name': 'Effect', 'vals': ["missense"], 'wrap_with': '"'})

        # if graph_id == 'ta_class':
        #     cri['exclude'].append({'column_name': 'TransactivationClass', 'vals': ["NA"], 'wrap_with': '"'})
        query_type = graph_configs[graph_id]['query_type']
        if query_type == 'group_sums':
            stm = bq_builder.build_mutation_dist_sum_query(criteria_map=cri, table=table,
                                                           group_by=graph_configs[graph_id]['group_by'],
                                                           sum_col=graph_configs[graph_id]['sum_col'])
        elif query_type == 'codon_counts':
            stm = bq_builder.build_codon_dist_query(column=graph_configs[graph_id]['codon_col'], table=table)
        else:
            # query type: 'group_counts'
            stm = bq_builder.build_mutation_query(criteria_map=cri, table=table, group_by=graph_configs[graph_id]['group_by'])
        sql_maps[graph_id] = stm
    return sql_maps

def build_graph_data(sql_maps):
    query_jobs = {}
    for graph_id in sql_maps:
        print(graph_id)
        print(sql_maps[graph_id])
        job = bigquery_client.query(sql_maps[graph_id])
        query_jobs[graph_id] = job
    graph_data = {}
    error_msg = None
    try:
        for graph_id in query_jobs:
            result = query_jobs[graph_id].result(timeout=30)
            data = []
            total = 0
            rows = list(result)
            labels = []
            for row in rows:
                label = row.get('LABEL')
                labels.append(label)
                cnt = row.get('CNT')
                data.append(cnt)
                total += cnt
            graph_data[graph_id] = {
                'labels': labels,
                'data': data,
                'total': total
            }

    except BadRequest:
        error_msg = "There was a problem with your search input. Please revise your search criteria and search again."
    except (concurrent.futures.TimeoutError, requests.exceptions.ReadTimeout):
        error_msg = "Sorry, query job has timed out."

    graph_result = {'graph_data': graph_data, 'msg': error_msg}
    return graph_result


@app.route("/view_exp_ind_mut")
def view_exp_ind_mut():
    column_filters = ['Exposure', 'g_description_GRCh38', 'c_description', 'ProtDescription', 'Model', 'Clone_ID',
                      'Add_Info', 'PubMed', 'MUT_ID']
    criteria = []
    sql_stm = bq_builder.build_simple_query(criteria=criteria, table='InducedMutationView',
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

    return render_template("view_exp_ind_mut.html", criteria=criteria, query_result=query_result)


@app.route("/view_mouse")
def view_mouse():
    column_filters = ['ModelDescription', 'TumorSites', 'AAchange', 'caMOD_ID', 'PubMed', 'MM_ID']
    sql_stm = bq_builder.build_simple_query(criteria=[], table='MouseModelView', column_filters=column_filters)
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

    return render_template("view_mouse.html", query_result=query_result)


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
    return render_template("search_cell_lines.html",
                           c_desc_list=cl_c_desc_list,
                           p_desc_list=cl_p_desc_list,
                           g_desc_hg19_list=cl_g_desc_hg19_list,
                           g_desc_hg38_list=cl_g_desc_hg38_list,
                           cl_tp53stat_list=cl_tp53stat_list,
                           topo_list=topo_list,
                           morph_list=morph_list,
                           topo_morph_assc=topo_morph_assc,
                           tumor_org_group_list=cl_tumor_org_group_list,
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


@app.route("/stats_cell_lines")
def stats_cell_lines():
    return render_template("stats_cell_lines.html")


@app.route("/cell_lines_mutation_stats", methods=['GET', 'POST'])
def cell_lines_mutation_stats():
    action = get_param_val(request, 'action')
    if action == 'get_mutation_type':
        table = 'CellLineView'
    elif action == 'get_tumor_dist':
        table = 'CellLineSiteStats'
    else:
        # action == 'get_codon_dist'
        table = 'CellLineMutationStats'
    graph_configs = build_graph_configs(action, table)
    sql_maps = build_graph_sqls(graph_configs, {}, table)
    graph_result = build_graph_data(sql_maps)
    return render_template("mutation_stats.html", criteria_map={}, title='Statistics on Cell Line Mutations',
                           graph_result=graph_result)


@app.route("/results_cell_line_mutation", methods=['GET', 'POST'])
def results_cell_line_mutation():
    criteria = []
    if request.method == 'POST':
        mut_id_criteria = get_mut_id_criteria()
        if (len(mut_id_criteria)):
            criteria = mut_id_criteria
        else:
            prefix = 'cl'
            criteria += get_cell_line_criteria(prefix)
            criteria += get_method_criteria(prefix)
            criteria += get_variation_criteria(prefix)
            criteria += get_mutation_criteria(prefix)
            criteria += get_patient_criteria(prefix)
            criteria += get_country_criteria(prefix)
            criteria += get_mut_id_criteria()
    return render_template("results_cell_lines.html", criteria=criteria)


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


def load_topo_morph_assc(json_file):
    topo_morph_map = {}
    try:
        file_path = TP53_STATIC_URL + '/list-files/' + json_file
        data = requests.get(file_path).json()
        for row in data:
            topo = row['Short_topo']
            morph = row['Morphology']
            if topo not in topo_morph_map.keys():
                topo_morph_map[topo] = []
            topo_morph_map[topo].append(morph)
        del data
    except:
        print('Error while loading ' + json_file)
    return topo_morph_map


def load_list(list_file, json=False, limit=None):
    data_list = []

    try:
        file_path = TP53_STATIC_URL + '/list-files/' + list_file
        file_data = requests.get(file_path)

        if json:
            data_list = file_data.json()

        else:
            lines = file_data.text.splitlines()
            if limit:
                lines = lines[0:limit]
            for line in lines:
                data_list.append({'label': line})
    except:
        data_list = []
    return data_list


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

    global topo_list
    if not topo_list:
        topo_list = load_list(TOPO_FILE)

    global morph_list
    if not morph_list:
        morph_list = load_list(MORPH_FILE)
    global country_list
    if not country_list:
        country_list = load_list(COUNTRY_FILE)
    global cl_exposure_list
    if not cl_exposure_list:
        cl_exposure_list = load_list(CL_EXPOSURE_FILE)
    global sm_start_material_list
    if not sm_start_material_list:
        sm_start_material_list = load_list(SM_START_MATERIAL_FILE)
    global sm_c_desc_list
    if not sm_c_desc_list:
        sm_c_desc_list = load_list(SM_C_DESC_FILE)
    global sm_p_desc_list
    if not sm_p_desc_list:
        sm_p_desc_list = load_list(SM_P_DESC_FILE)
    global sm_g_desc_hg19_list
    if not sm_g_desc_hg19_list:
        sm_g_desc_hg19_list = load_list(SM_G_DESC_HG19_FILE)
    global sm_g_desc_hg38_list
    if not sm_g_desc_hg38_list:
        sm_g_desc_hg38_list = load_list(SM_G_DESC_HG38_FILE)
    global sm_type_list
    if not sm_type_list:
        sm_type_list = load_list(SM_TYPE_FILE)
    global sm_desc_list
    if not sm_desc_list:
        sm_desc_list = load_list(SM_DESC_FILE)
    global sm_motif_list
    if not sm_motif_list:
        sm_motif_list = load_list(SM_MOTIF_FILE)
    global sm_exon_intron_list
    if not sm_exon_intron_list:
        sm_exon_intron_list = load_list(SM_EXON_INTRON_FILE)
    global sm_effect_list
    if not sm_effect_list:
        sm_effect_list = load_list(SM_EFFECT_FILE)
    global sm_ta_class_list
    if not sm_ta_class_list:
        sm_ta_class_list = load_list(SM_TA_CLASS_FILE)
    global sm_sift_list
    if not sm_sift_list:
        sm_sift_list = load_list(SM_SIFT_FILE)
    global sm_tumor_org_group_list
    if not sm_tumor_org_group_list:
        sm_tumor_org_group_list = load_list(SM_TUMOR_ORG_GROUP_FILE)
    global sm_sample_source_list
    if not sm_sample_source_list:
        sm_sample_source_list = load_list(SM_SAMPLE_SOURCE_GROUP_FILE)
    global sm_germ_mut_list
    if not sm_germ_mut_list:
        sm_germ_mut_list = load_list(SM_GERM_MUT_FILE)
    global sm_inf_agnt_list
    if not sm_inf_agnt_list:
        sm_inf_agnt_list = load_list(SM_INF_AGNT_FILE)
    global sm_exposure_list
    if not sm_exposure_list:
        sm_exposure_list = load_list(SM_EXPOSURE_FILE)
    global gm_c_desc_list
    if not gm_c_desc_list:
        gm_c_desc_list = load_list(GM_C_DESC_FILE)
    global gm_p_desc_list
    if not gm_p_desc_list:
        gm_p_desc_list = load_list(GM_P_DESC_FILE)
    global gm_g_desc_hg19_list
    if not gm_g_desc_hg19_list:
        gm_g_desc_hg19_list = load_list(GM_G_DESC_HG19_FILE)
    global gm_g_desc_hg38_list
    if not gm_g_desc_hg38_list:
        gm_g_desc_hg38_list = load_list(GM_G_DESC_HG38_FILE)
    global gm_type_list
    if not gm_type_list:
        gm_type_list = load_list(GM_TYPE_FILE)
    global gm_desc_list
    if not gm_desc_list:
        gm_desc_list = load_list(GM_DESC_FILE)
    global gm_motif_list
    if not gm_motif_list:
        gm_motif_list = load_list(GM_MOTIF_FILE)
    global gm_exon_intron_list
    if not gm_exon_intron_list:
        gm_exon_intron_list = load_list(GM_EXON_INTRON_FILE)
    global gm_effect_list
    if not gm_effect_list:
        gm_effect_list = load_list(GM_EFFECT_FILE)
    global gm_ta_class_list
    if not gm_ta_class_list:
        gm_ta_class_list = load_list(GM_TA_CLASS_FILE)
    global gm_sift_list
    if not gm_sift_list:
        gm_sift_list = load_list(GM_SIFT_FILE)
    global gm_family_hist_list
    if not gm_family_hist_list:
        gm_family_hist_list = load_list(GM_FAMILY_HIST_FILE)
    global gm_inh_mode_list
    if not gm_inh_mode_list:
        gm_inh_mode_list = load_list(GM_INH_MODE_FILE)
    global gm_family_case_list
    if not gm_family_case_list:
        gm_family_case_list = load_list(GM_FAMILY_CASE_FILE)
    global topo_morph_assc
    if not topo_morph_assc:
        topo_morph_assc = json.dumps(load_topo_morph_assc(TOPO_MORPH_JSON_FILE))
    global gm_ref_data
    if not gm_ref_data:
        gm_ref_data = load_list(GM_REF_FILE, json=True)
    return


setup_app(app)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        TIER = sys.argv[1]
        if TIER.lower() != 'test' and TIER.lower() != 'prod' and TIER.lower() != 'uat':
            TIER = 'test'  # default DATA SET
        bq_builder.set_project_dataset(proj_id=project_id, d_set=TIER)
    app.run(host='127.0.0.1', port=8080, debug=True)

# Select Topography, Sample_analyzed, Sample_mutated
#         FROM PrevalenceStat
#         Where Sample_analyzed>500
#         order by ((Sample_mutated*100) / Sample_analyzed)";

#
# SELECT     topo.GroupOfOrgan AS Topography, SUM(prevDL.Sample_analyzed) AS Sample_analyzed,
#                       SUM(prevDL.Sample_mutated) AS Sample_mutated
# FROM         `isb-cgc-tp53-dev.P53_data.PrevalenceDownload` as prevDL INNER JOIN
#                       `isb-cgc-tp53-dev.P53_data.Topography_dic` as topo ON prevDL.Topo_code = topo.Topo_code
# WHERE     (topo.GroupOfOrgan IS NOT NULL) AND (prevDL.Exclude_analysis = 0)
# GROUP BY topo.GroupOfOrgan
# ORDER BY SUM(prevDL.Sample_mutated) DESC

# SELECT    s_prev.Prevalence_ID, topo.Topography, s_prev.Topo_code, morph.Morphology,
#                       morph.Morpho_code, s_prev.Sample_analyzed, s_prev.Sample_mutated, country.Population,
#                       country.Country, s_prev.Comment, s_ref.Ref_ID, s_ref.Cross_Ref_ID, s_ref.Title,
#                       s_ref.Authors, s_ref.S_Ref_Year, s_ref.Journal, s_ref.Volume, s_ref.Start_page,
#                       s_ref.End_page, s_ref.PubMed, s_ref.Comment AS Ref_comment, s_ref.Tissue_processing,
#                       s_ref.Start_material, s_ref.Prescreening, s_ref.Material_sequenced, s_ref.exon2,
#                       s_ref.exon3, s_ref.exon4, s_ref.exon5, s_ref.exon6, s_ref.exon7, s_ref.exon8,
#                       s_ref.exon9, s_ref.exon10, s_ref.exon11, s_ref.Exclude_analysis, s_ref.WGS_WXS
# FROM         `isb-cgc-tp53-dev.P53_data.S_PREVALENCE` as s_prev INNER JOIN
# `isb-cgc-tp53-dev.P53_data.S_REFERENCE` as s_ref ON s_prev.Ref_ID = s_ref.Ref_ID INNER JOIN
#                       `isb-cgc-tp53-dev.P53_data.Topography_dic` as topo ON s_prev.Topo_code = topo.Topo_code INNER JOIN
#                       `isb-cgc-tp53-dev.P53_data.Morphology_dic` as morph ON s_prev.Morpho_ID = morph.Morphology_ID INNER JOIN
#                       `isb-cgc-tp53-dev.P53_data.Country_dic` as country ON s_prev.Country_ID = country.Country_ID
# ORDER BY s_ref.Ref_ID


# Select {0}, SUM({1}) as Counter FROM {2} GROUP BY {0} ORDER BY SUM({1}) ASC";
# "SomaticTumorStats", "StatisticGraph"


# SELECT     topo.StatisticGraph, topo.Short_topo, COUNT(topo.Short_topo) AS DatasetRx,
#                       ref.Exclude_analysis
# FROM         `isb-cgc-tp53-dev.P53_data.S_MUTATION` as mut  INNER JOIN
#                       `isb-cgc-tp53-dev.P53_data.S_SAMPLE` as sam ON mut.Sample_ID = sam.Sample_ID INNER JOIN
#                       `isb-cgc-tp53-dev.P53_data.Subtopography_dic` as sub ON sam.Subtopo_ID = sub.Subtopo_ID INNER JOIN
#                       `isb-cgc-tp53-dev.P53_data.Topography_dic` as topo ON sub.Topo_code = topo.Topo_code INNER JOIN
#                       `isb-cgc-tp53-dev.P53_data.S_INDIVIDUAL`as ind ON sam.Individual_ID = ind.Individual_ID INNER JOIN
#                       `isb-cgc-tp53-dev.P53_data.S_REFERENCE` as ref ON ind.Ref_ID = ref.Ref_ID
# WHERE     (ref.Ref_ID <> 2636) AND (ref.Ref_ID <> 2637) AND (ref.Ref_ID <> 2638)
# GROUP BY topo.StatisticGraph, ref.Exclude_analysis, topo.Short_topo
# HAVING      (ref.Exclude_analysis = 0)
# ORDER BY COUNT(topo.Short_topo) DESC


# CellLineMutationStatsView
# SELECT s_mut.Mutation_ID, l.Codon_number, l.hg38_Chr17_coordinates, l.hg19_Chr17_coordinates, e.Effect, t.Type,
#                          m.Description, m.Type_ID, m.Effect_ID, m.Mutant_nucleotide, m.Mutant_codon, s_sam.Sample_source_ID
# FROM            `isb-cgc-tp53-dev.P53_data.MUTATION` as m INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.Location` as l ON m.Location_ID = l.Location_ID INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.Genetic_code` as g ON m.Mutant_codon = g.Codon INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.p53_sequence` as s ON l.Codon_number = s.Codon_number INNER JOIN
#                          ON `isb-cgc-tp53-dev.P53_data.Effect_dic` as e m.Effect_ID = e.Effect_ID INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.Type_dic` as t ON m.Type_ID = t.Type_ID INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.S_MUTATION` as s_mut as ON m.MUT_ID = s_mut.MUT_ID INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.S_SAMPLE` as s_mut ON m.Sample_ID = s_sam.Sample_ID
# WHERE        (s_sam.Sample_source_ID = 4)
# ORDER BY l.Codon_number

# GermlineMutationStatsView
# SELECT        l.Codon_number, gc.Amino_Acid, seq.WT_AA, eff.Effect, t.Type, l.ExonIntron, dbo.MUTATION.Description, g_mut.Family_ID,
#                          m.Type_ID, m.Effect_ID, m.Mutant_nucleotide, m.Mutant_codon, aa.AAchange, m.Polymorphism, m.c_description
# FROM            `isb-cgc-tp53-dev.P53_data.G_P53_MUTATION` as g_mut  INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.MUTATION` as m ON g_mut.MUT_ID = m.MUT_ID INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.Location` as l ON m.Location_ID = l.Location_ID INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.Genetic_code` as gc ON m.Mutant_codon = gc.Codon INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.p53_sequence` as seq ON l.Codon_number = seq.Codon_number INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.Effect_dic` as eff ON m.Effect_ID = eff.Effect_ID INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.Type_dic` as t ON m.Type_ID = t.Type_ID INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.AA_change` as aa ON m.AAchangeID = aa.AAchange_ID
# WHERE        (m.Polymorphism <> N'validated')

# GermlineTumorStatsView
# SELECT topo.StatisticGraphGermline, COUNT(topo.StatisticGraphGermline) AS Count
# FROM            `isb-cgc-tp53-dev.P53_data.G_INDIVIDUAL` as ind INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.G_FAMILY` as fam ON ind.Family_ID = fam.Family_ID INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.G_TUMOR` as tum ON ind.Individual_ID = tum.Individual_ID INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.G_P53_MUTATION` as mut ON fam.Family_ID = mut.Family_ID INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.Subtopography_dic` as sub ON tum.Subtopo_ID = sub.Subtopo_ID INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.Topography_dic` as topo ON sub.Topo_code = topo.Topo_code
# WHERE        (ind.Germline_carrier = N'confirmed' OR
#                          ind.Germline_carrier = N'obligatory') AND (topo.Short_topo IS NOT NULL) AND (fam.Germline_mutation LIKE N'TP53%')
# GROUP BY topo.StatisticGraphGermline
# ORDER BY Count DESC
