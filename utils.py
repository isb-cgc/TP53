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

# import os
# from flask import Flask, render_template, request, send_from_directory, json, jsonify, make_response
# from google.cloud import bigquery
# from google.api_core.exceptions import BadRequest
# import concurrent.futures
import requests
# import sys
# import copy
import csv
# from io import StringIO


def load_topo_morph_assc(json_file, base_url):
    topo_morph_map = {}
    try:
        file_path = base_url + '/list-files/' + json_file
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

def load_list(list_file, base_url, json=False, limit=None):
    data_list = []

    try:
        file_path = base_url + '/list-files/' + list_file
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

def load_csv_file(base_url, list_file):
    column_list = []

    try:
        file_path = base_url + '/data/' + list_file
        file_data = requests.get(file_path)
        lines = file_data.text.splitlines()
        reader = csv.reader(lines, delimiter=',')
        column_list = next(reader)
        data_list = list(reader)
        for row in data_list:
            row.insert(0, '')
    except:
        data_list = []
    return column_list, data_list