# AUTHOR: Leif Azzopardi
# 13-02-2022
# transform the retrievability scores

import os
import argparse

from collections import defaultdict


def check_file_exists(filename):
    if filename and not os.path.exists(filename):
        print("{0} Not Found".format(filename))
        quit(1)


def k_smooth_score(score, k):
    new_score = ((k+1.0) * score )/ (k + score)
    return new_score


def process_results(ret_file, out_file, k):
    of = open(out_file, "w")
    old_score_total = 0
    new_score_total = 0
    with open(ret_file, "r") as rf:
        while rf:
            line = rf.readline().strip()
            if not line:
                break
            (doc_id, score) = line.split('\t')
            doc_id = doc_id.strip()
            score = float(score.strip())
            new_score = k_smooth_score(score, k)
            old_score_total += score
            new_score_total += new_score
            of.write(f'{doc_id}\t{new_score:.4f}{os.linesep}')
        rf.close()
    of.close()
    print(f'Total Retrievability mass: {old_score_total}')
    print(f'New Total Retrievability mass: {new_score_total}')


def parse_args():
    arg_parser = argparse.ArgumentParser(description="Retrievability Transformer")
    arg_parser.add_argument("ret_file", help="A retrievability file. Two colum tab/space sep file with fields:"
                                             "doc_id retrievability_score")
    arg_parser.add_argument("out_file", help="A retrievability file where the scores are transformed. "
                                             "Two colum tab/space sep file with fields:"
                                             "doc_id retrievability_score")
    arg_parser.add_argument("k", help="The k transformer parameter", type=float)
    args = arg_parser.parse_args()
    return args


def main(ret_file, out_file, k):
    print(f'About to transform the retrievability file {ret_file} using {k}')
    process_results(ret_file, out_file, k)
    print(f'Done!')


if __name__ == '__main__':
    args = parse_args()
    check_file_exists(args.ret_file)
    main(args.ret_file, args.out_file, args.k)