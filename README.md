# Retrievability





## Document Retrievability Calculator
Use `document_retrievability_calculator.py` to compute the retrievability scores for each document. 

The `calculator.py` takes:
- result_file: TREC formatted
- out_file: the output file with contain the docid and retrievability scores for each item, one per line, tab/space sep.
- c: the cutoff
- b: the discount for gravity, set to 0.0 for cumulative scores

**Update to include a corpus file so that it outputs a value for each document, regardless of whether it has been
returned as a result or not.**

Example usage:
```console
$ python code/document_retrievability_calculator.py data/wapo2018.bm25.baseline.res data/wapo2018.bm25.baseline.c100.b0.5.ret 100 0.5

About to compute there retrievability on result file: data/wapo2018.bm25.baseline.res and will save the retrievability scores to: data/wapo2018.bm25.baseline.c100.b0.5.ret
Calculating the gravity score with discount: 0.5 and cut off: 100
Results written to: data/wapo2018.bm25.baseline.c100.b0.5.ret
Done!
```

** Note the above file is only on the 50 trec queries -- for demo purposes -- use a larger result file contain thousands of questions
for a better estimate of retrievability **

##  Author Retrievability Calculator
This script takes a document retrievability file (from the above script as input) and maps the document retrievabilty score to
an author given an document to author mapping.

The `author_retrievability_calculator.py` takes:
- ret_file: a file with contain the docid and retrievability scores for each item, one per line, tab/space sep.
- doc_author_file: a file that contains docid and author name, one per line, tab separated
- out_file: a retrievability file that contains author name and aggegrated retrievability scores, one per line, tab separated.

```console
$ python code/author_retrievability_calculator.py data/wapo2018.bm25.baseline.r0.5.ret data/wapo2018.doc.to.authors data/wapo2018.bm25.baseline.authors.r0.5.ret
About to compute there retrievability for authors ...
Results written to: data/wapo2018.bm25.baseline.authors.r0.5.ret
Done!
```


## Gini Calculator

Use `gini_calculator.py` to calculate the gini cofficient for a given retrievability file.
- ret_file: a file contained the docid and retrievability scores for each item, one per line, tab/space sep.

Example usage:
```console
$ python code/gini_calculator.py data/wapo2018.bm25.baseline.r0.5.ret 
About to compute the Gini given the retrievability file data/wapo2018.bm25.baseline.r0.5.ret
Read in 595037 scores.
Total Retrievability Mass: 3711861.8760
Gini Cofficient is: 0.3919
Done!

$ python code/gini_calculator.py data/wapo2018.bm25.baseline.authors.r0.5.ret 
About to compute the Gini given the retrievability file data/wapo2018.bm25.baseline.authors.r0.5.ret
Read in 28821 scores.
Total Retrievability Mass: 3711861.8758
Gini Cofficient is: 0.9346
Done!

```

## Transform Retrievability Scores
Use `transform_retrievability_scores.py` to perform a k transform on the retrievability scores.

It takes:
- ret_file: a file contained the docid and retrievability scores for each item, one per line, tab/space sep.
- out_file: an output file contains the docid and retrievability scores for each item, one per line, tab/space sep.
- k: the trasnformation value

```console
$ python code/transform_retrievability_scores.py data/wapo2018.bm25.baseline.c100.b0.5.ret data/wapo2018.bm25.baseline.c100.b0.5.k10.ret 10
About to transform the retrievability file data/wapo2018.bm25.baseline.c100.b0.5.ret using 10.0
Total Retrievability mass: 929.4847999999986
New Total Retrievability mass: 994.7788449467241
Done!
```


## Result Re-Ranker
Use `result_reranker.py` to re-rank TREC results run files by adjusting the scores
with retrievability (or any values).

The combination method is based on reducing the scores (via a lambda)
and re-ranking the top k documents.

The `result_reranker.py` takes:
- result_file: TREC formatted
- ret_file: a file contained the docid and retrievability scores for each item, one per line, tab/space sep.
- out_file: the name of the file which will store the re-ranking in TREC format
- k: the number of items to re-rank
- lam: the amount of adjustment

Example usage:
```console
$ python code/result_reranker.py data/wapo2018.bm25.baseline.res data/wapo2018.bm25.baseline.r0.5.ret data/wapo2018.reranked.bm25.50.0.9.res 50 0.9
About to re-rank: data/wapo2018.bm25.baseline.res using the retrievability scores from: data/wapo2018.bm25.baseline.r0.5.ret
Read in 595037 retrievability scores.
About to process the files and re-rank with k=50 and lambda=0.9
Reranking Topic: 321
Reranking Topic: 336
Reranking Topic: 341
Reranking Topic: 347
Reranking Topic: 350
Reranking Topic: 362
...
Reranking Topic: 823
Reranking Topic: 824
Reranking Topic: 825
Results written to: data/wapo2018.reranked.bm25.50.0.9.res
Done!
```

This will re-rank the top 50 per topic with lambda = 0.9 using the retrievability scores in the
.ret file.


## Performance

Use `trec_eval` to get the performance for the re-ranked run.

```
trec_eval data/wapo2018.qrels data/wapo2018.reranked.bm25.50.0.9.res 
runid                 	all	Anserini-rr-k50-lam0.9
num_q                 	all	50
num_ret               	all	49564
num_rel               	all	3948
num_rel_ret           	all	2401
map                   	all	0.2009
gm_map                	all	0.1254
Rprec                 	all	0.2604
bpref                 	all	0.2723
recip_rank            	all	0.5019
...
P_5                   	all	0.3400
P_10                  	all	0.3240
P_15                  	all	0.3253
P_20                  	all	0.3270
P_30                  	all	0.3247
P_100                 	all	0.2048
P_200                 	all	0.1406
P_500                 	all	0.0787
P_1000                	all	0.0480
```