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

Input Key files are simply a list of keys, one per line. For example, a GI file would look like:

		142343
		423423
		242233

Similarly, a SCINAME file would look like:

		Lutjanus_synagris
		Lutjanus_alexandrei
		Lutjanus_ambiguus

### Quick Start

Use one (wrapper) command to convert a Fasta to SAP-compatible Fasta

Must be in this directory when using the wrapper. It assumes that the various scripts of makesapdb are accessable from this point for simplicity. 

Must supply a key type (GI, SCINAME, or TAXID) and a header type (MINIMAL, NCBI, KEYVALUE)

		bash makesapdb_wrapper.sh -f <original_fasta_file> -o <SAP_fasta_file> -t <key_type> -l <header_type>

### Manual Mode

Does the same as above, but the gi-to-tax command has a wealth of options for more control. 

**Step 1:** Get taxonomic information from a Key Type.

Use GIs to get taxonomic information.

		python3 gi-to-tax/gi2tax.py -d . -i <GI_file> -o <taxon_file> -r "[0-9]*"

**OR** use TAXIDs to get taxonomic information.

		python3 tax2tax.py -i <TAXID_file> -o <taxon_file> -t taxid

**OR** use scientific names (SCINAMEs) to get taxonomic information

		python3 tax2tax.py -i <SCINAME_file> -o <taxon_file> -t sciname

**Step 2:** Generate SAP-compatible headers.

		python3 gi-to-tax/tax2sap.py -i <taxon_file> -o <header_file>

**Step 3:** Generate SAP-compatible Fasta.

		python3 makesapdb -s <header_file> -f <original_fasta_file> -o <SAP_fasta_file>


### Caveats (that I have experienced)

Using these tools, I was able to run SAP with a variety of sequences.
However, SAP expects you to create database from Genbank using its own tools. 
This has been problematic for users working with reference sequences from other databases or collected by the lab and not even in a database.
I ran into a few issues that should be kept in mind. These issues are on the SAP side and outside the scope of this package. 

**SAPs fails on erroneous headers**

If an entry has an incompatable header, SAP will completely abort rather than skip the sequence.
While the tax2sap.py script attempts to ensure valid headers, it is possible that I have not come across every possible failure case. 
For my own use, I modified SAP to skip bad sequences since it can take over an hour of indexing before it finds the bad entry. 
The method was a rough hack, and perhaps such a feature could be implemented more smoothly in the actual SAP code. 

**Very large database files fail**

In the SAP code, a temporary file is created. Afterwords, the reference database is indexed. 
If this database is large (in my case, over 200,000,000 sequences), then the temporary file was gone and the SAP crashed. 
I suppose it was cleaned up by the system since it was not being accessed for some time. This was observed on Ubuntu and Red Hat systems. 
My fix was to simply change the temporary file to a normal file by modifying the SAP code. 

**Multiple uses of the same database**

When you use an offline reference database, SAP creates a directory where it copies and indexes the Fasta file.
This is done even for subsequent uses of the same database, which is a major bottleneck. 
Further, multiple concurrent runs of SAP using that database risk writing to the same file causing havok.
I have not actually verified this behavior, but I believe that it would happen. 
A simple fix would be to check if the folder already exists and skip indexing. 
Browsing the SAP code, it looks like that is actually supposed to happen, but it wasn't working for me. 
Ideally, a user would manually specify if the database should be re-built to handle any changes to the source reference Fasta. 
Even a checksum would be useful since the user would not have to keep track, but has the drawback of needing to compute the checksum each time. 



