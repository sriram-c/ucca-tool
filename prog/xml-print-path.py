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
                path.append((node.text+'--Terminal-->'+node.parents[0].ID))
            for j in node.parents:
                find_path(j,path)
        return path



def main(args):

    for passage in get_passages_with_progress_bar(args.passages):
        t = split2sentences(passage)
        i = 0
        for sen in t:
            #print('sentence %d\n\n%s\n%s' %(i,convert.to_text(sen), convert.to_sequence(sen)))
            print('sentence %d\n\n%s\n' %(i,convert.to_text(sen)))
            i +=1
            compunds = []
            for node in sen.nodes:
                if(sen.nodes[node].layer.ID == '0'):
                    find_id = ''
                    l = sen.nodes[node]
                    if(l.parents[0].ftag == 'C'):
                        if (l.parents[0].ID not in compunds):
                            compunds.append(l.parents[0].ID)
                            tmp_c = []
                            for n in l.parents[0].children:
                                tmp_c.append(n.text)
                            #print('Word: %s\nWord ID: %s' %(tmp_c,l.parents[0].ID))
                            find_id = l.parents[0].ID
                            path = []
                            path.append(' '.join(tmp_c))
                            path = find_path(sen.nodes[find_id], path)
                            print(' '.join(path))
                            '''
                            for j in path:
                                print(j)
                            '''
                            print('-------')

                    else:
                        #print('Word: %s\nWord ID: %s' % (l.text, l.ID))
                        find_id = l.ID
                        path = []
                        path = find_path(sen.nodes[find_id],path)
                        print(' '.join(path))
                        '''
                        for j in path:
                            print(j)
                        '''
                        print('-------')
            print('------------------------------------------------------------------')


if __name__ == "__main__":
    argparser = ArgumentParser(description="Xml to conll and find the path of the word from UCCA xml file.")
    argparser.add_argument("passages", nargs="+", help="the corpus, given as xml/pickle file names")
    add_argument(argparser, False)
    main(argparser.parse_args())
