# makesapdb
Produces an SAP-formatted Fasta from GIs, Accessions, scientific names, or taxonomic identifiers




**Key types:**
1. NCBI GenInfo identifiers (GI)
2. NCBI Accession.Version 
3. Scientific name
4. NCBI taxonomic identifier

More information on GI and Accession Numbershttps://www.ncbi.nlm.nih.gov/genbank/sequenceids/


### Installation

python3
git clone gi2tax 
install ete3

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



### Quick Start

Use a single command to convert a Fasta to SAP-compatible Fasta

		bash makesapdb_wrapper.sh -f <original_fasta_file> -o <SAP_fasta_file> -t <key_type>

### Manual Mode

Use GIs to get taxonomic information.

		python3 gi-to-tax/gi2tax.py -d . -i <GI_file> -o <taxon_file> -r "[0-9]*"

Generate SAP-compatible headers

		python3 gi-to-tax/tax2sap.py -i <taxon_file> -o <header_file>

Generate SAP-compatible Fasta

		python3 makesapdb -s <header_file> -f <original_fasta_file> -o <SAP_fasta_file>

		







		
