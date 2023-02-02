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
		
	def itolize_jplace(self):
		for j in [self.jp]:
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
			
			fh = open(j+"_reconfigured.jplace", "w")
			fh.write(json_obj)
			fh.close()

		
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
		
		for placement_list in self.placements:
			for placement in placement_list['p']:
				node = best_placement[self.node_field]
			
				if node not in self.placements_by_node:
					self.placements_by_node[node] = []
					
				if node not in self.counts_by_node:
					self.counts_by_node[node] = 0
					
				if "nm" in placement_list_list:
					for read in placement['nm']:
						self.counts_by_node[node] += 1
						self.placements_by_node[node].append(read[0])
				
				elif "n" in placement_list:
					for read in placement_list['n']:
						self.counts_by_node[node] += 1
						self.placements_by_node[node].append(read[0])
			
			
	def render_tree(self):
		self.as_newick = re.sub("\{\d+\}", "", self.tree)
		
		self.tree_figure = ete3.Tree(self.as_newick)
		
		print(self.tree_figure)
		
		tot = 0
		for i in range(0, len(self.counts_by_node)):
			print("node", i, self.counts_by_node[i])
			tot += self.counts_by_node[i]
		print("tot", tot)
		
			
	
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
			#plotter.itolize_jplace()
			plotter.read_jplace()
			#plotter.render_tree()

		
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
		