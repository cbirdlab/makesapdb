# This script handles the generation of SAP-comptable Fasta files that
# can be used as reference database

# Parse arguments
OPTIND=1 # Wipe existing opts

# Init variables
input_fasta=""      # i
output_fasta=""     # o
taxon_db=""         # t
key_type=""         # k
header_type=""      # l

while getopts "hi:o:t:k:l:" opt; do
	case "$opt" in
	h)	echo "Check https://github.com/ekrell/makesapdb"
		exit 0
		;;
	i) 	input_fasta=$OPTARG
		;;
	o) 	output_fasta=$OPTARG
		;;
	t) 	taxon_db=$OPTARG
		;;
	k) 	key_type=$OPTARG
		;;
	l) 	header_type=$OPTARG
		;;
	esac
done

shift $((OPTIND))
[ "$1" = "--" ] && shift

echo "input_fasta=$input_fasta, output_fasta=$output_fasta, taxon_db=$taxon_db, key_type=$key_type, header_type=$header_type"

# Validate arguments

errcount=0

if [ "$input_fasta" == "" ]; then
	echo "Must supply input fasta with -i option"
	errcount=$((errcount+1))
fi

if [ "$output_fasta" == "" ]; then
	echo "Must supply output fasta with -o option"
	errcount=$((errcount+1))
fi

if [ "$taxon_db" == "" ]; then
	echo "Must supply NCBI taxonomic database path with -t option"
	errcount=$((errcount+1))
fi

if [ "$key_type" == "" ]; then
	echo "Must supply key type with -k option"
	errcount=$((errcount+1))
fi

if [ "$header_type" == "" ]; then
	echo "Must supply header_type with -l option"
	errcount=$((errcount+1))
fi

if [ "$errcount" -gt 0 ]; then
	exit 1
fi

if [ ! -f $input_fasta ]; then
	echo "Input fasta '$input_fasta' not found" >&2
	exit 1
fi

if [ ! -d $taxon_db ]; then
	echo "NCBI taxonomic database directory '$taxon_db' not found" >&2
	exit 1
fi

if [ -f $output_fasta ]; then
	echo "Output fasta '$output_fasta' already exists. Manually delete or move and try again" >&2
	exit 1
fi


# Create output files
file_prefix=${input_fasta%.*}
case $key_type in
	'GI') 		file_keys="$file_prefix"_GIkeys.txt
			;;
	'SCINAME') 	file_keys="$file_prefix"_SCINAMEkeys.txt
			;;
	'TAXID') 	file_keys="$file_prefix"_TAXIDkeys.txt
			;;
	*) 		echo "Key type '$key_type' is invalid" >&2
			exit 1
			;;
esac

file_taxons="$file_prefix"_taxons.txt

file_headers="$file_prefix"_headers.txt

file_sequences="$file_prefix"_sequences.txt

file_fasta_minimal="$file_prefix"_minimal.fasta

if [ -f $file_keys ]; then
	echo "Output keys file '$file_keys' already exists. Manually delete or move and try again" >&2
	exit 1
fi

if [ -f $file_taxons ]; then
	echo "Output taxonomic information file '$file_taxons' already exists. Manually delete or move and try again" >&2
	exit 1
fi

if [ -f $file_headers ]; then
	echo "Output SAP headers file '$file_headers' already exists. Manually delete or move and try again" >&2
	exit 1
fi

if [ "$header_type" != "MINIMAL" ]; then
	if [ -f $file_sequences ]; then
		echo "Sequences file '$file_sequences' already exists. Manually delete or move and try again" >&2
	fi
if [ -f $file_fasta_minimal ]; then
		echo "Converted-to-minimal Fasta file '$file_fasta_minmal' already exists. Manually delete or move and try again" >&2
	fi
fi

# Extract keys based on header type
echo "Extracting keys to $file_keys.."
case $header_type in
	'MINIMAL') 	grep '^>.*$' $input_fasta | sed -e 's/>//' > $file_keys
			;;
	'NCBI') 	grep 'gi|[0-9]*' -i -o  $input_fasta | sed -e 's/gi|//' > $file_keys
			grep 'gi|[0-9]*' -i --invert-match  $input_fasta > $file_sequences
			sed -e "s/^/>/" $file_keys | paste /dev/stdin $file_sequences > $file_fasta_minimal -d '\n'
			input_fasta=$file_fasta_minimal
			# Create MINIMAL fasta
			;;
	'KEYVALUE') 	grep "$key_type=[^;]*;" -i -o $input_fasta | sed -e "s/$key_type=//" -e "s/;//" -e "s/ /_/g" > $file_keys
			grep "$key_type=[^;]*;" -i --invert-match $input_fasta > $file_sequences
			sed -e "s/^/>/" $file_keys | paste /dev/stdin $file_sequences > $file_fasta_minimal -d '\n'
			input_fasta=$file_fasta_minimal
			# Create MINIMAL fasta
			;;
	*) 		echo "Key type '$header_type' is invalid" >&2
			exit 1
			;;
esac
echo "Finished extracting keys to $file_keys."

# Use keys to obtain taxonomic information
echo "Using '$key_type' keys to extract taxonomic information"
case $key_type in
	'GI') 		python3 gi-to-tax/gi2tax.py -d $taxon_db -i $file_keys -o $file_taxons -r "[0-9]*" -t nucleotide
			;;
	'SCINAME') 	python3 tax2tax.py -i $file_keys -o $file_taxons -t sciname
			;;
	'TAXID') 	python3 tax2tax.py -i $file_keys -o $file_taxons -t taxid
			;;
	*) 		echo "Key type '$key_type' is invalid" >&2
			exit 1
			;;
esac
echo "Finished using keys to extract taxonomic information"

# Format taxonomic information as SAP headers
echo "Formatting taxonomic information as SAP headers"
python3 gi-to-tax/tax2sap.py -i $file_taxons -o $file_headers
echo "Finished formatting taxonomic information as SAP headers"

#Combine sequences and SAP headers to make SAP-compatible Fasta
echo "Combining sequences and SAP headers to make SAP-compatible Fasta"
python3 makesapdb.py -s $file_headers -f $input_fasta -o $output_fasta -k $key_type
echo "Finished combining sequences and SAP headers to make SAP-compatible Fasta"

