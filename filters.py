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

from flask import request


def get_param_val(input_name):
    if request.method == 'POST':
        method_request = request.form
    else:
        method_request = request.args

    return method_request.get(input_name)


def list_param_val(input_name):
    if request.method == 'POST':
        method_request = request.form
    else:
        method_request = request.args
    return method_request.getlist(input_name)


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
        if param_col_name_map[param_key].get('between_op', False):
            between_op = True
            start_param = get_param_val(param_col_name_map[param_key]['start_param'])
            end_param = get_param_val(param_col_name_map[param_key]['end_param'])
            if not start_param and not end_param:
                vals = []
            else:
                vals = [start_param or param_col_name_map[param_key]['min_val'],
                        end_param or param_col_name_map[param_key]['max_val']]
        elif param_col_name_map[param_key]['multi_val']:
            vals = list_param_val(param_name)

        else:
            val = get_param_val(param_name)
            vals = [val] if val else []
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


def get_germline_patient_criteria(prefix):
    param_col_name_map = {
        '{prefix}_affected_only'.format(prefix=prefix): {
            'col_name': 'Unaffected',
            'multi_val': False,
            'wrap': False
        },
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



    if get_param_val('{prefix}_carriers_only'.format(prefix=prefix)):
        param_col_name_map['{prefix}_carrier'.format(prefix=prefix)] = {
            'multi_val': True,
            'col_name': 'Germline_carrier',
        }

    criteria = build_criteria(param_col_name_map)
    return criteria


def get_variant_feature_criteria(prefix):
    chrpos_type = get_param_val('{prefix}_chrpos_type'.format(prefix=prefix)) or 'hg38'
    codon_range = (get_param_val('{prefix}_codon_range'.format(prefix=prefix)) == 'checked')

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
            'max_val': 393,
            'min_val': 0,
            'start_param': '{prefix}_codon_start'.format(prefix=prefix),
            'end_param': '{prefix}_codon_end'.format(prefix=prefix),
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
    exon_columns = list_param_val('{prefix}_exon_analyzed'.format(prefix=prefix))
    for exon_col in exon_columns:
        criteria.append({'column_name': exon_col, 'vals': ['TRUE'], 'wrap_with': ''})

    return criteria


def get_gene_variant_criteria(prefix):
    type_input = get_param_val('type_input')


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
    gv_input_name = '{prefix}_{type_input}_list'.format(prefix=prefix, type_input=(type_input[5:])) if type_input else ''


    if param_col_name_map.get(gv_input_name, None):
        trimmed_map = {gv_input_name: param_col_name_map.get(gv_input_name, None)}
    else:
        trimmed_map = param_col_name_map

    return build_criteria(trimmed_map)


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
