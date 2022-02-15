# AUTHOR: Leif Azzopardi
# 13-02-2022
# calculate the gini coefficient give the retrievability file

import os
import argparse
from collections import defaultdict

def check_file_exists(filename):
    if filename and not os.path.exists(filename):
        print("{0} Not Found".format(filename))
        quit(1)


def calculate_gini(list_of_values):
    # https://planspace.org/2013/06/21/how-to-calculate-gini-coefficient-from-raw-data-in-python/
    sorted_list = sorted(list_of_values)
    height, area = 0, 0
    for value in sorted_list:
        height += value
        area += height - value / 2.
    fair_area = height * len(list_of_values) / 2.
    return (fair_area - area) / fair_area


def process_results(ret_file):
    ret_scores = []
    ret_total = 0.0
    with open(ret_file, "r") as rf:
        while rf:
            line = rf.readline().strip()
            if not line:
                break
            (doc_id, score) = line.split('\t')
            doc_id = doc_id.strip()
            score = float(score.strip())
            ret_scores.append(score)
            ret_total += score
        rf.close()
    print(f'Read in {len(ret_scores)} scores.')
    print(f'Total Retrievability Mass: {ret_total:.4f}')
    g = calculate_gini(ret_scores)
    print(f'Gini Cofficient is: {g:.4f}')



def parse_args():
    arg_parser = argparse.ArgumentParser(description="Gini Cofficient Calculator")
    arg_parser.add_argument("ret_file", help="A retrievability file. Two colum tab/space sep file with fields:"
                                             "doc_id retrievability_score")
    args = arg_parser.parse_args()
    return args


def main(ret_file):
    print(f'About to compute the Gini given the retrievability file {ret_file}')
    process_results(ret_file)
    print(f'Done!')


if __name__ == '__main__':
    args = parse_args()
    check_file_exists(args.ret_file)
    main(args.ret_file)