# AUTHOR: Leif Azzopardi
# 13-02-2022
# calculate the retrievability scores for authors

import os
import argparse
from collections import defaultdict

def check_file_exists(filename):
    if filename and not os.path.exists(filename):
        print("{0} Not Found".format(filename))
        quit(1)

def read_mapping(key_val_file):
    mapping = dict()
    with open(key_val_file, "r") as rf:
        while rf:

            line = rf.readline().strip()
            if not line:
                break
            vals = line.split()
            key = vals[0].strip()
            val = ' '.join(vals[1:]).strip()
            mapping[key] = val

    return mapping


def process_results(ret_file, doc_author_file,  out_file):

    doc_author_dict = read_mapping(doc_author_file)

    rets = defaultdict(float)

    with open(ret_file, "r") as rf:
        while rf:
            line = rf.readline().strip()
            if not line:
                break
            (doc_id, score) = line.split()
            doc_id = doc_id.strip()
            score = float(score.strip())
            author = doc_author_dict[doc_id]
            rets[author] += score

        rf.close()

    with open(out_file, "w") as of:
        for author, ret_score in rets.items():
            of.write(f'{author}\t{ret_score:.4f}{os.linesep}')

        of.close()


def parse_args():
    arg_parser = argparse.ArgumentParser(description="Author Retrievability Calculator")
    arg_parser.add_argument("ret_file",
                            help="A retrievability file. Two column tab/space sep file with fields:"
                                 "doc_id retrievability_score")

    arg_parser.add_argument("doc_author_file",
                            help="A document author mapping. Two column tab/space sep file with fields:"
                                 "doc_id author_name")

    arg_parser.add_argument("out_file", help="A retrievability file. Two column tab/space sep file with fields:"
                                             "author_name retrievability_score")

    args = arg_parser.parse_args()
    return args


def main(ret_file, doc_author_file, out_file='out.ret'):
    print(f'About to compute there retrievability for authors'
          f' on using the retrievability scores from: {ret_file} '
          f'using the mapping of doc to authors from: {doc_author_file} '
          f'and will save the author retrievability scores to: {out_file}')
    process_results(ret_file, doc_author_file, out_file)
    print(f'Results written to: {out_file}')
    print(f'Done!')


if __name__ == '__main__':
    args = parse_args()
    check_file_exists(args.ret_file)
    check_file_exists(args.doc_author_file)
    main(args.ret_file, args.doc_author_file, args.out_file)