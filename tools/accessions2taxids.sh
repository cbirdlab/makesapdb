ACC_LIST=$1

CMD_PREFIX="curl 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id="

CMD_SUFFIX="&rettype=fasta&retmode=xml'  | grep -F 'TSeq_taxid' | sed -e 's/  <TSeq_taxid>//'  -e 's/<\/TSeq_taxid>//'"

while read ACC; do
	echo $CMD_PREFIX""$ACC""$CMD_SUFFIX
done < $ACC_LIST
