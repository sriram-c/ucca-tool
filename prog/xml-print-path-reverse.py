import sys
from argparse import ArgumentParser
from ucca.constructions import extract_candidates, add_argument
import xml.etree.ElementTree as ETree
from ucca import layer0, layer1, convert, textutil
from operator import attrgetter, itemgetter
from ucca.convert import split2sentences
from ucca.ioutil import get_passages, get_passages_with_progress_bar, external_write_mode
import re



descr = {'Q':'Unknown', 'T':'Unknown', 'Terminal':'Terminal_node','P':'Process' ,'S':'State', 'A':'Participant', 'D':'Adverbial', 'C':'Center', 'E':'Elaborator', 'N':'Connector', 'R':'Relator', 'H':'Parallel_Scene', 'L':'Linker' ,'G':'Ground', 'F':'Function', 'U':'Punctuation'
}

def find_path(node,path):
        if(len(node.parents) >= 1):
            if(node.tag != 'Word') and (node.tag != 'Punctuation'):
                #path.append(node.ID+'--'+node.ftag+':'+descr[node.ftag]+'-->'+node.parents[0].ID)
                path.append(('-->('+node.ftag+':'+descr[node.ftag]+')-->'+node.parents[0].ID))
            else:
                #path.append(node.text+'--'+'Terminal'+'-->'+node.parents[0].ID)
                path.append((node.text+'('+str(node.ID)+')'+'--Terminal-->'+node.parents[0].ID))
            for j in node.parents:
                find_path(j,path)
        return path


def find_children(node, path, level):
    for ch in node.children:
        if (ch.tag != 'Word') and (ch.tag != 'Punctuation'):
            path.append((ch.ftag, ch.ID, level+1))
            find_children(ch, path, level+1)
        else:
            path.append((ch.text, ch.ID, level+1))
            path.append('End')

    return path




def main(args):

    for passage in get_passages_with_progress_bar(args.passages):
        t = split2sentences(passage)
        sen_no = 0
        for sen in t:
            #print('sentence %d\n\n%s\n%s' %(i,convert.to_text(sen), convert.to_sequence(sen)))
            print('sentence %d\n\n%s\n' %(sen_no, convert.to_text(sen)))

            root = sen.nodes['1.1']
            for i in root.children:
                path = []
                level = 1
                path.append((i.ftag, i.ID, level))
                path = find_children(i, path, level)
                pstr = root.ID
                end = 0
                tab_len = {}
                for j in path:
                    if(j == 'End'):
                        print(pstr)
                        pstr = ''
                        end = 1
                        continue
                    rel = j[0]
                    nd = j[1]
                    tab = int(j[2])
                    if(end):
                        for k in range(0,tab_len[tab-1]):
                            pstr = pstr+' '
                            end = 0
                    if(rel in descr):
                        rel_desc = rel+':' +descr[rel]
                    else:
                        rel_desc = rel
                    pstr = pstr+'|-->('+rel_desc+')-->'+nd
                    tab_len[tab] = len(pstr)

            print('-----------------------------------\n')
            sen_no += 1



if __name__ == "__main__":
    argparser = ArgumentParser(description="Xml to conll and find the path of the word from UCCA xml file.")
    argparser.add_argument("passages", nargs="+", help="the corpus, given as xml/pickle file names")
    add_argument(argparser, False)
    main(argparser.parse_args())
