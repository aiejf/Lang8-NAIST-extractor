import argparse
import codecs
import json
import re

language = ['English', 'Japanese', 'Korean']
tags = ["f-red", "f-blue", "f-bold"]

def main():
    args = parse_args()
    data_num = 0
    error_num = 0
    with codecs.open(args.data_path, 'r', encoding='utf8') as f:
        for line in f:
            data_num += 1
            try:
                jsonData = json.loads(line, strict=False)
                l2_lang, l1_lang = jsonData[2], jsonData[3]
                orig_sents, corr_sents = jsonData[4], jsonData[5]
                if (args.l1 == None or args.l1 == l1_lang) and args.l2 == l2_lang:
                    outputs = make_sent_pair(orig_sents, corr_sents, args)
                    for output in outputs:
                        print(output)
            except:
                error_num += 1
                pass

def make_sent_pair(orig_sents, corr_sents, args):
    outputs = []
    for i, orig_sent in enumerate(orig_sents):
        if len(corr_sents[i]) > 0:
            for corr_sent in corr_sents[i]:
                text, tag_err = delete_tags(corr_sent, args)
                if not tag_err:
                    output = orig_sent + "\t" + text
                    outputs.append(output)
        else:
            output = orig_sent + "\t" + orig_sent
            outputs.append(output)

    return outputs

def delete_tags(text, args):
    if args.tags:
        return text
    text = replace_tags(text)

    tag_err = False
    if text == None:
        text = ""
    for tag in tags:
        s = "\[" + tag + "\]"
        e = "\[\/" + tag + "\]"
        text = re.sub(r"%s" % s, r"", text)
        text = re.sub(r"%s" % e, r"", text)
        if tag in text:
            tag_err = True
    text = re.sub(r"\[sline\](.+?)\[\/sline\]", r"", text)

    text = re.sub(r'^\s+', '', text)
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text, tag_err

def replace_tags(s):
    s = s.replace("[赤]", "[f-red]")
    s = s.replace("[/赤]", "[/f-red]")
    s = s.replace("[青]", "[f-blue]")
    s = s.replace("[/青]", "[/f-blue]")
    return s

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", dest="data_path", type=str, metavar='<str>', required=True, help="The path to the data set")
    parser.add_argument("-l2", "--learn-lang", dest="l2", type=str, metavar='<str>', required=False, default='English', help="L2 language")
    parser.add_argument("-l1", "--native-lang", dest="l1", type=str, metavar='<str>', required=False, default=None, help="L1 language")
    parser.add_argument("-tags", "--remain-tags", dest="tags", default=False, action='store_true', help="If you want to remain tags (e.g. [f-red]), please use this option")

    args = parser.parse_args()

    assert args.l2 in language
    if args.l1 != None:
        assert args.l1 in language

    return args


if __name__ == "__main__":
    main()