from agnostic_reader_blocks import agnostic_open
from options import align_opts
from file_importer import file_importer
from progress_tracker import progress_tracker
import os
import sys
import multiprocessing

def do_align_and_filter(args):
	read, genomes, database, aln_name, filt_name, ma_name = args[0], args[1], args[2], args[3], args[4], args[5]
	pct_id, af = args[6], args[7]
	reference_multiple_aln = args[8]
	
	#align reads with magicblast
	mb_aln_comm = "magicblast -db {d} -query {q} -out {o} -infmt fasta -outfmt tabular -no_unaligned"
	mb_aln_comm = mb_aln_comm.format(d = database, q = read, o = aln_name)
	os.system(mb_aln_comm)
	
	passing_sequences = []
	for line in agnostic_open(aln_name):
		if line.startswith("#"):
			continue
		else:
			segs = line.strip().split()
			qid = segs[0]
			pid = float(segs[2])
			aln_1 = int(segs[6])
			aln_2 = int(segs[7])
			readlen = int(segs[15])
			aln_len_total = abs(aln_2 - aln_1 + 1)
			if pid > pct_id and (aln_len_total/readlen * 100) > af:
				passing_sequences.append(qid)
	
	#Faster lookup
	passing_sequences = set(passing_sequences)
	
	#We don't need to do anything else if there are no passing reads
	if len(passing_sequences) > 0:
		print_this_read = False
		filtered_reads = open(filt_name, "w")
		for line in agnostic_open(read):
			#Check if the sequence is a defline - if the line is just a sequence, it's covered by its defline.
			if line.startswith(">"):
				#Get the seqid and check if it's in the passing sequences
				print_this_read = (line.strip().split()[0][1:] in passing_sequences)
			#If it is, print it.	
			if print_this_read:
				filtered_reads.write(line)
		
		filtered_reads.close()
	
		mafft_comm = "mafft --quiet --add {combined_reads} --reorder {orig_ma} > {out}"
		mafft_comm = mafft_comm.format(combined_reads=filt_name, orig_ma = reference_multiple_aln, out = ma_name)
		#print("")
		#print(mafft_comm)
		#print("")
		os.system(mafft_comm)
	else:
		print("")
		print("No passing reads found for file:", read + ".", "This file will have no placements and no output in filtered_reads or ma_reads.")
		print("")
	
class phylomap_af:
	def __init__(self, reads, target, threads = 1, type = "nucl", pct_id = 85, aligned_frac = 90):
		self.outpath = target
		self.reads = reads
		
		self.threads = threads
		
		self.genomes = None
		self.whole_ma = None
		self.db = os.path.normpath(self.outpath + "/magicblast/mapping_db")
		self.dbtype = type
		
		self.pct_id = pct_id
		self.af = aligned_frac
		
	def make_dir(self, dir):
		to_make = os.path.normpath(self.outpath + "/" + dir)
		if not os.path.exists(to_make):
			os.makedirs(to_make, exist_ok = True)
	
	def parse_dir(self):
		ok = True
		source = os.path.normpath(self.outpath+"/source")
		if os.path.exists(source):
			self.genomes = os.path.normpath(self.outpath+"/source/combined_genomes.fasta")
			self.whole_ma = os.path.normpath(self.outpath+"/source/combined_genomes_multiple_alignment.fasta")
		else:
			ok = False
			print("No reference genomes detected. Aborting.")
			
		return ok
	
	def make_refdb(self):
		build_db_command = "makeblastdb -in {genomes} -out {db} -parse_seqids -dbtype {type}"
		build_db_command = build_db_command.format(genomes = self.genomes, db = self.db, type = self.dbtype)
		os.system(build_db_command)
	
	#Aligns with magicblast, filters original reads to mapping sequences, multiply aligns to ref with mafft
	def handle_reads(self):
		if self.reads is not None:
			jobs = []
			for r in self.reads:
				name = os.path.basename(r)
				while name != os.path.splitext(name)[0]:
					name = os.path.splitext(name)[0]
				aln_name = os.path.normpath(self.outpath + "/aligned_reads/" + name + ".fasta")
				filt_name = os.path.normpath(self.outpath + "/filtered_reads/" + name + ".fasta")
				ma_name = os.path.normpath(self.outpath + "/ma_reads/" + name + ".fasta")
				jobs.append((r, self.genomes, self.db, aln_name, filt_name, ma_name, self.pct_id, self.af, self.whole_ma,))
			
			tracker = progress_tracker(total = len(jobs), message = "Processing reads.")
			pool = multiprocessing.Pool(self.threads)
			for result in pool.imap_unordered(do_align_and_filter, jobs):
				tracker.update()
			pool.close()
		
	def run(self):
		ok = self.parse_dir()
		if ok:
			self.make_dir("magicblast")
			self.make_dir("aligned_reads")
			self.make_dir("filtered_reads")
			self.make_dir("ma_reads")
			self.make_refdb()
			self.handle_reads()
		
def phylomap_align_and_filter():
	parser, opts = align_opts()
	#not enough opts
	if len(sys.argv) < 3:
		parser.print_help()
		sys.exit()
	
	ok_to_run = True
	reads = opts.reads
	output = opts.targ_dir
	
	pid = float(opts.pid)
	frac = float(opts.frac)
	
	quiet = opts.quiet
	threads = int(opts.threads)
	
	
	if reads is None:
		ok_to_run = False
		print("Phylomap align and filter needs a directory of reads in nucleotide FASTA format. Exiting.")
		parser.print_help()
		sys.exit()
	else:
		imp = file_importer(reads)
		reads_list = imp.file_list
		
		
	if ok_to_run:
		mn = phylomap_af(reads = reads_list,
						target = output,
						threads = threads,
						type = "nucl",
						pct_id = pid,
						aligned_frac = frac)		
		mn.run()
	