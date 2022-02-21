### Boas Pucker ###
### b.pucker@tu-braunschweig.de ###
### v0.1 ###

__usage__ = """
					python3 PWM_merger.py
					--in <INPUT_FOLDER>
					--out <OUTPUT_FOLDER>
					--info <INFO_FILE>
					
					optional:
					--percutoff <PERCENTAGE_OF_MAX_SCORE_CUTOFF>[90%]
					"""
#	--numcutoff <NUMBER_CUTOFF>[500]

import os, sys, glob
from operator import itemgetter

# --- end of imports --- #

def pwms_per_TF( info_file ):
	"""! @brief load the IDs of all PWMs that belong to the same TF """
	
	pwms_per_tf = {}
	with open( info_file, "r" ) as f:
		f.readline()	#remove header
		line = f.readline()
		while line:
			parts = line.strip().split('\t')
			if len( parts[3] ) > 1:
				try:
					pwms_per_tf[ parts[0] ].append( parts[3] )
				except KeyError:
					pwms_per_tf.update( { parts[0]: [ parts[3] ] } )
			line = f.readline()
	return pwms_per_tf


def load_pmw( pwm_file ):
	"""! @brief load information from PMW file """
	
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


def calculate_average_pmw( pwms ):
	"""! @brief calcualte average frequencies of PWMs """
	
	factor = 10000000.0
	avg_pwm = {}
	for key in list( pwms[0].keys() ):
		tmp = { 'A': 0, 'C': 0, 'G': 0, 'T': 0 }
		for pwm in pwms:
			for nt in pwm[ key ]:
				tmp[ nt ] += pwm[ key ][ nt ] * factor
		freqs = {}
		for nt in list( tmp.keys() ):
			freqs.update( { nt: tmp[ nt ] / factor } )
		avg_pwm.update( { key: freqs } )
	return avg_pwm


def merge_PWMs( pwm_IDs, input_folder ):
	"""! @brief merge all PWMs that belong to the same TF """
	
	error = False
	# --- load all PWM data --- #
	loaded_pwms = []
	pwm_lengths = []
	pwm_cons_seq = []
	for ID in pwm_IDs:
		pwm_file = input_folder + ID + ".txt"
		pwm, pwm_len = load_pmw( pwm_file )
		if pwm_len > 1:
			loaded_pwms.append( pwm )
			pwm_lengths.append( pwm_len )
			cons_seq = []
			for key in list( pwm.keys() ):
				vals = pwm[ key ]
				max_freq = 0
				dominant = "N"
				for nt in list( vals.keys() ):
					if vals[ nt ] > max_freq:
						max_freq = vals[ nt ] + 0
						dominant = nt + ""
				cons_seq.append( dominant )
			pwm_cons_seq.append( "".join( cons_seq ) )
	
	if len( list( set( pwm_lengths ) ) ) == 1:	#all PWMs have the same length
		average_pmw = calculate_average_pmw( loaded_pwms )
		#print ( "ok" )
	elif len( list( set( pwm_lengths ) ) ) == 0:	#all PWMs are empty
		return {}
	else:
		min_len = min( pwm_lengths )
		min_cons_seq = pwm_cons_seq[ pwm_lengths.index( min_len ) ]
		trimmed_pwms = []
		#print( "\n\n\n\n" )
		#print( min_len )
		#print( min_cons_seq )
		for idx, pwm in enumerate( loaded_pwms ):
			if len( list( pwm.keys() ) ) == min_len:
				trimmed_pwms.append( pwm )
			else:
				start = pwm_cons_seq[ idx ].find( min_cons_seq )
				if start > -1:
					#print( "\n" )
					#print( start )
					#print( range( start, start+min_len ) )
					clean = {}
					for i in range( start, start+min_len ):
						clean.update( { i-start: pwm[ i ] } )
					trimmed_pwms.append( clean )
					#print( "ok" )
				else:
					error = True
					#print( "ERROR: consensus seq not matching - " + pwm_IDs[ idx ] + "\t" + str( len( pwm_IDs ) ) )
		average_pmw = calculate_average_pmw( trimmed_pwms )
	
	if error:
		print( pwm_IDs[:3] )
	return average_pmw
	

def main( arguments ):
	"""! @brief run everything """
	
	input_folder = arguments[ arguments.index('--in')+1 ]
	output_folder = arguments[ arguments.index('--out')+1 ]
	info_file = arguments[ arguments.index('--info')+1 ]
	
	pwms_per_tf = pwms_per_TF( info_file )
	merged_pwms_per_tf = {}
	for tf in list( pwms_per_tf.keys() ):
		merged = merge_PWMs( pwms_per_tf[ tf ], input_folder )
		merged_pwms_per_tf.update( { tf: merged } )



if '--in' in sys.argv and '--out' in sys.argv and '--info' in sys.argv:
	main( sys.argv )
else:
	sys.exit( __usage__ )
