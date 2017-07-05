# makesapdb
Produces an SAP-formatted Fasta from GIs, Accessions, scientific names, or taxonomic identifiers

Thanks to Darcy Jones (https://github.com/darcyabjones) for gi-2-tax package, which this package uses. 

**Key types:**
1. NCBI GenInfo identifiers (GI)
2. NCBI Accession.Version (Coming Soon)
3. Scientific name
4. NCBI taxonomic identifier

More information on GI and Accession Numbers: https://www.ncbi.nlm.nih.gov/genbank/sequenceids/


### Requirements

python3, python3-ete3

### Installation


		git clone https://github.com/ekrell/makesapdb.git
		cd makesapdb
		git clone https://github.com/darcyabjones/gi-to-tax.git
		
		wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/gi_taxid_nucl.dmp.gz
		wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/gi_taxid_nucl.dmp.gz.md5
		md5sum -c gi_taxid_nucl.dmp.gz.md5
		gunzip gi_taxid_nucl.dmp.gz

		wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/gi_taxid_prot.dmp.gz
		wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/gi_taxid_prot.dmp.gz.md5
		md5sum -c gi_taxid_prot.dmp.gz.md5
		gunzip gi_taxid_prot.dmp.gz

		wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
		wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz.md5
		md5sum -c taxdump.tar.gz.md5
		tar -zxf taxdump.tar.gz


### File Preparation

Input Fasta must be such that each sequence header is just the key. 

Example (Scientific name):

		>B.taurus
		CAAAAACATCGCCTCTTGCAAAATCAATGAATAAGAGGTCCCGCCTGCCCTGTGACTATAAGTTTAACGG
		CCGCGGTATTTTGACCGTGCGAAGGTAGCGCAATCACTTGTCTTTTAAATGGAGACCTGTATGAATGGCA

Example (GI):

		>123
		CAAAAACATCGCCTCTTGCAAAATCAATGAATAAGAGGTCCCGCCTGCCCTGTGACTATAAGTTTAACGG
		CCGCGGTATTTTGACCGTGCGAAGGTAGCGCAATCACTTGTCTTTTAAATGGAGACCTGTATGAATGGCA


### Quick Start

Use one (wrapper) command to convert a Fasta to SAP-compatible Fasta

Must be in this directory when using the wrapper. It assumes that the various scripts of makesapdb are accessable from this point for simplicity. 

Must supply a key type (GI, SCINAME, or TAXID) and a header type (MINIMAL, NCBI, KEYVALUE)

		bash makesapdb_wrapper.sh -f <original_fasta_file> -o <SAP_fasta_file> -t <key_type> -l <header_type>

### Manual Mode

Does the same as above, but the gi-to-tax command has a wealth of options for more control. 


Use GIs to get taxonomic information.

		python3 gi-to-tax/gi2tax.py -d . -i <GI_file> -o <taxon_file> -r "[0-9]*"

Generate SAP-compatible headers

		python3 gi-to-tax/tax2sap.py -i <taxon_file> -o <header_file>

Generate SAP-compatible Fasta

		python3 makesapdb -s <header_file> -f <original_fasta_file> -o <SAP_fasta_file>


