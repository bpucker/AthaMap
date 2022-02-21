### Boas Pucker ###
### b.pucker@tu-braunschweig.de ###
### v0.23 ###

__usage__ = """
					python3 cis2coexp.py
					[--cis <CIS_ELEMENT_FILE>|--cisdir <CIS_ELEMENT_FILE_FOLDER>]
					--exp <EXPRESSION_FILE>
					[--ref <REFERENCE_AGI>|--reffile <REFERENCE_AGI_FILE>]
					--out <OUTPUT_FOLDER>
					--cutoff <MIN_SCORE_CUTOFF>
					
					optional:
					
					bug reports and feature requests: b.pucker@tu-braunschweig.de
					"""

import os, sys, re, glob, subprocess, math
import numpy as np
from operator import itemgetter
from scipy import stats
import matplotlib.pyplot as plt

# --- end of imports --- #


def load_agis_from_cis_element_file( cis_element_file, min_score_cutoff ):
	"""! @brief load all AGIs from given file """
	
	agis = []
	with open( cis_element_file, "r" ) as f:
		f.readline()	#header
		line = f.readline()
		while line:
			parts = line.strip().split('\t')
			try:
				score = float( parts[-1] )
				if score > min_score_cutoff:
					agis.append( parts[0].split('.')[0].upper() )
			except ValueError:
				pass
			line = f.readline()
	agis = list( set( agis ) )
	final_agis = {}
	for agi in agis:
		final_agis.update( { agi: None } )
	return final_agis


def load_expression_values( filename ):
	"""! @brief load all expression values """
	
	expression_data = {}
	with open( filename, "r" ) as f:
		tissues = f.readline().strip().split('\t')[1:]
		line = f.readline()
		while line:
			parts = line.strip().split('\t')
			expression = {}
			for idx, each in enumerate( parts[1:] ):
				expression.update( { tissues[  idx ] : float( parts[ idx+1 ] ) } )
			line = f.readline()
			expression_data.update( { parts[0].split('.')[0]: expression } )
	return expression_data


def compare_candidates_against_all( candidate, gene_expression, rcut, pcut, expcut, number_of_genes ):
	"""! @brief compare candidate gene expression against all genes to find co-expressed genes """
	
	tissues = list( sorted( list( gene_expression[ list( gene_expression.keys() )[0] ].keys() ) ) )
	coexpressed_genes = []
	errors = []
	for i, gene2 in enumerate( gene_expression.keys() ):
		if candidate != gene2:
			values = []
			total_expression = 0
			for tissue in tissues:
				try:
					x = gene_expression[ candidate ][ tissue ]
					y = gene_expression[ gene2 ][ tissue ]
					total_expression += y
					if not math.isnan( x ) and not math.isnan( y ) :
						values.append( [ x, y ] )
				except KeyError:
					pass
			try:
				r, p = stats.spearmanr( values )
				if not math.isnan( r ) and total_expression > expcut:
					#if r > rcut and (p*number_of_genes) < pcut:
					if abs( r ) > rcut and p < pcut:
						coexpressed_genes.append( { 'id': gene2, 'correlation': r, 'p_value': p } )
			except ValueError:
				errors.append( candidate )
	if len( list( set( errors ) ) ) > 0:
		sys.stdout.write( "ERRORS: " + ";".join( list( set( errors ) ) ) )
		sys.stdout.flush()
	return coexpressed_genes


def load_ref_AGIs( input_file ):
	"""! @brief load AGIs from given file """
	
	ref_AGIs = {}
	with open( input_file, "r" ) as f:
		line = f.readline()
		while line:
			parts = line.strip().split('\t')
			if len( parts ) > 1:
				ref_AGIs.update( { parts[0]: parts[1] } )
			line = f.readline()
	return ref_AGIs


def main( arguments ):
	"""! @brief run everything """
	
	if '--cis' in arguments:
		cis_element_files = [ arguments[ arguments.index('--cis')+1 ] ]
		ref_AGIs = { cis_element_files[0].split('/')[-1].split('.tx')[0]: arguments[ arguments.index('--ref')+1 ] }
	else:
		input_folder = arguments[ arguments.index('--cisdir')+1 ]
		cis_element_files = glob.glob( input_folder + "*.txt" )
		ref_AGIs = load_ref_AGIs( arguments[ arguments.index('--reffile')+1 ] )
	
	exp_file = arguments[ arguments.index('--exp')+1 ]
	output_folder = arguments[ arguments.index('--out')+1 ]
	
	if '--cutoff' in arguments:
		try:
			min_score_cutoff = float( arguments[ arguments.index('--cutoff')+1 ] )
		except:
			min_score_cutoff = 0.0
	else:
		min_score_cutoff = 0.0
	
	print( min_score_cutoff )
	
	rcut = 0.1
	pcut = 0.05
	expcut = 1
	
	gene_expression = load_expression_values( exp_file )
	
	for cis_element_file in cis_element_files:
		cis_element_related_agis = load_agis_from_cis_element_file( cis_element_file, min_score_cutoff )
		ID = cis_element_file.split('/')[-1].split('.tx')[0]
		try:
			ref_AGI = ref_AGIs[ ID ]
			number_of_genes = float( len( list( gene_expression.keys() ) ) )
			coexpressed_genes = sorted( compare_candidates_against_all( ref_AGI, gene_expression, rcut, pcut, expcut, number_of_genes ), key=itemgetter( 'correlation' ) )[::-1]
			cis_supported = []
			cis_independent = []
			sys.stdout.write( str( len( coexpressed_genes ) ) + "\n" )
			for entry in coexpressed_genes:
				try:
					cis_element_related_agis[ entry['id'] ]
					cis_supported.append( entry['correlation'] )
				except KeyError:
					cis_independent.append( entry['correlation'] )
			sys.stdout.write( ID + "\t" + str( np.mean( cis_supported ) ) + "\t" + str( np.mean( cis_independent ) ) + "\n" )
			sys.stdout.flush()
		except KeyError:
			pass


if '--cis' in sys.argv and '--exp' in sys.argv and '--ref' in sys.argv and '--out' in sys.argv:
	main( sys.argv )
elif '--cisdir' in sys.argv and '--exp' in sys.argv and '--reffile' in sys.argv and '--out' in sys.argv:
	main( sys.argv )
else:
	sys.exit( __usage__ )
