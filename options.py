import sys
import argparse

def build_opts():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
			description='''''')

	parser.add_argument('-g', '--genomes', dest = 'genomes', default = None, 
	help =  'A directory containing sequences in nucleotide FASTA format.')

	parser.add_argument('-o', '--output', dest = 'output', default = "phylomap", 
	help = '')
	
	parser.add_argument('-p', '--pakname', dest = 'pkgname', default = "reference.refpkg", 
	help = '')
	
	parser.add_argument('--quiet', dest = 'quiet', action='store_true', 
	help = '')

	args, unknown = parser.parse_known_args()
	
	return parser, args
	
	
def align_opts():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
			description='''''')

	parser.add_argument('-r', '--reads', dest = 'reads', default = None, 
	help =  'A directory containing reads in nucleotide FASTA format.')
	
	parser.add_argument('--target', dest = "targ_dir", default = "phylomap",
	help = 'An existing phylomap directory created by phylomap build.')
	
	parser.add_argument('--pct', dest = "pid", default = 85.0, type = float,
	help = 'Min pct ID to the reference for a read to be kept. Default 85.')
	parser.add_argument('--fraction', dest = "frac", default = 90.0, type = float,
	help = "Min fraction of a read's length that must align to ref to be kept. Default 90")
	
	parser.add_argument('--quiet', dest = 'quiet', action='store_true', 
	help = '')
	parser.add_argument('-t', '--threads', dest = 'threads', type = int, default = 1, 
	help = '')

	args, unknown = parser.parse_known_args()
	
	return parser, args
	
def place_opts():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
			description='''''')

	parser.add_argument('--target', dest = "targ_dir", default = "phylomap",
	help = 'An existing phylomap directory created by phylomap build.')
	
	parser.add_argument('--keep_n', dest = "placements", default = 1, type=int,
	help = 'Top n pplacer placements to keep. A read will appear up to as many times as n. Default 1 (very strongly recommended to keep this at 1).')
	
	parser.add_argument('--quiet', dest = 'quiet', action='store_true', 
	help = '')
	
	parser.add_argument('-t', '--threads', dest = 'threads', type = int, default = 1, 
	help = '')

	args, unknown = parser.parse_known_args()
	
	return parser, args
	
	
def viz_opts():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
			description='''''')

	parser.add_argument('--target', dest = "targ_dir", default = "phylomap",
	help = 'An existing phylomap directory created by phylomap build.')
	
	parser.add_argument('-t', '--threads', dest = 'threads', type = int, default = 1, 
	help = '')
	parser.add_argument('--quiet', dest = 'quiet', action='store_true', 
	help = '')
	
	args, unknown = parser.parse_known_args()
	
	return parser, args