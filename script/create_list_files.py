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

CELLLINE_VIEW_TBL = 'CellLineView'
MUTATION_VIEW_TBL = 'MutationView'

columns=['Type']
GCP_NAME='isb-cgc-tp53-dev'
# choose from prod, test, stage
DATA_SET='P53_data'
#DATA_SET=uat
#DATA_SET=prod

for f in ../data/processed/*.TXT
    do
        echo " "
        echo " "
        date
        # rename extension to TXT.4bq
        bn=$(basename ${f} .TXT)
        t=${!bn}
        j=bq_schema/${bn}.TXT.SCHEMA
        # get the up-to-date table schema and store as a json file
        bq show --format=prettyjson --schema $GCP_NAME:$DATA_SET.$t > $j

        bq rm -f $GCP_NAME:$DATA_SET.$t
        bq load --source=CSV --field_delimiter='\t' \
            --quote=''  --allow_jagged_rows \
            $GCP_NAME:$DATA_SET.$t $f $j
        echo " "
        bq show $GCP_NAME:$DATA_SET.$t
    done

bq query \
--destination_table mydataset.mytable \
--use_legacy_sql=false \
'SELECT TransactivationClass FROM `isb-cgc-tp53-dev.P53_data.CellLineView`
WHERE TransactivationClass != '' and TransactivationClass != 'NA'
GROUP BY TransactivationClass
ORDER BY TransactivationClass'