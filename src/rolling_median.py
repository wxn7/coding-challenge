import sys
import json
from datetime import datetime

def parse_time(time_str):
		'''raw format of timestamp: YYYY-MM-DDTHH:MM:SSZ'''
		'''convert to datetime object'''
		timestamp = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
		return timestamp

class Tran:
	def __init__(self, time, target = "", actor=""):
		self.time = time
		self.target = target
		self.actor = actor
	def isBad(self):
		if (self.target == "" or self.actor == ""):
			return True
		else:
			return False

class Graph:
	def __init__(self, cur_graph={}):
		''' Graph is represented by a dictionary'''
		''' With the vertices as 'key', and adjacent list as 'value' '''
		''' default to be empty '''
		self.__graph_dict = cur_graph
		self.__latest_ts = datetime(1900, 1, 1, 0, 0, 0)

	def add_edge(self, item):
		'''
		Passing in a transaction named "item",
		and add into graph only if it's within 60 sec window.
		'''
		ts = item.time #current timestamp
		v1 = item.actor
		v2 = item.target

		gap = (ts - self.__latest_ts).total_seconds()
		# print gap

		#only add if the new item is within 60 sec window prior to __latest_ts
		if gap <= -60:
			pass # too old, ignore
		else:
			#check if need to add new vertex
			if v1 not in self.__graph_dict:
				self.__graph_dict[v1] = []
			if v2 not in self.__graph_dict:
				self.__graph_dict[v2] = []

			#if both v1, v2 already exist, check if they are connected
			adj_list = self.__graph_dict[v1]
			connected = False
			for (v, t) in adj_list: 
				if v == v2:  #v1, v2 already connected
					connected = True
					if t < ts: #cur is the newer version
						self.__graph_dict[v1].remove((v2,t))
						self.__graph_dict[v2].remove((v1,t))
						self.__graph_dict[v1].append((v2, ts))
						self.__graph_dict[v2].append((v1, ts))
					else: 
						break #ignore this
			if not connected:
				self.__graph_dict[v1].append((v2, ts))
				self.__graph_dict[v2].append((v1, ts))

		# check if newer than latest, we need to:
		# 	1. update latest timestamp
		#   2. prune old
		if gap > 0: 
			self.__latest_ts = ts
			#Done: prune old
			#check current vertices one by one, remove too old ones
			vertices = self.__graph_dict.keys()
			for v1 in vertices:
				for (v2, t) in self.__graph_dict[v1]:
					if (ts-t).total_seconds() >= 60:
						# print v2
						#remove edge
						self.__graph_dict[v1].remove((v2, t))
						self.__graph_dict[v2].remove((v1, t))
						degree_v1 = self.calculate_degree(v1)
						degree_v2 = self.calculate_degree(v2)
						# evict disconnected node
						if degree_v1 == 0:
							vertices.remove(v1)
							self.__graph_dict.pop(v1)
						if degree_v2 == 0:
							vertices.remove(v2)
							self.__graph_dict.pop(v2)


	def calculate_degree(self, vertex):
		'''degree of a vertex is the number of its adjacent node'''
		if vertex in self.__graph_dict:
			return len(self.__graph_dict[vertex])

	def calculate_median(self):
		degrees = [] # maintain a degree list
		for k in self.__graph_dict.keys():
			degrees.append(self.calculate_degree(k))

		# return median(degrees)
		degrees.sort()
		n = len(degrees)
		
		if n % 2:
			return degrees[n//2]
		else:
			return (degrees[n//2-1] + degrees[n//2]) / 2.0
	
	
	# Functions for debugging only
	# def get_ts(self):
	# 	return self.__latest_ts
	#
	# def check_graph(self):
	#   	print "# of nodes: " + str(len(self.__graph_dict.keys()))
	# 	for k in self.__graph_dict.keys():
	# 		print k + ":" + str(self.calculate_degree(k))
	#
	

# def test_loading_file(record):
# 	print "actor="+record['actor'] \
# 		+ "  target=" + record["target"]\
# 		+ "  created_time="+record["created_time"]

if __name__ == "__main__":	
	try:
		in_path = sys.argv[1]
		out_path = sys.argv[2]
	except IndexError:
		print "Not enough I/O arguments. Needs " \
				+str(3-len(sys.argv))+" more."
		quit()

	try:
		inf = open(in_path, 'r')
		outf = open(out_path, 'w')
		g = Graph()
		cnt = 0

		for line in inf:
			try:
				record = json.loads(line)
			
				_time_ = parse_time(record["created_time"])
				_target_ = record["target"]
				_actor_ = record["actor"]

				item = Tran(_time_, _target_ , _actor_)
				if item.isBad(): #incomplete record
					continue
				else:
					g.add_edge(item)
					median = g.calculate_median()
					#Debug:
					# cnt += 1
					# test_loading_file(record)
					# g.check_graph()
					# print '{0:.2f}'.format(median)# + str(g.get_ts())
					outf.write('{0:.2f}\n'.format(median))
			except ValueError:
				print("JSON decoder failed.")
		
		inf.close()
		outf.close()
		# print str(cnt) + " medians generated."
	except IOError:
		print("Could not read file:", in_path)