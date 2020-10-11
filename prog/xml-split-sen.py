from argparse import ArgumentParser
from ucca.constructions import extract_candidates, add_argument
from ucca.convert import *
from ucca.ioutil import get_passages, get_passages_with_progress_bar, external_write_mode

def main(args):

    for passage in get_passages_with_progress_bar(args.passages):
        t = split2sentences(passage)
        for sen in t:
            passage2file(sen, sen.ID+'.xml', indent=True, binary=False)



if __name__ == "__main__":
    argparser = ArgumentParser(description="Xml to conll and find the path of the word from UCCA xml file.")
    argparser.add_argument("passages", nargs="+", help="the corpus, given as xml/pickle file names")
    add_argument(argparser, False)
    main(argparser.parse_args())
