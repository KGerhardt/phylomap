from agnostic_reader_blocks import agnostic_open
from options import build_opts
from file_importer import file_importer
import os
import sys

class phyl_builder:
	def __init__(self, genomes, outpath, package_name = "phylomap_ref.pkg", is_nt = True, locus = "placeholder"):
		self.gens = genomes
		self.outpath = outpath
		
		self.is_nt = is_nt
		
		self.make_dir("source")
		
		self.combined_genomes = os.path.normpath(outpath + "/source/combined_genomes.fasta")
		self.cg_writer = None
		
		self.mult_aln = os.path.normpath(outpath + "/source/combined_genomes_multiple_alignment.fasta")
		self.fasttree_log = os.path.normpath(outpath + "/source/combined_genomes_fasttree_log.txt")
		self.fasttree_tree = os.path.normpath(outpath + "/source/combined_genomes_fasttree_tree.txt")
		
		self.make_dir("reference_package")
		
		self.refpkg = os.path.normpath(outpath + "/reference_package/" + package_name)
		if not self.refpkg.endswith(".refpkg"):
			self.refpkg+=".refpkg"
			
		self.locus = locus
		
	def make_dir(self, dir):
		to_make = os.path.normpath(self.outpath + "/" + dir)
		if not os.path.exists(to_make):
			os.makedirs(to_make, exist_ok = True)
		
	def combine_fasta(self, file):
		try:
			for line in agnostic_open(file):
				self.cg_writer.write(line)
		except:
			print("Couldn't read file", file)
			print("Skipping.")
			
	def make_ma(self):
		#This might be a version thing
		muscle_ma_command = ["muscle", "-align", self.combined_genomes, "-output", self.mult_aln]
		muscle_ma_command = " ".join(muscle_ma_command)
		#print(muscle_ma_command)
		os.system(muscle_ma_command)
		
	def make_tree(self):
		fasttree_command = ["fasttree", "-nt", "-gtr", "-log", self.fasttree_log, "-out", self.fasttree_tree, self.mult_aln]
		fasttree_command = " ".join(fasttree_command)
		os.system(fasttree_command)
			
	def make_refpak(self):
		if self.is_nt:
			taxit_arg = "taxit create -l {locus} -P {packname} --aln-fasta {aln} --tree-stats {log} --tree-file {tree}"
			taxit_arg = taxit_arg.format(locus=self.locus, packname=self.refpkg, aln=self.mult_aln, log=self.fasttree_log, tree=self.fasttree_tree)
			os.system(taxit_arg)
		else:
			print("Make proteins work?")
		
	def run(self):
		self.cg_writer = open(self.combined_genomes, "w")
		for g in self.gens:
			self.combine_fasta(g)
		self.cg_writer.close()
		
		self.make_ma()
		self.make_tree()
		self.make_refpak()		

def phylomap_build():
	parser, opts = build_opts()
	#not enough opts
	if len(sys.argv) < 3:
		parser.print_help()
		sys.exit()
	
	ok_to_run = True
	genomes = opts.genomes
	output = opts.output
	pakname = opts.pkgname
	quiet = opts.quiet
	
	if genomes is None:
		ok_to_run = False
		print("Phylomap build needs a directory of genomes in nucleotide FASTA format. Exiting.")
		parser.print_help()
		sys.exit()
	else:
		imp = file_importer(genomes)
		genome_list = imp.file_list
		
		
	if ok_to_run:
		mn = phyl_builder(genomes = genome_list,
						outpath = output,
						package_name = pakname,
						is_nt = True)		
		mn.run()
		