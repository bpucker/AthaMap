### Boas Pucker ###
### b.pucker@tu-braunschweig.de ###
### v0.1 ###

__usage__ = """
					python3 pos_transfer.py
					--in <INPUT_FILE>
					--tair10 <TAIR10_FILE>
					--tair8 <TAIR8_FILE>
					--out <OUTPUT_FILE>
					bug reports and feature requests: b.pucker@tu-braunschweig.de
					"""

import os, sys, re
from operator import itemgetter

# --- end of imports --- #

def load_sequences( fasta_file ):
	"""! @brief load candidate gene IDs from file """
	
	sequences = {}
	with open( fasta_file ) as f:
		header = f.readline()[1:].strip()
		if " " in header:
			header = header.split(" ")[0]
		seq = []
		line = f.readline()
		while line:
			if line[0] == '>':
					sequences.update( { header: "".join( seq ) } )
					header = line.strip()[1:]
					if " " in header:
						header = header.split(" ")[0]
					seq = []
			else:
				seq.append( line.strip() )
			line = f.readline()
		sequences.update( { header: "".join( seq ) } )	
	return sequences


def load_cis_elements( input_file, tair8, fragment_length ):
	"""! @brief load cis elements from given file """
	
	cis_elements = []
	with open( input_file, "r" ) as f:
		header = f.readline().strip().split('\t')
		line = f.readline()
		while line:
			parts = line.strip().split('\t')
			if len( parts ) == len( header ):
				tmp = {}
				for idx, head in enumerate( header ):
					tmp.update( { head: parts[ idx ] } )
				tmp.update( { 	'chr': "Chr" + parts[0][2],
										'up_seq': tair8[ "Chr" + parts[0][2] ][ int( parts[3] )-1: int( parts[3] )+fragment_length ],
										'down_seq': tair8[ "Chr" + parts[0][2] ][ int( parts[3] )-fragment_length: int( parts[3] )+1 ]
									} )
				cis_elements.append( tmp )
			line = f.readline()
	return header, cis_elements


def main( arguments ):
	"""! @brief run everything """
	
	input_file = arguments[ arguments.index('--in')+1 ]
	tair10_file = arguments[ arguments.index('--tair10')+1 ]
	tair8_file = arguments[ arguments.index('--tair8')+1 ]
	output_file = arguments[ arguments.index('--out')+1 ]
	
	fragment_length = 100	#number of basepairs used to transfer position
	
	tair8 = load_sequences( tair8_file )
	tair10 = load_sequences( tair10_file )
	
	# --- load cis elements including 100bp TAIR8 sequence downstream of the annotated position --- #
	headers, cis_elements = load_cis_elements( input_file, tair8, fragment_length )
	
	# --- find match in TAIR10 --- #
	updated_cis_elements = []
	for cis in cis_elements:
		pos = tair10[ cis['chr'] ].find( cis['down_seq'] ) + fragment_length - 1
		print( pos )
		if pos == -1:
			pos = tair10[ cis['chr'] ].find( cis['up_seq'] )
		if pos > -1:
			cis['Position'] = pos+1
			updated_cis_elements.append( cis )
		else:
			print( cis )
	
	# --- generate output file --- #
	with open( output_file, "w" ) as out:
		out.write( "\t".join( headers ) + "\n" )
		for element in updated_cis_elements:
			new_line = []
			for each in headers:
				new_line.append( str( element[ each ] ) )
			out.write( "\t".join( new_line ) + "\n" )
	
	#add search with downstream region as backup to avoid issues caused by SNPs
	#check revcomp in case of inversion
	#add BLAST search as fall-back option for critical regions
	


if '--in' in sys.argv and '--tair10' in sys.argv and '--tair8' in sys.argv and '--out' in sys.argv:
	main( sys.argv )
else:
	sys.exit( __usage__ )
