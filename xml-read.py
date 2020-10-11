import sys
from argparse import ArgumentParser
from ucca.constructions import extract_candidates, add_argument
import xml.etree.ElementTree as ETree
from ucca import layer0, layer1, convert, textutil
from operator import attrgetter, itemgetter
from ucca.convert import split2sentences
from ucca.ioutil import get_passages, get_passages_with_progress_bar, external_write_mode
import re



descr = { 'T':'unknown','Terminal':'Terminal_node','P':'Process' ,'S':'State', 'A':'Participant', 'D':'Adverbial', 'C':'Center', 'E':'Elaborator', 'N':'Connector', 'R':'Relator', 'H':'Parallel_Scene', 'L':'Linker' ,'G':'Ground', 'F':'Function', 'U':'Punctuation'
}
def load_xml(path):
    """XML file path ==> root element
    :param path: path to XML file
    """
    with open(path, encoding="utf-8") as f:
        return ETree.ElementTree().parse(f)

def xmltoconll(passage):
    words = {}
    for layer in sorted(passage.layers, key=attrgetter('ID')):
        if(layer.ID == '0'):
            print("Layer 0\n------\n")
            print('WordID, ParagraphID, Paragraph_Position, Text, Pos_Tag')
            for data in layer.all:
                print(data.ID,data.paragraph, data.para_pos, data.text, data.tag)
                words[data.ID] = data.text
        elif(layer.ID == '1'):
            print("\nLayer 1\n------\n")
            for data in layer.all:
                for l in data.outgoing:
                    if(l.tag == 'Terminal'):
                        #print(data.tag, data.ID, l.child.text, l.tag)
                        continue
                    else:
                        if l.tag in descr:
                            tag_tmp = descr[l.tag]
                        else:
                            tag_tmp = 'unknown'
                        if(len(l.child.terminals) >= 1):
                            tmp_wd = []
                            for k in l.child.terminals:
                                tmp_wd.append(k.text)

                            #print(data.tag, data.ID, l.child.ID+":"+l.child.terminals[0].text, l.tag+':'+tag_tmp)
                            print(data.tag, data.ID, l.child.ID+":"+' '.join(tmp_wd), l.tag+':'+tag_tmp)
                        else:
                            print(data.tag, data.ID, l.child.ID, l.tag+':'+tag_tmp)

def find_path(node,path):
        if(len(node.parents) >= 1):
            if(node.tag != 'Word'):
                path.append(node.ID+'--'+node.ftag+':'+descr[node.ftag]+'-->'+node.parents[0].ID)
            else:
                path.append(node.text+'--'+'Terminal'+'-->'+node.parents[0].ID)
            for j in node.parents:
                print(path)
                find_path(j,path)
        return path



def main(args):

    for passage in get_passages_with_progress_bar(args.passages):
        #passage = convert.from_standard(elem)
        #print("Linearised\n------\n")
        # print(convert.to_sequence(passage))
        words = {}
        xmltoconll(passage)
        t = split2sentences(passage)
        i = 0
        for sen in t:
            print('sentence %d\n\n%s\n' %(i,convert.to_text(sen)))
            i +=1

        while(1):
            word = input('\nType the word below\n\n')
            for node in passage.nodes:
                t = passage.nodes[node]
                if(re.match(rf'\b{word}\b',t.text, re.IGNORECASE)):
                    print('Word: %s\nWord ID: %s' %(t.text,t.ID))
                    #ans = input('\nDo you want to continue with wordi Id : %s', t.ID)
                    path = []
                    path = find_path(passage.nodes[t.ID],path)
                    break
            for i in path:
                print(i)


if __name__ == "__main__":
    argparser = ArgumentParser(description="Xml to conll and find the path of the word from UCCA xml file.")
    argparser.add_argument("passages", nargs="+", help="the corpus, given as xml/pickle file names")
    add_argument(argparser, False)
    main(argparser.parse_args())
