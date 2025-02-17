import sys
from datetime import datetime

import numpy as np

import MLETrain
from DictUtils import DictUtils
from FileUtils import FileUtils
from WordSignature import WordSignatures

START = 'START'
UNK = '*unk*'


def get_words(sentence):
    return sentence.split(' ')


def get_word_signatures_tag(word, dict_e, unk_tag_list):
    signatures = WordSignatures.get_word_signatures(word)
    if signatures == [word.lower()]:
        return {UNK: unk_tag_list}
    else:
        signatures_tags = dict()
        for signature in signatures:
            signatures_tags[signature] = DictUtils.possible_tags(signature, dict_e)
        return signatures_tags


def possible_tags(word, dict_e, unk_tag_list):
    words_tags = DictUtils.possible_tags(word, dict_e)
    if len(words_tags) == 0:
        return get_word_signatures_tag(word, dict_e, unk_tag_list)
    else:
        return {word: words_tags}


def max_prob_and_tag(v_table, i, w_i, tag, prev_tag, prev_prev_tags, dict_q, dict_e):
    max_prob = -np.inf
    max_tag = prev_prev_tags[0]
    for prev_prev_tag in prev_prev_tags:
        prob = v_table[(i - 1, prev_prev_tag, prev_tag)] + MLETrain.get_score(w_i.lower(), tag, prev_tag, prev_prev_tag,
                                                                              dict_q, dict_e)
        if prob > max_prob:
            max_prob = prob
            max_tag = prev_prev_tag

    return max_prob, max_tag


def calc_v_table_at_i(v_table, bq, i, dict_tags, prev_tags, prev_prev_tags, dict_q, dict_e, unk_tag_list):
    for word, tags in dict_tags.items():
        for tag in tags:
            for prev_tag in prev_tags:
                max_prob, max_tag = max_prob_and_tag(v_table, i, word, tag, prev_tag, prev_prev_tags, dict_q, dict_e)
                v_table[(i, prev_tag, tag)] = max_prob
                bq[(i, prev_tag, tag)] = max_tag


def get_backtrack(v_table, bq, words):
    n = len(words) - 1
    y_n = ''
    y_n_1 = ''
    max_prob = -np.math.inf

    for key, value in v_table.items():
        if key[0] == n and max_prob < value:
            max_prob = value
            y_n = key[2]
            y_n_1 = key[1]

    if n == 0:
        tagged_line = [(words[-1], y_n)]
    else:
        tagged_line = [(words[-2], y_n_1), (words[-1], y_n)]
        for i in reversed(range(n - 1)):
            y_i = bq[(i + 2, y_n_1, y_n)]
            tagged_line.insert(0, (words[i], y_i))
            y_n = y_n_1
            y_n_1 = y_i

    return tagged_line


def viterbi(sentences, dict_q, dict_e, unk_tag_list):
    tagged_text = list()
    for sentence in sentences:
        words = get_words(sentence)

        v_table = {(-1, START, START): 1}
        bq = dict()
        prev_tags = [START]
        prev_prev_tags = [START]
        for i in range(len(words)):
            w_i = words[i]
            dict_tags = possible_tags(w_i, dict_e, unk_tag_list)
            calc_v_table_at_i(v_table, bq, i, dict_tags, prev_tags, prev_prev_tags, dict_q, dict_e, unk_tag_list)

            prev_prev_tags = prev_tags
            prev_tags = []
            for list_tags in dict_tags.values():
                prev_tags += list_tags

        tagged_line = get_backtrack(v_table, bq, words)

        print(tagged_line)
        tagged_text.append(tagged_line)
    return tagged_text


def main(input_file_name, q_mle, e_mle, hmm_viterbi_predictions, extra_file_name):
    start = datetime.now()

    sentences = FileUtils.read_lines(input_file_name)
    dict_q = DictUtils.convert_line_to_dict(FileUtils.read_lines(q_mle))
    dict_e = DictUtils.convert_line_to_dict(FileUtils.read_lines(e_mle))
    unk_tag_list = DictUtils.possible_tags('*UNK*', dict_e)
    tagged_text = viterbi(sentences, dict_q, dict_e, unk_tag_list)
    FileUtils.write_tagged_text(hmm_viterbi_predictions, tagged_text)

    end = datetime.now()
    print('Running Time: {0}'.format(end - start))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
