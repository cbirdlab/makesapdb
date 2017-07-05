#!/usr/bin/python3

# Replace the sequence headers of a FASTA with SAP-formatted headers

import sys
import os
import argparse
import json
import re
from Bio import SeqIO



def main (fasta_file, header_file, output_fasta, key_type):
    
    if fasta_file is None or header_file is None:
        sys.stderr.write ("error: Both the '-f' and 's' arguments are required")
        exit (-1)

    fasta = open (fasta_file)
    print ("Indexing FASTA..")
    fasta_dict = SeqIO.to_dict (SeqIO.parse(fasta, "fasta"))

    with open(header_file) as h:
        headers = h.read().splitlines()

    print (headers)

    gisNotFound = []
    output = open (output_fasta, 'w')

    print ("Building SAP-formatted FASTA")
    for header in headers:
        try:
            if (key_type == "GI" or key_type == "TAXID"):
                gi = re.search('^>[0-9]*|', header).group(0).replace ('>', '')
            elif (key_type == "SCINAME"):
                gi = re.search("; [^;]*$", header).group(0).replace ('; ', '').replace ("']", '').replace (" ", "_")
            entry = fasta_dict[gi]
            output.write (header + '\n')
            output.write (str (entry.seq) + '\n')
        except Exception:
            gisNotFound.append (gi)

    output.close () 

    print ("The following GIs were not found:")
    for gi in gisNotFound:
        print (gi)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser ()
    arg_parser.add_argument(
        "-f", "--fasta",
        dest='fasta_file',
        help=(
            "Path to fasta file whose headers are to be replaced"
            )
        )
    arg_parser.add_argument(
        "-s", "--sap_headers",
        dest='header_file',
        help=(
            "Path to headers file whose lines are SAP-formatted sequence headers"
            )
        )
    arg_parser.add_argument(
        "-o", "--output_fasta",
        dest='output_fasta',
        help=(
            "Path to output file to write SAP-formatted FASTA to"
            )
        )
    arg_parser.add_argument(
        "-k", "--key_type",
        dest='key_type',
        help=(
            "Type of key to use for matching up SAP headers and minimal Fasta."
            "Options: 'GI', 'SCINAME', 'TAXID'"
            )
        )
    args = arg_parser.parse_args()
    main (**args.__dict__)
