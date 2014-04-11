#!/usr/bin/env python

import sys
import pprint

def main():

    if len(sys.argv) < 5 or len(sys.argv) > 6:
      print sys.argv[0] + " scores_file_1.txt scores_file_2.txt [append | replace] id poz"
      sys.exit()
    elif sys.argv[3] == "replace":
      if len(sys.argv) != 5:
        print sys.argv[0] + " scores_file_1.txt scores_file_2.txt replace id"
        sys.exit()
    elif sys.argv[3] == "append":
      if len(sys.argv) != 6:
        print sys.argv[0] + " scores_file_1.txt scores_file_2.txt append id poz"
        poz = int(sys.argv[5])
        sys.exit()

    id = sys.argv[4]

    header = open(sys.argv[1], "r").readline().strip().split("\t")

    # header.strip().split("\t").index(id)
    first = {}
    for line in open(sys.argv[1], "r").readlines()[1:]:
        fields = line.strip().split("\t")
        first[fields[-4]] = fields

    header2 = open(sys.argv[2], "r").readline();
    index2 = header2.strip().split("\t").index(id)

    second = {}
    for line in open(sys.argv[2], "r").readlines()[1:]:
        fields = line.strip().split("\t")
        second[fields[-4]] = fields

    nrElems = len(header) - 4

    grouped = {}
    for key in first:
        assert key in second

        if sys.argv[3] == "append":
            grouped[key] = first[key]

            grouped[key][0] = int(first[key][0]) + int(second[key][index2])
            grouped[key].insert(poz, second[key][index2])
        elif sys.argv[3] == "replace":
            index1 = header.index(id)

            grouped[key] = first[key]
            grouped[key][0] = int(grouped[key][0]) + int(second[key][index2]) - \
                int(first[key][index1])
            grouped[key][index1] = second[key][index2]

    if sys.argv[3] == "append":
        header.insert(poz, id)
    print "\t".join(header)

    scores = sorted(grouped.itervalues(), key=lambda x: -x[0])
    for score in scores:
        print "\t".join([str(x) for x in score])

if __name__ == "__main__":
    main()
