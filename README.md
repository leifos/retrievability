# retrievability


## Result Re-Ranker
Use `rerank.py` to re-rank TREC results run files by adjusting the scores
with retrievability (or any values).

The combination method is based on reducing the scores (via a lambda)
and re-ranking the top k documents.

The `rerank.py` takes:
- result_file: TREC formatted
- ret_file: a file contained the docid and retrievability scores for each item, one per line, tab/space sep.
- out_file: the name of the file which will store the re-ranking in TREC format
- k: the number of items to re-rank
- lam: the amount of adjustment

```
python rerank.py bm25.baseline.wapo-2018.res ret-scores-ra0.5.ret out-ra-50-0.9.res 50 0.9  
```

This will re-rank the top 50 per topic with lambda = 0.9

## Retrievability Calculator
Use `calculator.py` to compute the retrievability scores for each document. 

The `calculator.py` takes:
- result_file: TREC formatted
- out_file: the output file with contain the docid and retrievability scores for each item, one per line, tab/space sep.
- c: the cutoff
- b: the discount for gravity, set to 0.0 for cumulative scores

**Update to include a corpus file so that it outputs a value for each document, regardless of whether it has been
returned as a result or not.**


## Gini 

Use `gini.py` to calculate the gini cofficient for a given retrievability file.