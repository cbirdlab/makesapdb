#!/usr/bin/python3

import csv
import argparse
import sys
import os
import json
from ete3 import NCBITaxa

program = "tax2tax"
version = "0.1.0"
author = "Evan Krell"
date = "23 June 2017"
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


def main (in_file, out_file, in_type):

    ncbi = NCBITaxa()
    record = {}

    output = None
    if out_file is not None:
        output = open(out_file, 'w')

    with open(in_file, 'r') as fh:
        queries = fh.read().splitlines()

    queries = [x.replace ("_", " ") for x in queries if x]
    print (queries)
    try:
        if in_type == "taxid":
            queries = list(ncbi.get_taxid_translator(queries).values())
        taxons = ncbi.get_name_translator(queries)
    except:
        print ("Unable to read keys.")
        print ("Are you using the right type ('-t') option?")
        print ("Default is 'sciname', but 'taxid' available if using NCBI taxonomics IDs.")
        exit (1)

    count = 0
    for q in queries:
        try:
            record['taxid'] = taxons[q][0]
            if (in_type == "taxid"):
                record['gi'] = record['taxid']
            else:
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
            if output is not None:
                output.write(json.dumps(record) + '\n')
            else:
                sys.stdout.write(json.dumps(record) + '\n')
        except:
            pass


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
    args = arg_parser.parse_args()
    main(**args.__dict__)

