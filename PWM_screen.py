### Boas Pucker ###
### b.pucker@tu-braunschweig.de ###
### v0.11 ###

__usage__ = """
					python3 PWM_screen.py
					--pwm <pwm_FILE>
					--seq <FASTA_FILE>
					--out <OUTPUT_FILE>
					
					optional:
					--cutoff <MIN_SCORE_CUTOFF>[3.0]
					"""


import os, sys
from operator import itemgetter

# --- end of imports --- #

def load_pwm( pwm_file ):
	"""! @brief load information from pwm file """
	
	pwm = {}
	with open( pwm_file, "r" ) as f:
		header = f.readline()
		line = f.readline()
		while line:
			parts = line.strip().split('\t')
			pwm.update( { int( parts[0] )-1: { 	'A': float( parts[1] ),
																	'C': float( parts[2] ),
																	'G': float( parts[3] ),
																	'T': float( parts[4] )
																} } )
			line = f.readline()
	return pwm, len( list( pwm.keys() ) )


def load_sequences( fasta_file ):
	"""! @brief load candidate gene IDs from file """
	
	sequences = {}
	with open( fasta_file ) as f:
		header = f.readline()[1:].strip()
		seq = []
		line = f.readline()
		while line:
			if line[0] == '>':
					sequences.update( { header: "".join( seq ).upper() } )
					header = line.strip()[1:]
					seq = []
			else:
				seq.append( line.strip() )
			line = f.readline()
		sequences.update( { header: "".join( seq ).upper() } )	
	return sequences


def construct_revcomp_pwm( pwm_fw ):
	"""! @brief construct reverse pwm """
	
	pwm_rv = {}
	data = []
	for key in list( pwm_fw.keys() ):
		data.append( { 'key': key, 'val': pwm_fw[ key ] } )
	data = sorted( data, key=itemgetter('key') )[::-1]
	for idx, each in enumerate( data ):
		pwm_rv.update( { idx: { 	'A': each['val']['A'],
												'C': each['val']['G'],
												'G': each['val']['C'],
												'T': each['val']['A']
											} } )
	return pwm_rv


def calculate_score( pwm, kmer ):
	"""! @brief calculate score for each k-mer based on pwm """
	
	score = 0
	for k, nt in enumerate( kmer ):
		try:
			score += pwm[ k ][ nt ]
		except KeyError:
			pass
	return score


def revcomp( seq ):
	"""! @brief construct reverse complement of sequence """
	
	new_seq = []
	
	bases = { 'a':'t', 't':'a', 'c':'g', 'g':'c' }
	for nt in seq.lower():
		try:
			new_seq.append( bases[nt] )
		except:
			new_seq.append( 'n' )
	return ''.join( new_seq[::-1] ).upper()


def main( arguments ):
	"""! @brief run everything """
	
	pwm_file = arguments[ arguments.index('--pwm')+1 ]
	seq_file = arguments[ arguments.index('--seq')+1 ]
	output_file = arguments[ arguments.index('--out')+1 ]
	
	if "--cutoff" in arguments:
		cutoff_factor = float( arguments[ arguments.index('--cutoff')+1 ] )
	else:
		cutoff_factor = 0.5
	
	pwm_fw, pwm_len = load_pwm( pwm_file )
	if pwm_len == 0:
		sys.exit( "ERROR: EMPTY pwm file - processing stopped." )
	pwm_rv = construct_revcomp_pwm( pwm_fw )
	
	cutoff = cutoff_factor * pwm_len
	
	seqs = load_sequences( seq_file )
	with open( output_file, "w" ) as out:
		out.write( "Sequence\tStart\tEnd\tOrientation\tSequence\tScore\n" )
		for key in list( seqs.keys() ):
			seq = seqs[ key ]
			for i in range( len( seq )-1 ):
				kmer = seq[ i:i+pwm_len ]
				fw_score = calculate_score( pwm_fw, kmer )
				rv_score = calculate_score( pwm_rv, kmer )
				if fw_score > cutoff:
					out.write( "\t".join( [ key, str( i+1 ), str( i+pwm_len+1 ), "+", kmer, str( fw_score ) ] ) + "\n" )
				if rv_score > cutoff:
					out.write( "\t".join( [ key, str( i+1 ), str( i+pwm_len+1 ), "-", revcomp( kmer ), str( rv_score ) ] ) + "\n" )


if '--pwm' in sys.argv and '--seq' in sys.argv and '--out' in sys.argv:
	main( sys.argv )
else:
	sys.exit( __usage__ )
