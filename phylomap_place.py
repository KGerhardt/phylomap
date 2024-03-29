from file_importer import file_importer
from agnostic_reader_blocks import agnostic_open
from options import place_opts

import sys
import os

import json


class pplacer_operator:
	def __init__(self, targ_dir, threads = 1, max_placements = 1):
		self.outpath = targ_dir
		self.reads = None
		self.refpak = None
		self.jplaces = []
		self.jplace_tsvs = []
		#self.itol_friendly = []
		self.threads = threads
		self.max_place = max_placements
		
	def make_dir(self, dir):
		to_make = os.path.normpath(self.outpath + "/" + dir)
		if not os.path.exists(to_make):
			os.makedirs(to_make, exist_ok = True)
		
	def locate_refpak(self):
		pak_loc = os.path.normpath(self.outpath+"/reference_package/")
		rp = os.listdir(pak_loc)
		rp = os.path.normpath(pak_loc + "/" + rp[0])
		if os.path.exists(rp):
			self.refpak = rp
		
	def locate_reads(self):
		#ma_reads
		reads_loc = os.path.normpath(self.outpath+"/ma_reads/")
		read_files = [os.path.normpath(reads_loc + "/" + r) for r in os.listdir(reads_loc)]
		
		if len(read_files) > 0:
			self.reads = []
			for r in read_files:
				if os.path.exists(r):
					self.reads.append(r)
		if self.reads == 0:
			self.reads = None
			
	def prep_outputs(self):
		self.make_dir("pplacer_jplace")
		#self.make_dir("itol_friendly_jplace")
		self.make_dir("pplacer_tsv")
		for r in self.reads:
			name = os.path.basename(r)
			while name != os.path.splitext(name)[0]:
				name = os.path.splitext(name)[0]
			jp_name = os.path.normpath(self.outpath + "/pplacer_jplace/"+name + ".jplace")
			tsv_name = os.path.normpath(self.outpath + "/pplacer_tsv/"+name + ".tsv")
			#friendly_name = os.path.normpath(self.outpath + "/itol_friendly_jplace/"+name + ".ItoL.jplace")
			self.jplaces.append(jp_name)
			self.jplace_tsvs.append(tsv_name)
			#self.itol_friendly.append(friendly_name)
		
	def itolize_jplace(self):
		for j, i in zip(self.jplaces, self.itol_friendly):
			fh = open(j, "r")
			jp = json.load(fh)
			fh.close()
			
			#We're duplicating placement info to map each placement set onto just one read for ItoL
			reconfigured_placements = []
			for placement in jp["placements"]:
				if "nm" in placement:
					for read in placement['nm']:
						next_placement = {"p":placement['p'], "nm":[read]}
						reconfigured_placements.append(next_placement)
				elif "n" in placement:
					for read in placement['n']:
						next_placement = {"p":placement['p'], "n":[read]}
						reconfigured_placements.append(next_placement)
	
			jp["placements"] = reconfigured_placements
			
			json_obj = json.dumps(jp, indent = 1)
			
			fh = open(i, "w")
			fh.write(json_obj)
			fh.close()
		
	def run_place(self):
		self.locate_refpak()
		if self.refpak is None:
			print("Couldn't find reference package! Quitting.")
			sys.exit()
			
		self.locate_reads()
		if self.reads is None:
			print("Couldn't find reads! Quitting.")
			sys.exit()
			
		self.prep_outputs()
		
		for r, j, t in zip(self.reads, self.jplaces, self.jplace_tsvs):
			pplacer_arg = "pplacer --discard-nonoverlapped -c {refpkg} -o {out} {reads_aln} -j {thds} --keep-at-most {place_count}"
			pplacer_arg = pplacer_arg.format(refpkg = self.refpak, out=j, reads_aln=r, thds = self.threads, place_count = self.max_place)
			os.system(pplacer_arg)
			
			gup_convert_arg = "guppy to_csv {jplace} > {tsv}_temp.csv".format(jplace = j, tsv = t)
			os.system(gup_convert_arg)
			swap = open(t, "w")
			for line in agnostic_open(t+"_temp.csv"):
				line = line.replace(",", "\t")
				swap.write(line)
			swap.close()
			os.remove(t+"_temp.csv")
		
		#ItoL corrected their jplace parser with my help; this is no longer needed.
		#self.itolize_jplace()

def phylomap_place():
	parser, opts = place_opts()
	#not enough opts
	if len(sys.argv) < 3:
		parser.print_help()
		sys.exit()
	
	ok_to_run = True
	
	td = opts.targ_dir
	threads = opts.threads
	place_ct = opts.placements
	
	if ok_to_run:
		mn = pplacer_operator(targ_dir = td,
							threads = threads,
							max_placements = place_ct)
		mn.run_place()
	