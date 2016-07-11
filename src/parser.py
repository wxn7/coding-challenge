import json

class Tran:
	time = 0
	actor = ""
	target = ""

	def __init__(self, time, target, actor):
		self.time = time
		self.target = target
		self.actor = actor

def load(path, data):
	with open(path) as inf:
		for line in inf:
			record = json.loads(line)

			_time_ = record["created_time"]
			_target_ = record["target"]
			_actor_ = record["actor"]

			x = Tran(_time_, _target_ , _actor_)

			data.append(x)
	
	return data



# print data[0].target
	

	
	

