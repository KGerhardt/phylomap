import sys

def main():
	if len(sys.argv) < 2:
		print("Use: 'phylomap [module] to specify a behavior.'")
		print("Modules are: 'build', 'af', 'place', 'viz'.")
		sys.exit("Specify a phylomap module. Or else.")
		
	arg = sys.argv[1]
	if arg == "build":
		from phylomap_build import phylomap_build
		phylomap_build()
		
	if arg == "af":
		from phylomap_align_and_filter import phylomap_align_and_filter
		phylomap_align_and_filter()
		
	if arg == "place":
		from phylomap_place import phylomap_place
		phylomap_place()
		
	if arg == "viz":
		from phylomap_visualize import phylomap_viz
		phylomap_viz()
	
if __name__ == "__main__":
	main()