###
# Copyright 2019, ISB
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

import re

# change dataset you want to use
global project_id
project_id = 'isb-cgc-tp53-dev'

global dataset
dataset = 'TP53_data'  # default

global bq_proj_dataset
bq_proj_dataset = "{projectId}.{dataset}".format(projectId=project_id, dataset=dataset)


def set_project_dataset(proj_id='isb-cgc-tp53-dev', d_set='TP53_data'):
    global project_id
    global dataset
    global bq_proj_dataset
    project_id = proj_id
    dataset = d_set

    bq_proj_dataset = "{projectId}.{dataset}".format(projectId=proj_id, dataset=d_set)


# def build_vars_act_query(mut_id):
#     query_temp = """
#         SELECT fv.Loss_of_Function, fv.Conserved_WT_Function, fv.Gain_of_Function,
#           fv.Dominant_Negative_Activity, fv.Temperature_Sensitivity, fv.Cell_lines, fv.PubMed,
#           fv.AAchange_ID
#         FROM {bq_proj_dataset}.FunctionView fv
#         JOIN {bq_proj_dataset}.MutationView mv
#         ON mv.AAchange_ID = fv.AAchange_ID
#         WHERE mv.MUT_ID = {mut_id}
#         GROUP BY fv.Loss_of_Function, fv.Conserved_WT_Function, fv.Gain_of_Function,
#           fv.Dominant_Negative_Activity, fv.Temperature_Sensitivity, fv.Cell_lines, fv.PubMed,
#           fv.AAchange_ID
#         ORDER BY fv.AAchange_ID
#         """
#     query = query_temp.format(bq_proj_dataset=bq_proj_dataset, mut_id=mut_id)
#
#     # simple_query="SELECT AAchange_ID FROM {bq_dataset}.MutationView {where_clause} GROUP BY AAchange_ID"
#     return query
#
#
# def build_mouse_query(mut_id):
#     query_temp = """
#         SELECT mmv.ModelDescription, mmv.TumorSites, mmv.caMOD_ID, mmv.PubMed, mmv.AAchange_ID
#         FROM {bq_proj_dataset}.MouseModelView mmv
#         JOIN {bq_proj_dataset}.MutationView mv
#         ON mv.AAchange_ID = mmv.AAchange_ID
#         WHERE mv.MUT_ID = {mut_id}
#         GROUP BY mmv.ModelDescription, mmv.TumorSites, mmv.caMOD_ID, mmv.PubMed, mmv.AAchange_ID
#         ORDER BY mmv.AAchange_ID
#         """
#
#     query = query_temp.format(bq_proj_dataset=bq_proj_dataset, mut_id=mut_id)
#
#     return query
#
#
# def build_induced_query(mut_id):
#     query_temp = """
#         SELECT imv.Exposure, imv.Model, imv.PubMed, imv.MUT_ID
#         FROM {bq_proj_dataset}.InducedMutationView imv
#         JOIN {bq_proj_dataset}.MutationView mv
#         ON mv.MUT_ID = imv.MUT_ID
#         WHERE mv.MUT_ID = {mut_id}
#         GROUP BY imv.Exposure, imv.Model, imv.PubMed, imv.MUT_ID
#         ORDER BY imv.MUT_ID
#         """
#
#     query = query_temp.format(bq_proj_dataset=bq_proj_dataset, mut_id=mut_id)
#
#     return query


def build_mutation_view_join_query(mut_id, join_table, column_filters, join_column, ord_column):
    query_temp = """
        #standardSQL
        SELECT {columns}
        FROM `{bq_proj_dataset}.{join_table}` tbl
        JOIN `{bq_proj_dataset}.MutationView` mv
        ON mv.{join_column} = tbl.{join_column}
        WHERE mv.MUT_ID = {mut_id}
        GROUP BY {columns}
        ORDER BY tbl.{ord_column}
        """
    columns = ', '.join("tbl.{0}".format(col) for col in column_filters)
    query = query_temp.format(bq_proj_dataset=bq_proj_dataset, mut_id=mut_id, join_table=join_table, columns=columns,
                              join_column=join_column, ord_column=ord_column)

    return query


# SELECT m.MUT_ID, l.hg19_Chr17_coordinates, l.hg38_Chr17_coordinates, l.Context_coding_3, m.g_description,
#                          m.g_description_GRCh38, m.c_description, aa_ch.ProtDescription, m.COSMIClink, e.Exposure, im.Model,
#                          im.Clone_ID, im.Add_Info, ir.IRef_ID, ir.PubMed, im.Induced_ID, l.Genomic_nt
# FROM            `isb-cgc-tp53-dev.P53_data.INDUCED_MUTATIONS` im INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.I_REFERENCE` ir ON im.IRef_ID = ir.IRef_ID INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.MUTATION` m ON im.MUT_ID = m.MUT_ID INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.AA_change` aa_ch ON m.AAchangeID = aa_ch.AAchange_ID INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.Exposure_dic` e ON im.Exposure_ID = e.Exposure_ID INNER JOIN
#                          `isb-cgc-tp53-dev.P53_data.Location` l ON m.Location_ID = l.Location_ID
# ORDER BY e.Exposure


def build_simple_query(criteria, table, column_filters, do_counts=False, distinct_col=None, ord_column=None,
                       desc_ord=False, start=0, length=None):
    # build where clause
    where_clause = 'TRUE'
    for criterion in criteria:
        column_name = criterion.get('column_name')
        vals = criterion.get('vals')
        wrap_with = criterion.get('wrap_with', '')

        op = 'IN' if len(vals) > 1 else '='
        vals_str = ', '.join('{wrap_with}{val}{wrap_with}'.format(val=val, wrap_with=wrap_with) for val in vals)
        where_clause += '\nAND {column_name} {op} ({vals_str})'.format(column_name=column_name, op=op,
                                                                       vals_str=vals_str)

    columns = ', '.join(column_filters)

    order_by_clause = ''
    limit_clause = ''
    if do_counts:
        select_clause = "COUNT(DISTINCT {distinct_col}) as CNT".format(distinct_col=distinct_col)
        group_by = ''
    else:
        select_clause = columns
        group_by = 'GROUP BY {columns}'.format(columns=columns)
        if ord_column:
            ord_dir = "DESC" if desc_ord else ""
            order_by_clause = "ORDER BY {ord_column} {ord_dir}".format(ord_column=ord_column, ord_dir=ord_dir)
        if length:
            limit_clause = "LIMIT {limit_cnt} OFFSET {skip_rows}".format(limit_cnt=length, skip_rows=start)

    query_str = """
            #standardSQL
            SELECT {select_clause}
            FROM `{bq_proj_dataset}.{table}`
            WHERE {where_clause}
            {group_by}
            {order_by_clause}
            {limit_clause}
        """.format(bq_proj_dataset=bq_proj_dataset,
                   select_clause=select_clause,
                   where_clause=where_clause,
                   table=table,
                   group_by=group_by,
                   order_by_clause=order_by_clause,
                   limit_clause=limit_clause
                   )

    return query_str


# tp53 Gene Validated Polymorphism Query
def build_view_val_poly():
    # standardSQL
    # SELECT
    # DISTINCT
    # g_description_GRCh38, ExonIntron, CpG_site, Splice_site, Context_coding_3, WT_codon, Mutant_codon, Effect, EffectGroup3, MUT_ID
    # FROM
    # `{bq_proj_dataset}.MutationView`
    # ORDER
    # BY
    # MUT_ID

    query_str = """
        #standardSQL
        SELECT g_description_GRCh38, c_description, ProtDescription, ExonIntron, Effect,
                    SNPlink, gnomADlink, CLINVARlink, PubMedlink, SourceDatabases
        FROM `{bq_proj_dataset}.MutationView`
        WHERE polymorphism = 'validated'
        GROUP BY g_description_GRCh38, c_description, ProtDescription, ExonIntron, Effect,
                    SNPlink, gnomADlink, CLINVARlink, PubMedlink, SourceDatabases
        ORDER BY g_description_GRCh38
    """.format(bq_proj_dataset=bq_proj_dataset)
    print(query_str)
    return query_str


def do_in(field, list):
    if not list:
        return ""
    temp = []
    for p in list.split(','):
        temp.append("'{p}'".format(p=p))
    return "{field} in ({temp_join})".format(field=field, temp_join=', '.join(temp))


def do_wild_cardable(field, val):
    parts = []
    parts_wc = []
    for p in val.split(','):
        if len(re.findall(r'\%', p)) > 0:
            p = re.sub(r'\%+$', '', p)
            parts_wc.append(p)
        else:
            parts.append(p)
    both = len(parts) > 0 and len(parts_wc) > 0
    stmt = "(" if both else ""
    stmt += do_in(field, ",".join(parts))
    stmt += " OR " if both else ""
    stmt += do_op_list(field, "LIKE", ",".join(parts_wc), 1)
    stmt += ")" if both else ""
    return stmt


# The Mitelman Gene Fusions and Clinical Associations Searcher
# to use Gene Fusions Searcher use op = "M"
# to use Clinical Associations Searcher, use op = "C"
def build_mc_query(
        op=None,
        abnorm_op=None,
        abnormality=None,
        break_op=None,
        breakpoint=None,
        gene_op=None,
        gene=None,
        top=None,
        morph=None,
        immuno=None,
        author=None,
        journal=None,
        year=None,
        refno=None,
        invno=None
):
    # abnorm_op: string, "a" for AND operation, "o" for OR operation for abnormality
    # abnormality: string, can use wild card *, multiple inputs can be provided with comma delimited string (eg 't(19;19)(p13;p13)' or 'del(7)*')
    # author: string, can use wild card * or _, multiple inputs can be provided with comma delimited string (operation is always "AND")
    # break_op: string, "a" for AND operation, "o" for OR operation for breakpoint
    # breakpoint: string, can use wild card *, multiple inputs can be provided with comma delimited string (eg '19p13' or '12q2?3')
    # gene_op: string, "a" for AND operation, "o" for OR operation for gene
    # gene: string, can use wild card *, multiple inputs can be provided with comma delimited string (eg 'KMT2A' or 'BCR/ABL1')
    # immuno: string, 'B' for B Lineage or 'T' for TLineage
    # invno: string, operators "<", ">", and "-" can be used together with the value
    # journal: string, can use wild card *
    # morph: string, morphology code, can use wild card *, multiple inputs can be provided with comma delimited string
    # op: string, search type, "M" for Gene Fusions Searcher "C" for Clinical Associations Searcher
    # refno: string, operators "<", ">", and "-" can be used together with the value (e.g. refno = "<120"  or refno = "34-24")
    # top: string, topology code, can use wild card *, multiple inputs can be provided with comma delimited string
    # year: string, operators "<", ">", and "-" can be used together with the value

    query_str = "#standardSQL"
    query_str += "\nSELECT DISTINCT r.Abbreviation, r.Journal, "
    query_str += "\nc.RefNo, c.InvNo, mk.benamning as MorphName, tk.benamning as TopoName, c.Morph, c.Topo, c.KaryShort, "
    query_str += "\nc.GeneShort, c.Immunology "
    query_str += "\nFROM `{bq_proj_dataset}.MolBiolClinAssoc` c".format(bq_proj_dataset=bq_proj_dataset)
    query_str += "\nLEFT JOIN `{bq_proj_dataset}.Koder` mk".format(bq_proj_dataset=bq_proj_dataset)
    query_str += "\nON (c.Morph = mk.Kod AND mk.Kodtyp = 'MORPH')"
    query_str += "\nLEFT JOIN `{bq_proj_dataset}.Koder` tk".format(bq_proj_dataset=bq_proj_dataset)
    query_str += "\nON (c.Topo = tk.Kod AND tk.Kodtyp = 'TOP')"
    query_str += ",\n`{bq_proj_dataset}.Reference` r".format(bq_proj_dataset=bq_proj_dataset)
    query_str += ",\n`{bq_proj_dataset}.MolClinGene` k".format(bq_proj_dataset=bq_proj_dataset) if gene else ""
    query_str += ",\n`{bq_proj_dataset}.MolClinAbnorm` a".format(bq_proj_dataset=bq_proj_dataset) if abnormality else ""
    query_str += ",\n`{bq_proj_dataset}.MolClinBreak` br".format(bq_proj_dataset=bq_proj_dataset) if breakpoint else ""
    query_str += ",\n`{bq_proj_dataset}.AuthorReference` ar".format(bq_proj_dataset=bq_proj_dataset) if author else ""
    query_str += "\nWHERE"
    query_str += "\nc.Refno = r.Refno"
    query_str += "\nAND c.MolClin = '{op}'".format(op=op)
    ## NOTE: we now have "c.Refno = r.Refno" specified potentially
    ## more than once
    if author and (year or journal):
        query_str += "\nAND r.RefNo = ar.RefNo and c.RefNo = r.RefNo"
    else:
        if author:
            query_str += "\nAND c.RefNo = ar.RefNo"
        if year or journal:
            query_str += "\nAND c.RefNo = r.RefNo"
    if year:
        query_str += "\nAND " + do_range("r.year", year, 1)
    if abnormality:
        query_str += "\nAND c.RefNo = a.RefNo AND c.InvNo = a.InvNo"
        query_str += "\nAND a.MolClin = '{op}'".format(op=op)
    if breakpoint:
        query_str += "\nAND c.RefNo = br.RefNo AND c.InvNo = br.InvNo"
        query_str += "\nAND br.MolClin = '{op}'".format(op=op)
    if gene:
        query_str += "\nAND c.RefNo = k.RefNo AND c.InvNo = k.InvNo"
        query_str += "\nAND k.MolClin = '{op}'".format(op=op)
    if refno:
        query_str += "\nAND " + do_range("c.RefNo", refno, 1)
    if invno:
        query_str += "\nAND " + do_range("c.InvNo", invno, 1)
    if immuno:
        query_str += "\nAND " + do_op_list("c.Immunology", "=", immuno, 0)
    if morph:
        query_str += "\nAND " + do_wild_cardable("c.Morph", morph)
    if top:
        query_str += "\nAND " + do_wild_cardable("c.Topo", top)
    if author:
        authors = fix_author_input(author)
        query_str += "\nAND ( " + do_and_or_pile("AuthorReference", "ar", "Name", "c", authors) + " )"
    if journal:
        journal = journal.lower()
        journal = journal.replace('*', '%')
        journals = journal.split(",")
        query_str += "\nAND ( " + do_and_or_pile("Reference", "r", "Journal", "c", journals) + " )"
    if abnormality:
        abnormality = abnormality.lower()
        abnormality = abnormality.replace('*', '%')
        abnormality = re.sub(r"^ \\'", "", abnormality)
        abnormality = re.sub(r"\\'$", "", abnormality)
        parts = abnormality.split(",")
        query_str += "\nAND ( " + do_and_or_pile("MolClinAbnorm", "a", "Abnormality", abnorm_op, parts) + " )"

    if gene:
        gene = gene.lower()
        gene = gene.replace('*', '%')
        parts = gene.split(",")
        query_str += "\nAND ( " + do_gene_pile("Gene", gene_op, parts) + " )"

    if breakpoint:
        breakpoint = breakpoint.lower()
        breakpoint = breakpoint.replace('*', '%')
        breakpoint = re.sub(r"^ \\'", "", breakpoint)
        breakpoint = re.sub(r"\\'$", "", breakpoint)
        parts = breakpoint.split(",")
        query_str += "\nAND ( " + do_and_or_pile("MolClinBreak", "br", "Breakpoint", break_op, parts) + " )"

    query_str += "\nORDER BY r.Abbreviation, c.Refno, c.Invno"
    return query_str


def split_breakpoint(breakpoint):
    chr_in = None
    arm_in = None
    band_in = None
    if breakpoint:
        if re.search(r'p', breakpoint, re.IGNORECASE):
            chr_in, band_in = re.split(r'p', breakpoint, flags=re.IGNORECASE)
            arm_in = 'p'
            if not band_in or not re.search(r'^\d+$', band_in):
                band_in = None
        elif re.search(r'q', breakpoint, re.IGNORECASE):
            chr_in, band_in = re.split(r'q', breakpoint, flags=re.IGNORECASE)
            arm_in = 'q'
            if not band_in or not re.search(r'^\d+$', band_in):
                band_in = None
        elif re.search(r'\d+', breakpoint):
            chr_in = re.findall(r'\d+', breakpoint)
            arm_in = None
            band_in = None
        elif re.search(r'X', breakpoint, re.IGNORECASE):
            chr_in = 'X'
            arm_in = None
            band_in = None
        elif re.search(r'Y', breakpoint, re.IGNORECASE):
            chr_in = 'Y'
            arm_in = None
            band_in = None
    return chr_in, arm_in, band_in


# The Recurrent Chromosome Aberrations in Cancer: Structural Aberration Search
def structural_ab_search(
        breakpoint=None,
        neopl_key=None,
        tissue_key=None,
        gene_key=None,
        type_key=None):
    # chr_key: string, chromosome key, "All", "", or chromosome key val
    # arm_key: string, arm key, "All", "", or arm key val
    # band_key: string, band key, "All", "", or band key val
    # neopl_key: string, morphology code
    # tissue_key: string, topography code
    # gene_key: string, gene code
    # type_key: string, aberration type, "U" for unbalanced, "B" for balanced
    chr_key, arm_key, band_key = split_breakpoint(breakpoint)

    sql_stm = """
        #standardSQL
        SELECT a.Chromosome, a.Arm, a.Band, a.Abnormality,
        b.Benamning as MorphName, a.Morph, c.Benamning as TopoName, a.Topo, a.TotalCases,
        a.Gene, a.Type 
        FROM `{bq_proj_dataset}.RecurrentData` a
        LEFT JOIN `{bq_proj_dataset}.Koder` b
        ON (a.Morph = b.Kod AND b.Kodtyp = 'MORPH')
        LEFT JOIN `{bq_proj_dataset}.Koder` c
        ON (a.Topo = c.Kod AND c.Kodtyp = 'TOP')
        WHERE TRUE
        """.format(bq_proj_dataset=bq_proj_dataset)

    if chr_key:
        sql_stm += "\nAND a.Chromosome='{chr_key}'".format(chr_key=chr_key)
    if arm_key:
        sql_stm += "\nAND a.Arm='{arm_key}'".format(arm_key=arm_key)
    if band_key:
        sql_stm += "\nAND a.Band='{band_key}'".format(band_key=band_key)
    if neopl_key:
        sql_stm += "\nAND a.Morph LIKE '{neopl_key}%' ".format(neopl_key=neopl_key)
    if tissue_key:
        sql_stm += "\nAND a.Topo LIKE '{tissue_key}%' ".format(tissue_key=tissue_key)
    if gene_key:
        sql_stm += """\nAND (
            a.Gene='{gene_key}' OR
            a.Gene LIKE '{gene_key}/%' OR
            a.Gene LIKE '%,{gene_key}/%' OR
            a.Gene LIKE '%/{gene_key}' OR
            a.Gene LIKE '%/{gene_key},%'
            )""".format(gene_key=gene_key)
    if type_key:
        sql_stm += "\nAND a.Type = '{type_key}' ".format(type_key=type_key)
    sql_stm += "\nORDER BY a.ChrOrder, a.Arm, a.Band, a.Abnormality, b.Benamning"

    return sql_stm


# The Recurrent Chromosome Aberrations in Cancer: by Numerical Aberration Search
def numerical_ab_search(
        chr_key=None,
        neopl_key=None,
        tissue_key=None,
        type_key=None):
    # chr_key: string, chromosome key
    # neopl_key: string, morphology code
    # tissue_key: string topology code
    # type_key: string, "T" for Trisomy, "M" for Monosomy

    sql_stm = """
        #standardSQL
        SELECT a.Abnormality, b.Benamning as MorphName, a.Morph, c.Benamning AS TopoName, a.Topo, a.TotalCases,
          CASE
            WHEN STARTS_WITH(a.Abnormality,'+')
              THEN 'Trisomy'
            WHEN STARTS_WITH(a.Abnormality,'-')
              THEN 'Monosomy'
          END AS Type
        FROM `{bq_proj_dataset}.RecurrentNumData` a
        LEFT JOIN `{bq_proj_dataset}.Koder` b
        ON (a.Morph = b.Kod AND b.Kodtyp = 'MORPH')
        LEFT JOIN `{bq_proj_dataset}.Koder` c
        ON (a.Topo = c.Kod AND c.Kodtyp='TOP')
        WHERE TRUE
        """.format(bq_proj_dataset=bq_proj_dataset)

    if chr_key:
        sql_stm += "\nAND a.Chromosome='{chr_key}'".format(chr_key=chr_key)
    if neopl_key:
        sql_stm += "\nAND a.Morph LIKE '{neopl_key}' ".format(neopl_key=neopl_key)
    if tissue_key:
        sql_stm += "\nAND a.Topo LIKE '{tissue_key}' ".format(tissue_key=tissue_key)
    if type_key:
        if type_key == "T":
            type_str = "+"
        elif type_key == "M":
            type_str = "-"

        if type_str:
            sql_stm += "\nAND a.Abnormality LIKE '{type_str}%' ".format(type_str=type_str)

    sql_stm += "\nORDER BY a.ChrOrder, a.Abnormality, b.Benamning"
    return sql_stm


# Reference Searcher
def build_ref_search(author=None, journal=None, op_i=None, op_m=None, op_c=None, refno=None, year=None):
    # author: string, can use wild card * or _, multiple inputs can be provided with comma delimited string (operation is always "AND")
    # journal: string, can use wild card *
    # op_i: boolean, Reference Group of Individual Cases
    # op_m: boolean, Reference Group of Gene Fusions
    # op_c: boolean, Reference Group of Clinical Association
    # refno: integer, operators "<", ">", and "-" can be used together with the value (e.g. refno = "<120"  or refno = "34-24")
    # year: integer, operators "<", ">", and "-" can be used together with the value

    # TODO: include check_flag to handle special characters

    query_str = "#standardSQL"
    query_str += "\nSELECT DISTINCT r.Abbreviation, r.Journal, r.refno"
    query_str += "\nFROM `{bq_proj_dataset}.Reference` r".format(bq_proj_dataset=bq_proj_dataset)
    query_str += ", `{bq_proj_dataset}.AuthorReference` ar".format(bq_proj_dataset=bq_proj_dataset) if author else ""
    query_str += '\nWHERE TRUE'
    if op_i or op_m or op_c:
        op_list = []
        if op_i:
            op_list.append(
                "\n(EXISTS (SELECT c.refno FROM `{bq_proj_dataset}.CytogenInv` c WHERE c.refno=r.refno))".format(
                    bq_proj_dataset=bq_proj_dataset))
        if op_m:
            op_list.append(
                "\n(EXISTS (SELECT m.refno FROM `{bq_proj_dataset}.MolBiolClinAssoc` m WHERE m.molclin='M' AND m.refno=r.refno))".format(
                    bq_proj_dataset=bq_proj_dataset))
        if op_c:
            op_list.append(
                "\n(EXISTS (SELECT a.refno FROM `{bq_proj_dataset}.MolBiolClinAssoc` a WHERE a.molclin='C' AND a.refno=r.refno))".format(
                    bq_proj_dataset=bq_proj_dataset))
        query_str += '\nAND (' + ' OR '.join(op_list) + ')'

    if author:
        query_str += "\nAND r.RefNo = ar.RefNo"
    if year:
        query_str += "\nAND " + do_range("r.year", year, 1)
    if refno:
        query_str += "\nAND " + do_range("r.RefNo", refno, 1)
    if author:
        authors = fix_author_input(author)
        query_str += "\nAND ( " + do_and_or_pile("AuthorReference", "ar", "Name", "d", authors) + " )"
    if journal:
        journals = journal.lower().split(",")
        query_str += "\nAND ( " + do_and_or_pile("Reference", "r", "Journal", "d", journals) + " )"

    query_str += "\nORDER BY r.Abbreviation, r.Refno"

    return query_str


# Get Case Info
def build_get_case(refno=None, caseno=None):
    query_str = "#standardSQL"
    query_str += "\nSELECT r.Abbreviation, r.Journal, c.RefNo, c.CaseNo, i.KaryShort, i.KaryLong, c.Sex, c.Age," \
                 " rk.Benamning as Race, c.Series, ck.Benamning as Country," \
                 " pmk.Benamning as PrevMorphName, c.PrevMorph, ptk.Benamning as PrevTopoName, c.PrevTopo," \
                 " ptrk.Benamning as PrevTreat, hk.Benamning as HerDis, mk.Benamning as MorphName, c.Morph," \
                 " t.Benamning as Tissue, tk.Benamning as TopoName, c.Topo, c.Immunology"

    query_str += "\nFROM `{bq_proj_dataset}.Cytogen` c".format(bq_proj_dataset=bq_proj_dataset)
    query_str += ",\n`{bq_proj_dataset}.CytogenInv` i".format(bq_proj_dataset=bq_proj_dataset)
    query_str += ",\n`{bq_proj_dataset}.Reference` r".format(bq_proj_dataset=bq_proj_dataset)
    query_str += "\nLEFT JOIN `{bq_proj_dataset}.Koder` rk ON (c.Race = rk.Kod AND rk.KodTyp = 'RACE')".format(
        bq_proj_dataset=bq_proj_dataset)
    query_str += "\nLEFT JOIN `{bq_proj_dataset}.Koder` ck ON (c.Country = ck.Kod AND ck.KodTyp = 'GEO')".format(
        bq_proj_dataset=bq_proj_dataset)
    query_str += "\nLEFT JOIN `{bq_proj_dataset}.Koder` pmk ON (c.PrevMorph = pmk.Kod AND pmk.KodTyp = 'MORPH')".format(
        bq_proj_dataset=bq_proj_dataset)
    query_str += "\nLEFT JOIN `{bq_proj_dataset}.Koder` ptk ON (c.PrevTopo = ptk.Kod AND ptk.KodTyp = 'TOP')".format(
        bq_proj_dataset=bq_proj_dataset)
    query_str += "\nLEFT JOIN `{bq_proj_dataset}.Koder` ptrk ON (c.PrevTreat = ptrk.Kod AND ptrk.KodTyp = 'TREAT')".format(
        bq_proj_dataset=bq_proj_dataset)
    query_str += "\nLEFT JOIN `{bq_proj_dataset}.Koder` hk ON (c.HerDis = hk.Kod AND hk.KodTyp = 'HER')".format(
        bq_proj_dataset=bq_proj_dataset)
    query_str += "\nLEFT JOIN `{bq_proj_dataset}.Koder` mk ON (c.Morph = mk.Kod AND mk.KodTyp = 'MORPH')".format(
        bq_proj_dataset=bq_proj_dataset)
    query_str += "\nLEFT JOIN `{bq_proj_dataset}.Koder` tk ON (c.Topo = tk.Kod AND tk.KodTyp = 'TOP')".format(
        bq_proj_dataset=bq_proj_dataset)
    query_str += "\nLEFT JOIN `{bq_proj_dataset}.Koder` t ON (i.Tissue = t.Kod AND t.KodTyp = 'TISSUE')".format(
        bq_proj_dataset=bq_proj_dataset)
    query_str += "\nWHERE c.RefNo = {refno}".format(refno=refno)
    query_str += "\nAND c.RefNo = i.RefNo AND c.CaseNo = i.CaseNo"
    query_str += "\nAND c.RefNo = r.RefNo"
    query_str += "\nAND c.CaseNo = '{caseno}'".format(caseno=caseno)
    return query_str


# Get Reference Info
def build_get_ref(refno=None):
    query_str = "#standardSQL"
    query_str += "\nSELECT r.RefNo, r.TitleShort, r.Volume, r.Year, r.Journal, r.Pubmed "
    query_str += "\n, m.MolClin as Mol, c.MolClin as Clin, COUNT(DISTINCT a.CaseNo) as Cas"
    query_str += "\n, ARRAY(SELECT NAME FROM `{bq_proj_dataset}.AuthorReference` ar WHERE ar.RefNo = {refno} ORDER BY ar.NameOrder) AS Name".format(
        bq_proj_dataset=bq_proj_dataset, refno=refno)
    query_str += "\nFROM `{bq_proj_dataset}.Reference` r".format(bq_proj_dataset=bq_proj_dataset)
    query_str += "\nLEFT JOIN `{bq_proj_dataset}.Cytogen` a ON r.RefNo = a.RefNo".format(
        bq_proj_dataset=bq_proj_dataset)
    query_str += "\nLEFT JOIN `{bq_proj_dataset}.MolBiolClinAssoc` m ON r.RefNo = m.RefNo AND m.MolClin = 'M'".format(
        bq_proj_dataset=bq_proj_dataset)
    query_str += "\nLEFT JOIN `{bq_proj_dataset}.MolBiolClinAssoc` c ON r.RefNo = c.RefNo AND c.MolClin = 'C'".format(
        bq_proj_dataset=bq_proj_dataset)
    query_str += '\nWHERE r.RefNo = {refno}'.format(refno=refno)
    query_str += '\nGROUP BY r.RefNo, r.TitleShort, r.Volume, r.Year, r.Journal, r.Pubmed, Mol, Clin'
    return query_str


def do_range(field, val, is_numeric):
    quote = "" if is_numeric else "'"
    val = val.replace(" ", "")
    match = re.findall(r"^([<>])(.+)", val)
    if len(match) > 0:
        (op, val) = match[0]
        return "{field} {op} {quote}{val}{quote}".format(field=field, op=op, quote=quote, val=val)
    elif re.findall(r"-", val):
        (lo, hi) = val.split('-')
        return "{field} BETWEEN {quote}{lo}{quote} AND {quote}{hi}{quote}".format(field=field, quote=quote, lo=lo,
                                                                                  hi=hi)
    else:
        return "{field} = {quote}{val}{quote}".format(field=field, val=val, quote=quote)


def fix_author_input(auth_str):
    auth_str = auth_str.lower()  # $string =~ tr/A-Z/a-z/;
    auth_str = auth_str.replace("*", "%")  # $string =~ tr/*'/%_/ #TODO: replace * to % ?
    auth_str = auth_str.replace("'", "_")
    authors = auth_str.split(",")
    fixed_authors = []
    for auth in authors:
        auth = auth.strip()
        auth = ' '.join(auth.split())
        if not re.findall(r" ", auth):
            auth += ' %'
        fixed_authors.append(auth)
    return fixed_authors


def parse_term(part):
    match_list = re.findall(r'\"([^\"]*)\"', part)
    if len(match_list) > 0:
        return '=', match_list[0]
    else:
        return 'LIKE', part


def do_op_list(field, op, val, is_numeric):
    if not val:
        return ""
    ## pre_wc is here only for PrevTreat, which, regrettably, may
    ## have multiple, comma-separated single-character treatment
    ## values
    pre_wc = "%" if op == "LIKE" and not is_numeric else ""
    post_wc = "%" if op == "LIKE" else ""
    quote = "'" if post_wc == "%" else ("" if is_numeric else "'")
    vals = val.split(",")  # split ",", $val;
    return \
        ("(" if len(vals) > 1 else "") + \
        "{field} {op} {quote}{pre_wc}".format(field=field, op=op, quote=quote, pre_wc=pre_wc) + \
        ("{post_wc}{quote} OR {field} {op} {quote}{pre_wc}".format(post_wc=post_wc, quote=quote, field=field, op=op,
                                                                   pre_wc=pre_wc)).join(vals) + \
        "{post_wc}{quote}".format(post_wc=post_wc, quote=quote) + \
        (")" if len(vals) > 1 else "")


def do_and_or_pile(table, var, field, log_op, parts):
    negative_terms = []
    positive_terms = []
    stmt = ''
    for i in parts:
        i = re.sub(r"^ +", "", i)
        i = re.sub(r" +$", "", i)
        match = re.findall(r"^(not +)(.*)", i, re.IGNORECASE)
        if len(match) > 0:
            op, term = match[0]
            negative_terms.append(term)
        else:
            positive_terms.append(i)

    if len(positive_terms) > 0:
        op, term = parse_term(positive_terms[0])
        wc = "%" if op == "LIKE" else ""
        if wc and 'http' not in term:
            sub_term = term.split("/")
        else:
            sub_term = [term]
        stmt += "("
        for indx, s_term in enumerate(sub_term):
            stmt += "\nOR " if indx > 0 else ""
            if log_op == "n":
                stmt += "\nLOWER({var}.{field}) {op} \"{s_term}\" ".format(var=var, field=field, op=op, s_term=s_term)
            else:
                stmt += "\nLOWER({var}.{field}) {op} \"{s_term}{wc}\" ".format(var=var, field=field, op=op,
                                                                               s_term=s_term, wc=wc)
            stmt += ")"

        for i in range(1, len(positive_terms)):
            op, term = parse_term(positive_terms[i])
            wc = '%' if op == 'LIKE' else ''
            if log_op == 'a':
                stmt += "\nAND EXISTS"
                stmt += "\n( SELECT {field} FROM `{bq_proj_dataset}.{table}` {var}{i} ".format(field=field,
                                                                                               bq_proj_dataset=bq_proj_dataset,
                                                                                               table=table, var=var,
                                                                                               i=i)
                stmt += "\nWHERE c.RefNo = {var}{i}.RefNo AND ".format(var=var, i=i)
                stmt += "\n c.CaseNo = {var}{i}.CaseNo AND ".format(var=var, i=i) if table != 'MolClinAbnorm' else ""
                stmt += "\n c.InvNo = {var}{i}.InvNo AND (".format(var=var, i=i)
                sub_term = term.split("/")
                for indx, s_term in enumerate(sub_term):
                    stmt += "\nOR " if indx > 0 else ""
                    stmt += "\nLOWER({var}{i}.{field}) {op} \"{s_term}{wc}\" ".format(var=var, i=i, field=field,
                                                                                      op=op, s_term=s_term, wc=wc)
                stmt += "\n))"

            # log_op = c represents the "and" case for reference associated vars
            elif log_op == "c":
                stmt += """\nAND EXISTS
                    ( SELECT {field} FROM `{bq_proj_dataset}.{table}` {var}{i} 
                    WHERE c.RefNo = {var}{i}.RefNo AND 
                    LOWER({var}{i}.{field}) {op} \"{term}{wc}\" )""".format(field=field,
                                                                            bq_proj_dataset=bq_proj_dataset,
                                                                            table=table, var=var, i=i, op=op,
                                                                            wc=wc, term=term)
            # log_op = d represents the "and" case for reference search
            elif log_op == 'd':
                stmt += """\nAND EXISTS
                    ( SELECT {field} FROM  `{bq_proj_dataset}.{table}` {var}{i}
                        WHERE r.RefNo = {var}{i}.RefNo AND
                        LOWER({var}{i}.{field}) {op} \"{term}{wc}\" ) """.format(field=field,
                                                                                 bq_proj_dataset=bq_proj_dataset,
                                                                                 table=table, var=var, i=i, term=term,
                                                                                 op=op, wc=wc)

            # log_op = o represents the general "or" case
            elif log_op == 'o':
                stmt += "\nOR LOWER({var}.{field}) {op} \"{term}{wc}\" ".format(var=var, field=field, op=op, term=term,
                                                                                wc=wc)

            # log_op = n represents the general "or" case and no wildcards
            elif log_op == 'n':
                stmt += "\nOR LOWER({var}.{field}) {op} \"{term}\" ".format(var=var, field=field, op=op, term=term)
            else:
                print("illegal logical operator\n")

    positive_terms_len = len(positive_terms)

    if len(negative_terms) > 0:
        stmt += " AND " if stmt else ""
        stmt += "NOT EXISTS "
        stmt += "\n( SELECT {field} FROM `{bq_proj_dataset}.{table}` {var}{i} ".format(field=field,
                                                                                       bq_proj_dataset=bq_proj_dataset,
                                                                                       table=table, var=var,
                                                                                       i=positive_terms_len)
        stmt += "\nWHERE c.RefNo = {var}{i}.RefNo AND ".format(var=var, i=positive_terms_len)
        stmt += "\nc.CaseNo = {var}{i}.CaseNo AND ".format(var=var,
                                                           i=positive_terms_len) if table != 'MolClinAbnorm' else ""
        stmt += "\nc.InvNo = {var}{i}.InvNo AND ( ".format(var=var, i=positive_terms_len)
        or_stmt_list = []
        for j in range(len(negative_terms)):
            (op, term) = parse_term(negative_terms[j])
            wc = "%" if op == "LIKE" else ""
            or_stmt_list.append(
                "LOWER({var}{i}.{field}) {op} \"{term}{wc}\" ".format(var=var, i=positive_terms_len, field=field, op=op,
                                                                      term=term, wc=wc))
        stmt += 'OR '.join(or_stmt_list)
        stmt += "))"
    return stmt


def do_gene_pile(field, log_op, parts):
    positive_terms = []
    negative_terms = []
    temp = []
    stmt = ""

    for i in parts:
        i = re.sub(r'^ +', '', i)
        i = re.sub(r' +$', '', i)
        match = re.findall(r"^(not +)(.*)", i, re.IGNORECASE)
        if len(match) > 0:
            op, term = match[0]
            negative_terms.append(term)
        else:
            positive_terms.append(i)
    if len(positive_terms) > 0:
        match = re.findall(r"(\+|-)*([^+-]+)(\+|-)*", positive_terms[0])
        prefix, gene, suffix = match[0]
        gene = gene.upper()
        if prefix:
            stmt = "k.prefix = '{prefix}' AND ".format(prefix=prefix)
        stmt += "\nk.gene LIKE '{gene}'".format(gene=gene)
        if suffix:
            stmt += "\nAND k.suffix = '{suffix}'".format(suffix=suffix)
        positive_terms_len = len(positive_terms)
        for i in range(1, positive_terms_len):
            match = re.findall(r"(\+|-)*([^+-]+)(\+|-)*", positive_terms[i])
            prefix, gene, suffix = match[0]
            gene = gene.upper()
            if log_op == "a":
                stmt += "\nAND EXISTS "
                stmt += "\n( SELECT {field} FROM `{bq_proj_dataset}.MolClinGene` k{i} ".format(field=field,
                                                                                               bq_proj_dataset=bq_proj_dataset,
                                                                                               i=i)
                stmt += "\nWHERE c.RefNo = k{i}.RefNo AND ".format(i=i)
                stmt += "\nc.InvNo = k{i}.InvNo AND ".format(i=i)
                stmt += "\nc.MolClin = k{i}.MolClin AND ".format(i=i)
                if prefix:
                    stmt += "\nk{i}.prefix = '{prefix}' AND ".format(i=i, prefix=prefix)
                stmt += "\nk{i}.gene LIKE '{gene}'".format(i=i, gene=gene)
                if suffix:
                    stmt += "\nAND k{i}.suffix = '{suffix}'".format(i=i, suffix=suffix)
                stmt += ")"
            elif log_op == "o":
                stmt += "\nOR EXISTS "
                stmt += "\n( SELECT {field} FROM `{bq_proj_dataset}.MolClinGene` k{i} ".format(field=field,
                                                                                               bq_proj_dataset=bq_proj_dataset,
                                                                                               i=i)
                stmt += "\nWHERE c.RefNo = k{i}.RefNo AND ".format(i=i)
                stmt += "\nc.InvNo = k{i}.InvNo AND ".format(i=i)
                stmt += "\nc.MolClin = k{i}.MolClin AND ".format(i=i)
                if prefix:
                    stmt += "\nk{i}.prefix = '{prefix}' AND ".format(i=i, prefix=prefix)
                stmt += "\nk{i}.gene LIKE '{gene}'".format(i=i, gene=gene)
                if suffix:
                    stmt += "\nAND k{i}.suffix = '{suffix}'".format(i=i, suffix=suffix)
                stmt += ")"
    if len(negative_terms) > 0:
        stmt += "\n AND " if stmt else ""
        stmt += "NOT EXISTS "
        stmt += "\n( SELECT {field} FROM `{bq_proj_dataset}.MolClinGene` k{i} ".format(field=field,
                                                                                       bq_proj_dataset=bq_proj_dataset,
                                                                                       i=i)
        stmt += "\nWHERE c.RefNo = k{i}.RefNo AND ".format(i=i)
        stmt += "\nc.MolClin = k{i}.MolClin AND ".format(i=i)
        stmt += "\nc.InvNo = k{i}.InvNo AND ( ".format(i=i)

        for j in range(len(negative_terms)):
            match = re.findall(r"(\+|-)*([^+-]+)(\+|-)*", negative_terms[j])
            prefix, gene, suffix = match[0]
            gene = gene.upper()
            t = "("
            if prefix:
                t += "\nk{i}.prefix = '{prefix}' AND ".format(i=positive_terms_len, prefix=prefix)
            t += "\nk{i}.gene LIKE '{gene}'".format(i=positive_terms_len, gene=gene)
            if suffix:
                t += "\nAND k{i}.suffix = '{suffix}'".format(i=i, suffix=suffix)
            t += ")"
            temp.append(t)
        stmt += "\nOR ".join(temp)
        stmt += " ) )"
    return stmt
