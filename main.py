import srt
import string
import sys
import re

from os.path import isfile, join
from collections import Counter


def get_file_lines_set(in_file: str) -> set:
    assert isfile(in_file)
    with open(in_file, 'r') as file:
        return set(file.read().splitlines())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Wrong args")

    input_sub_file = sys.argv[1]
    assert isfile(input_sub_file)

    known_words_file = "known_words.txt"
    known_names_file = "known_names.txt"
    english_words_file = join("english-words", "words.txt")

    known_words = get_file_lines_set(known_words_file)
    known_names = get_file_lines_set(known_names_file)
    english_words = get_file_lines_set(english_words_file)

    with open(input_sub_file, 'r') as file:
        data = file.read()

        subs = [re.sub(r"(<br/>|\n|♪)", "", c.content) for c in srt.parse(data)]

        text_list = []
        text_set = set()
        for s in subs:
            s = s.replace("'s", "").lower()  # no English possessive
            s = ''.join([i for i in s if not i.isdigit()])  # no digits
            s = s.translate(str.maketrans('', '', string.punctuation))  # no punctuation
            str_list = list(filter(None, s.split(" ")))
            text_list.extend(str_list)
            text_set.update(set(text_list))

        unknown_set = text_set - known_words - known_names
        c = Counter(text_list)
        for e in c.most_common():
            word = e[0]
            if word in unknown_set and word in english_words and len(word) > 1:
                print(e[1], word, "\t", "https://www.wordreference.com/enit/"+word, "\t", "https://www.wordreference.com/ende/"+word)
                #print(word)
