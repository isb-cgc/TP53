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
from flask import json
import utils


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
CL_TOBACCO_FILE = 'CL_TOBACCO.TXT.LIST'
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
SM_TOBACCO_FILE = 'SM_TOBACCO.TXT.LIST'
SM_INF_AGNT_FILE = 'SM_INF_AGNT.TXT.LIST'
SM_EXPOSURE_FILE = 'SM_EXPOSURE.TXT.LIST'
SM_REF_FILE = 'SM_REF.json'
EVENT_FILE = 'EVENTS.json'

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


# app = Flask(__name__)

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

global cl_tobacco_list
cl_tobacco_list = None

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
global sm_tobacco_list
sm_tobacco_list = None
global sm_ref_data
sm_ref_data = None

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

global event_list
event_list = None

BQ_GCP=os.environ.get('BQ_GCP', 'isb-cgc-tp53-dev')
BQ_DATASET = os.environ.get('BQ_DATASET', 'P53_data')
GOOGLE_SE_ID = os.environ.get('GOOGLE_SE_ID', 'dab1bee9d7d88fe88')
DATA_VERSION = os.environ.get('DATA_VERSION', 'r20')
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
IS_TEST = os.environ.get('IS_TEST', 'True').lower() == 'true'
TP53_STATIC_URL = os.environ.get('TP53_STATIC_URL', 'https://storage.googleapis.com/tp53-static-files-dev')
SECRET_KEY = os.environ.get('SIGNED_SESSION_COOKIE', 'FALSE_SESSION_COOKIE')

def setup_app(app):
    global m_c_desc_list
    if not m_c_desc_list:
        m_c_desc_list = utils.load_list(M_C_DESC_FILE, TP53_STATIC_URL)

    global m_p_desc_list
    if not m_p_desc_list:
        m_p_desc_list = utils.load_list(M_P_DESC_FILE, TP53_STATIC_URL)

    global m_g_desc_hg19_list
    if not m_g_desc_hg19_list:
        m_g_desc_hg19_list = utils.load_list(M_G_DESC_HG19_FILE, TP53_STATIC_URL)

    global m_g_desc_hg38_list
    if not m_g_desc_hg38_list:
        m_g_desc_hg38_list = utils.load_list(M_G_DESC_HG38_FILE, TP53_STATIC_URL)

    global m_type_list
    if not m_type_list:
        m_type_list = utils.load_list(M_TYPE_FILE, TP53_STATIC_URL)

    global m_desc_list
    if not m_desc_list:
        m_desc_list = utils.load_list(M_DESC_FILE, TP53_STATIC_URL)

    global m_motif_list
    if not m_motif_list:
        m_motif_list = utils.load_list(M_MOTIF_FILE, TP53_STATIC_URL)

    global m_exon_intron_list
    if not m_exon_intron_list:
        m_exon_intron_list = utils.load_list(M_EXON_INTRON_FILE, TP53_STATIC_URL)

    global m_effect_list
    if not m_effect_list:
        m_effect_list = utils.load_list(M_EFFECT_FILE, TP53_STATIC_URL)

    global m_ta_class_list
    if not m_ta_class_list:
        m_ta_class_list = utils.load_list(M_TA_CLASS_FILE, TP53_STATIC_URL)

    global m_sift_list
    if not m_sift_list:
        m_sift_list = utils.load_list(M_SIFT_FILE, TP53_STATIC_URL)

    global cl_c_desc_list
    if not cl_c_desc_list:
        cl_c_desc_list = utils.load_list(CL_C_DESC_FILE, TP53_STATIC_URL)

    global cl_p_desc_list
    if not cl_p_desc_list:
        cl_p_desc_list = utils.load_list(CL_P_DESC_FILE, TP53_STATIC_URL)

    global cl_g_desc_hg19_list
    if not cl_g_desc_hg19_list:
        cl_g_desc_hg19_list = utils.load_list(CL_G_DESC_HG19_FILE, TP53_STATIC_URL)

    global cl_g_desc_hg38_list
    if not cl_g_desc_hg38_list:
        cl_g_desc_hg38_list = utils.load_list(CL_G_DESC_HG38_FILE, TP53_STATIC_URL)

    global cl_tp53stat_list
    if not cl_tp53stat_list:
        cl_tp53stat_list = utils.load_list(CL_TP53STAT_FILE, TP53_STATIC_URL)

    global cl_tumor_org_group_list
    if not cl_tumor_org_group_list:
        cl_tumor_org_group_list = utils.load_list(CL_TUMOR_ORG_GROUP_FILE, TP53_STATIC_URL)

    global cl_desc_list
    if not cl_desc_list:
        cl_desc_list = utils.load_list(CL_DESC_FILE, TP53_STATIC_URL)

    global cl_effect_list
    if not cl_effect_list:
        cl_effect_list = utils.load_list(CL_EFFECT_FILE, TP53_STATIC_URL)

    global cl_motif_list
    if not cl_motif_list:
        cl_motif_list = utils.load_list(CL_MOTIF_FILE, TP53_STATIC_URL)

    global cl_start_material_list
    if not cl_start_material_list:
        cl_start_material_list = utils.load_list(CL_START_MATERIAL_FILE, TP53_STATIC_URL)

    global cl_ta_class_list
    if not cl_ta_class_list:
        cl_ta_class_list = utils.load_list(CL_TA_CLASS_FILE, TP53_STATIC_URL)

    global cl_type_list
    if not cl_type_list:
        cl_type_list = utils.load_list(CL_TYPE_FILE, TP53_STATIC_URL)

    global cl_sift_list
    if not cl_sift_list:
        cl_sift_list = utils.load_list(CL_SIFT_FILE, TP53_STATIC_URL)

    global cl_exon_intron_list
    if not cl_exon_intron_list:
        cl_exon_intron_list = utils.load_list(CL_EXON_INTRON_FILE, TP53_STATIC_URL)

    global cl_germ_mut_list
    if not cl_germ_mut_list:
        cl_germ_mut_list = utils.load_list(CL_GERM_MUT_FILE, TP53_STATIC_URL)

    global cl_tobacco_list
    if not cl_tobacco_list:
        cl_tobacco_list = utils.load_list(CL_TOBACCO_FILE, TP53_STATIC_URL)

    global cl_inf_agnt_list
    if not cl_inf_agnt_list:
        cl_inf_agnt_list = utils.load_list(CL_INF_AGNT_FILE, TP53_STATIC_URL)

    global topo_list
    if not topo_list:
        topo_list = utils.load_list(TOPO_FILE, TP53_STATIC_URL)

    global morph_list
    if not morph_list:
        morph_list = utils.load_list(MORPH_FILE, TP53_STATIC_URL)
    global country_list
    if not country_list:
        country_list = utils.load_list(COUNTRY_FILE, TP53_STATIC_URL)
    global cl_exposure_list
    if not cl_exposure_list:
        cl_exposure_list = utils.load_list(CL_EXPOSURE_FILE, TP53_STATIC_URL)
    global sm_start_material_list
    if not sm_start_material_list:
        sm_start_material_list = utils.load_list(SM_START_MATERIAL_FILE, TP53_STATIC_URL)
    global sm_c_desc_list
    if not sm_c_desc_list:
        sm_c_desc_list = utils.load_list(SM_C_DESC_FILE, TP53_STATIC_URL)
    global sm_p_desc_list
    if not sm_p_desc_list:
        sm_p_desc_list = utils.load_list(SM_P_DESC_FILE, TP53_STATIC_URL)
    global sm_g_desc_hg19_list
    if not sm_g_desc_hg19_list:
        sm_g_desc_hg19_list = utils.load_list(SM_G_DESC_HG19_FILE, TP53_STATIC_URL)
    global sm_g_desc_hg38_list
    if not sm_g_desc_hg38_list:
        sm_g_desc_hg38_list = utils.load_list(SM_G_DESC_HG38_FILE, TP53_STATIC_URL)
    global sm_type_list
    if not sm_type_list:
        sm_type_list = utils.load_list(SM_TYPE_FILE, TP53_STATIC_URL)
    global sm_desc_list
    if not sm_desc_list:
        sm_desc_list = utils.load_list(SM_DESC_FILE, TP53_STATIC_URL)
    global sm_motif_list
    if not sm_motif_list:
        sm_motif_list = utils.load_list(SM_MOTIF_FILE, TP53_STATIC_URL)
    global sm_exon_intron_list
    if not sm_exon_intron_list:
        sm_exon_intron_list = utils.load_list(SM_EXON_INTRON_FILE, TP53_STATIC_URL)
    global sm_effect_list
    if not sm_effect_list:
        sm_effect_list = utils.load_list(SM_EFFECT_FILE, TP53_STATIC_URL)
    global sm_ta_class_list
    if not sm_ta_class_list:
        sm_ta_class_list = utils.load_list(SM_TA_CLASS_FILE, TP53_STATIC_URL)
    global sm_sift_list
    if not sm_sift_list:
        sm_sift_list = utils.load_list(SM_SIFT_FILE, TP53_STATIC_URL)
    global sm_tumor_org_group_list
    if not sm_tumor_org_group_list:
        sm_tumor_org_group_list = utils.load_list(SM_TUMOR_ORG_GROUP_FILE, TP53_STATIC_URL)
    global sm_sample_source_list
    if not sm_sample_source_list:
        sm_sample_source_list = utils.load_list(SM_SAMPLE_SOURCE_GROUP_FILE, TP53_STATIC_URL)
    global sm_germ_mut_list
    if not sm_germ_mut_list:
        sm_germ_mut_list = utils.load_list(SM_GERM_MUT_FILE, TP53_STATIC_URL)
    global sm_tobacco_list
    if not sm_tobacco_list:
        sm_tobacco_list = utils.load_list(SM_TOBACCO_FILE, TP53_STATIC_URL)
    global sm_inf_agnt_list
    if not sm_inf_agnt_list:
        sm_inf_agnt_list = utils.load_list(SM_INF_AGNT_FILE, TP53_STATIC_URL)
    global sm_exposure_list
    if not sm_exposure_list:
        sm_exposure_list = utils.load_list(SM_EXPOSURE_FILE, TP53_STATIC_URL)
    global gm_c_desc_list
    if not gm_c_desc_list:
        gm_c_desc_list = utils.load_list(GM_C_DESC_FILE, TP53_STATIC_URL)
    global gm_p_desc_list
    if not gm_p_desc_list:
        gm_p_desc_list = utils.load_list(GM_P_DESC_FILE, TP53_STATIC_URL)
    global gm_g_desc_hg19_list
    if not gm_g_desc_hg19_list:
        gm_g_desc_hg19_list = utils.load_list(GM_G_DESC_HG19_FILE, TP53_STATIC_URL)
    global gm_g_desc_hg38_list
    if not gm_g_desc_hg38_list:
        gm_g_desc_hg38_list = utils.load_list(GM_G_DESC_HG38_FILE, TP53_STATIC_URL)
    global gm_type_list
    if not gm_type_list:
        gm_type_list = utils.load_list(GM_TYPE_FILE, TP53_STATIC_URL)
    global gm_desc_list
    if not gm_desc_list:
        gm_desc_list = utils.load_list(GM_DESC_FILE, TP53_STATIC_URL)
    global gm_motif_list
    if not gm_motif_list:
        gm_motif_list = utils.load_list(GM_MOTIF_FILE, TP53_STATIC_URL)
    global gm_exon_intron_list
    if not gm_exon_intron_list:
        gm_exon_intron_list = utils.load_list(GM_EXON_INTRON_FILE, TP53_STATIC_URL)
    global gm_effect_list
    if not gm_effect_list:
        gm_effect_list = utils.load_list(GM_EFFECT_FILE, TP53_STATIC_URL)
    global gm_ta_class_list
    if not gm_ta_class_list:
        gm_ta_class_list = utils.load_list(GM_TA_CLASS_FILE, TP53_STATIC_URL)
    global gm_sift_list
    if not gm_sift_list:
        gm_sift_list = utils.load_list(GM_SIFT_FILE, TP53_STATIC_URL)
    global gm_family_hist_list
    if not gm_family_hist_list:
        gm_family_hist_list = utils.load_list(GM_FAMILY_HIST_FILE, TP53_STATIC_URL)
    global gm_inh_mode_list
    if not gm_inh_mode_list:
        gm_inh_mode_list = utils.load_list(GM_INH_MODE_FILE, TP53_STATIC_URL)
    global gm_family_case_list
    if not gm_family_case_list:
        gm_family_case_list = utils.load_list(GM_FAMILY_CASE_FILE, TP53_STATIC_URL)
    global topo_morph_assc
    if not topo_morph_assc:
        topo_morph_assc = json.dumps(utils.load_topo_morph_assc(TOPO_MORPH_JSON_FILE, TP53_STATIC_URL))
    global gm_ref_data
    if not gm_ref_data:
        gm_ref_data = utils.load_list(GM_REF_FILE, TP53_STATIC_URL, json=True)
    global sm_ref_data
    if not sm_ref_data:
        sm_ref_data = utils.load_list(SM_REF_FILE, TP53_STATIC_URL, json=True)
    global event_list
    if not event_list:
        event_list = utils.load_list(EVENT_FILE, TP53_STATIC_URL, json=True)
    return


