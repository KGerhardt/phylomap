import os

class file_importer:
	def __init__(self, path):
		self.base_path = path
		self.file_list = None
		self.type = None
		self.determine_type()
	
	def determine_type(self):
		if os.path.isdir(self.base_path):
			self.file_list = [os.path.normpath(self.base_path + "/" + f) for f in os.listdir(self.base_path)]
			
		if os.path.isfile(self.base_path):
			is_paths = True
			self.file_list = []
			fh = open(self.base_path)
			for line in fh:
				line = line.strip()
				if not os.path.exists(line):
					self.file_list = None
					is_paths = False
					break
				else:
					self.file_list.append(line)
				
			fh.close()
			
			if is_paths:
				self.eat_paths_file()
			else:
				self.file_list = [self.base_path]
				
			
		