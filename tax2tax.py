import csv
import argparse
import sys
import os
import json
from ete3 import NCBITaxa

program = "tax2tax"
version = "0.1.0"
author = "Evan Krell, Darcy Jones"
date = "17 July 2017"
email = "evan.krell@tamucc.edu"
blurb = (
    "{program}\n"
    "{:<}"
    )
short_blurb = (
    "Get taxonomic lineage from a list of scientific names or NCBI taxonomic IDs"
    ).format(**locals())
license = (
    '{program}-{version}\n'
    '{short_blurb}\n\n'
    'Copyright (C) {date},  {author}'
    '\n\n'
    'This program is free software: you can redistribute it and/or modify '
    'it under the terms of the GNU General Public License as published by '
    'the Free Software Foundation, either version 3 of the License, or '
    '(at your option) any later version.'
    '\n\n'
    'This program is distributed in the hope that it will be useful, '
    'but WITHOUT ANY WARRANTY; without even the implied warranty of '
    'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the '
    'GNU General Public License for more details.'
    '\n\n'
    'You should have received a copy of the GNU General Public License '
    'along with this program. If not, see <http://www.gnu.org/licenses/>.'
    ).format(**locals())


def main (in_file, out_file, in_type, out_filetype):

    ncbi = NCBITaxa()
    records = []
    record = {'taxid':None, 'gi':None,'id':None}

    with open(in_file, 'r') as fh:
        queries = fh.read().splitlines()

    if out_filetype == 'JSON':
                output = open(out_file, 'w')

    queries = [x.replace("_", " ") for x in queries if x]
    try:
        if in_type == "taxid":
            queries = list(ncbi.get_taxid_translator(queries).values())
        taxons = ncbi.get_name_translator(queries)
        record['taxid'] == taxons[queries[0]][0]
    except:
        print ("Unable to read keys.")
        print ("Are you using the right type ('-t') option?")
        print ("Default is 'sciname', but 'taxid' available if using NCBI taxonomics IDs.")
        exit (-1)

    count = 0
    for q in queries:
        record['taxid'] = taxons[q][0]
        record['gi'] = count
        record['id'] = q
        count = count + 1
        record['tax_path'] = []
        lineage = ncbi.get_lineage (record['taxid'])
        lineage_names = ncbi.translate_to_names (lineage)
        lineage_ranks = ncbi.get_rank (lineage)
        lineage.pop()
        lineage.pop(0)
        for l in lineage:
            tax_path_entry = {}
            tax_path_entry['taxid'] = l
            tax_path_entry['rank_name'] = lineage_names[count]
            tax_path_entry['rank'] = lineage_ranks[l]
            lin = ncbi.get_lineage(l)
            tax_path_entry['parent_taxid'] = lin[-2]
            record['tax_path'].append (tax_path_entry)


        if out_file is not None:
            if out_filetype == 'JSON':
                output = open(out_file, 'w')
                output.write(json.dumps(record) + '\n')
        else:
            sys.stdout.write(json.dumps(record) + '\n')

        records.append(record)

    if out_filetype == 'CSV':
        with open (out_file, 'w') as csvfile:
            fieldnames = ['ID', 'GI', 'TAXID']
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
            writer.writeheader ()
            for record in records:
                writer.writerow({'ID': record['id'], 'GI':record['gi'], 'TAXID':record['taxid']})


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-i", "--infile", 
        dest='in_file',
        help=(
            "Path to input file containing scientific names or taxonomic IDS"
            )
        )
    arg_parser.add_argument(
        "-o", "--outfile",
        dest='out_file',
        default = None,
        help=(
            "Path to write output to."
            "Enter '-' for stdout (default)."
            )
        )
    arg_parser.add_argument(
        "-t", "--type",
        dest='in_type',
        default="sciname",
        help=(
            "Type of input entries. Either 'sciname' or 'taxid'"
            )
        )
    arg_parser.add_argument(
        "-f", "--filetype",
        dest='out_filetype',
        default="JSON",
        help=(
            "Type of file. Either 'JSON' or 'CSV'"
            )
        )
    args = arg_parser.parse_args()
    main(**args.__dict__)

