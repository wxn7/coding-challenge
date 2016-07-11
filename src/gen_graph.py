import parser as p

inf = '../data-gen/venmo-trans.txt'

data = []
data = p.load(inf, data)

print data[0].time