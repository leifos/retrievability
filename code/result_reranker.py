# AUTHOR: Leif Azzopardi
# 12-02-2022
# Reranking result runs using retrievability scores

import os
import argparse


def check_file_exists(filename):
    if filename and not os.path.exists(filename):
        print("{0} Not Found".format(filename))
        quit(1)


def read_ret_file(ret_file):
    rets = dict()
    with open(ret_file, "r") as cf:
        while cf:
            line = cf.readline().strip()
            if not line:
                break
            (doc_id, ret_score) = line.split()
            doc_id = doc_id.strip()
            rets[doc_id] = float(ret_score)
    return rets


def get_max(rets):
    max_ret = 0
    for key,val in rets.items():
        if val > max_ret:
            max_ret = val
    return max_ret


def rerank(doc_list, rets, k, lam):
    max_ret = get_max(rets)
    max_ret_lam = max_ret * lam

    reranking = []
    for i,doc in enumerate(doc_list):
        if i <= k:
            doc_ret_score = rets.get(doc[0], 0.0)
            # to make sure that the updated scores are not lower than the kth + scores,
            # we add the maximum adjustment possible, and then decrease the score for the doc.

            new_doc_score = float(doc[1]) + max_ret_lam - (doc_ret_score*lam)
            reranking.append( (doc[0], new_doc_score) )
        else:
            reranking.append(doc)

    # resort the list in descending order --- bigggest score to the smallest.
    reranking.sort(key=lambda x:x[1], reverse=True )

    return reranking


def do_reranking(out_file_handler, topic_id, doclist, rets, run_id, k, lam):
    print(f'Reranking Topic: {topic_id}')
    # Perform the re-ranking for the curr_topic_id, current_topic_doclist
    reranked_list = rerank(doclist, rets, k=k, lam=lam)
    # output the re-ranking to the outfile
    for i, doc in enumerate(reranked_list):
        rank = i+1
        out_file_handler.write(f'{topic_id} Q1 {doc[0]} {rank} {doc[1]} {run_id}-rr-k{k}-lam{lam}\n')


def process_results(result_file, rets, out_file, k, lam):
    curr_topic_id = None
    curr_topic_doclist = []
    of = open(out_file, "w")

    with open(result_file, "r") as rf:
        while rf:
            line = rf.readline().strip()
            if not line:
                # before we stop, peform the re-ranking for the final topic
                do_reranking(of, curr_topic_id, curr_topic_doclist, rets, run_id, k, lam)
                break
            (topic_id, element_type, doc_id, rank, score, run_id) = line.split()
            doc_id = doc_id.strip()
            score = float(score.strip())
            if topic_id == curr_topic_id:
                # add doc and score to list
                curr_topic_doclist.append((doc_id, score))
            else:
                if curr_topic_id is not None:
                # do the re ranking for the current topic, before moving to the next one
                    do_reranking(of, curr_topic_id, curr_topic_doclist, rets, run_id, k, lam)
                # reset for the new topic
                curr_topic_id = topic_id
                curr_topic_doclist = [(doc_id, score)]
    rf.close()
    of.close()


def parse_args():
    arg_parser = argparse.ArgumentParser(description="Reranker")
    arg_parser.add_argument("result_file",
                            help="TREC formatted results file. Six column tab/space sep file with fields:"
                                 " topic_id element_type doc_id rank score run_id.")
    arg_parser.add_argument("ret_file", help="A retrievability file. Two colum tab/space sep file with fields:"
                                             "doc_id retrievability_score")

    arg_parser.add_argument("out_file", help="Outputs a TREC formmatted results file.")
    arg_parser.add_argument("k", help="Number of results to re-rank", type=int)
    arg_parser.add_argument("lam", help="Lambda", type=float)

    args = arg_parser.parse_args()
    return args


def main(result_file, ret_file, out_file='out.res', k=50, lam=0.5):
    print(f'About to re-rank: {result_file} using the retrievability scores from: {ret_file}')
    rets = read_ret_file(ret_file)
    print(f'Read in {len(rets)} retrievability scores.')
    print(f'About to process the files and re-rank with k={k} and lambda={lam}')
    process_results(result_file, rets, out_file, k, lam)
    print(f'Results written to: {out_file}')
    print(f'Done!')


if __name__ == '__main__':
    # performance_main()
    args = parse_args()
    check_file_exists(args.result_file)
    check_file_exists(args.ret_file)
    main(args.result_file, args.ret_file, args.out_file, args.k, args.lam)