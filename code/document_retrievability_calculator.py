# AUTHOR: Leif Azzopardi
# 13-02-2022
# calculate the retrievability scores given the res file

import os
import argparse
from collections import defaultdict

def check_file_exists(filename):
    if filename and not os.path.exists(filename):
        print("{0} Not Found".format(filename))
        quit(1)


def process_results(result_file,  out_file, c, b):
    rets = defaultdict(float)
    with open(result_file, "r") as rf:
        while rf:
            line = rf.readline().strip()
            if not line:
                break
            (topic_id, element_type, doc_id, rank, score, run_id) = line.split()
            doc_id = doc_id.strip()
            score = float(score.strip())
            rank = int(rank.strip())
            if rank <= c:
                rets[doc_id] += (1.0 / (rank**b))

        rf.close()

    with open(out_file, "w") as of:
        for doc_id, ret_score in rets.items():
            of.write(f'{doc_id}\t{ret_score:.4f}{os.linesep}')

        of.close()


def parse_args():
    arg_parser = argparse.ArgumentParser(description="Document Retrievability Calculator")
    arg_parser.add_argument("result_file",
                            help="TREC formatted results file. Six column tab/space sep file with fields:"
                                 " topic_id element_type doc_id rank score run_id.")
    arg_parser.add_argument("out_file", help="A retrievability file. Two colum tab/space sep file with fields:"
                                             "doc_id retrievability_score")
    arg_parser.add_argument("c", help="Cut off", type=int)
    arg_parser.add_argument("b", help="Beta", type=float)

    args = arg_parser.parse_args()
    return args


def main(result_file, out_file='out.ret', c=50, b=0.0):
    print(f'About to compute there retrievability'
          f' on result file: {result_file} and will save the retrievability scores to: {out_file}')
    if b==0.0:
        print(f'Calculating the cumulative score with cut off: {c}')
    else:
        print(f'Calculating the gravity score with discount: {b} and cut off: {c}')
    process_results(result_file, out_file, c, b)
    print(f'Results written to: {out_file}')
    print(f'Done!')


if __name__ == '__main__':
    args = parse_args()
    check_file_exists(args.result_file)
    main(args.result_file, args.out_file, args.c, args.b)