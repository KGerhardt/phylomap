from file_importer import file_importer
from agnostic_reader_blocks import agnostic_open
from options import viz_opts

import json
import sys
import os

import re

import ete3


class jplace_plotter:
	def __init__(self, my_jp, name, viz_path):
		self.jp = my_jp
		self.name = name
		self.vp = viz_path
		
		self.tree = None
		self.as_newick = None
		self.tree_figure = None
		
		self.placements = None
		self.metadata = None
		self.fields = None
		
		self.node_field = None
		
		self.placements_by_node = None
		self.counts_by_node = None
		
	def read_jplace(self):
		fh = open(self.jp, "r")
		jp_data = json.load(fh)
		fh.close()
		#The tree structure
		self.tree = jp_data["tree"]
		#The data wrt read placements is all in this. This is what really needs parsing.
		self.placements = jp_data["placements"]
		#Really just the invocation of pplacer
		self.metadata = jp_data["metadata"]
		self.fields = jp_data["fields"]
		jp_data = None
		
		self.node_field = self.fields.index('edge_num')
		
		self.placements_by_node = {}
		self.counts_by_node = {}
		
		for placement in self.placements:
			best_placement = placement['p'][0]
				
			node = best_placement[self.node_field]
			
			if node not in self.counts_by_node:
				self.counts_by_node[node] = 0
			self.counts_by_node[node] += 1
			#This is just bookkeeping.
			if node not in self.placements_by_node:
				self.placements_by_node[node] = []
			
			#This is consistent for getting the best hit name,
			read_name = placement['nm'][0][0]
			self.placements_by_node[node].append(read_name)	

	def render_tree(self):
		self.as_newick = re.sub("\{\d+\}", "", self.tree)
		
		self.tree_figure = ete3.Tree(self.as_newick)
		
		print(self.tree_figure)
		#print(dir(self.tree_figure))
		
		#self.tree_figure.show()
		
		self.tree_figure.render("example.svg")
			
	
class jplace_visualizer:
	def __init__(self, output_path, threads = 1):
		self.jp = None
			
		self.outpath = output_path
		self.threads = threads
		
		self.names = None
		self.viznames = None
		
	def make_dir(self, dir):
		to_make = os.path.normpath(self.outpath + "/" + dir)
		if not os.path.exists(to_make):
			os.makedirs(to_make, exist_ok = True)
			
	def find_placements(self):
		place_loc = os.path.normpath(self.outpath+"/pplacer_jplace/")
		self.jp = [os.path.normpath(place_loc + "/" + j) for j in os.listdir(place_loc)]
		self.names = []
		self.viznames = []
		for j in self.jp:
			name = os.path.basename(j)
			while name != os.path.splitext(name)[0]:
				name = os.path.splitext(name)[0]
			
			vizname = os.path.normpath(self.outpath+"/figures/"+name+".svg")
			self.names.append(name)
			self.viznames.append(vizname)
			
	def craft_plots(self):
		#we'll pool this later.
		for j, n, v in zip(self.jp, self.names, self.viznames):
			plotter = jplace_plotter(j, n, v)
			plotter.read_jplace()
			plotter.render_tree()

		

		
def phylomap_viz():
	parser, opts = viz_opts()
	#not enough opts
	if len(sys.argv) < 3:
		parser.print_help()
		sys.exit()
	
	ok_to_run = True
	
	td = opts.targ_dir
	threads = opts.threads
	
	if ok_to_run:
		mn = jplace_visualizer(output_path = td,
		threads = threads)
		mn.find_placements()
		mn.craft_plots()
		