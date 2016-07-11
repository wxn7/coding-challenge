##Summary

This repo is for Insight Data Engineering Coding Challenge, 2016. What I achieved are:

- Building a  graph of users and their relationship with one another to reflect Venmo payment stream.

- Calculating the median degree across a 60-second sliding window in the rolling.

##Details of implementation

- Transaction/edge representation:
	```
	class Trans { 
		time, 
		target,
		actor
	}
	```
- Graph representation:
	The graph shows payment relationship between people. Here I constructed an undirected graph that is stored in a dictionary, where the 'keys' represents **vertices**, the correspoinding 'value' represents **edges** stored in a adjacent list.

	For example:   
```
	class Graph{
		__graph_dict = {
			"vertex1": [("vertex2", t1), ("vertex3", t2)], 
			"vertex2": [("vertex1", t1)],   
			"vertex3": [("vertex1", t2)] 
			},
		__latest_timestamp = max(t1, t2)
	}
```

- degree of vertex = # of elements in the vertex's adjacent list

## Working environment

- Language: python 2.7.10
- Addtional packages: json, datetime, sys
- Machine specs: 1.3 GHz Intel Core i5 processor and 4GB 1600 MHz DDR3 memory

## Testing and Result:   
	
I constructed my own unit test on the go. Successfully passed the examples given in the discription. Here is the file structure under the folder "insight-testsuit/tests", each of which contains 2 folders for input and output:

- test-1-venmo-trans: read 1 JSON record, making sure correct file structure and output format
- test-2-simple-loading: testing 3 JSON records without time changing, testing degree calculation
- test-3-ordered-inwindow:testing 4 JSON records comming in order, and within 60 sec window
- test-4-ordered-outwindow: the 5th JSON results in new latest timestamp, tested on prunning older records
- test-5-disordered-outwindow: tested on out-of-order transaction

About scaling: I also tested the performance for the larger data file provided, finished in ~0.7s. No records are corrupted/has missing value, but my code takes that into consideration and will skip the incomplete item.


