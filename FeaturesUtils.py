import re


class FeaturesUtils:
    @staticmethod
    def all_suffixes(word, num=4):
        if num > len(word):
            num = len(word)
        return [word[-i:] for i in range(1, num + 1)]

    @staticmethod
    def all_prefixes(word, num=4):
        if num > len(word):
            num = len(word)
        return [word[:i + 1] for i in range(num)]

    @staticmethod
    def add_prefixes_features(feature_dict, word, type_word_string):
        prefixes = FeaturesUtils.all_prefixes(word)
        for i in range(len(prefixes)):
            feature_dict['{0}_pref_{1}'.format(type_word_string, i + 1)] = prefixes[i]

    @staticmethod
    def add_suffixes_features(feature_dict, word, type_word_string):
        suffixes = FeaturesUtils.all_suffixes(word)
        for i in range(len(suffixes)):
            feature_dict['{0}_suff_{1}'.format(type_word_string, i + 1)] = suffixes[i]

    @staticmethod
    def is_contains_number(word):
        re.match(r'.*\d.*', word)

    @staticmethod
    def is_contains_uppercase(word):
        re.match(r'.*[A-Z].*', word)

    @staticmethod
    def is_contains_hyphen(word):
        re.match(r'.*-.*', word)

    @staticmethod
    def add_rare_word_features(feature_dict, word):
        if FeaturesUtils.is_contains_number(word):
            feature_dict['contains_number'] = 'True'
        if FeaturesUtils.is_contains_uppercase(word):
            feature_dict['contains_uppercase'] = 'True'
        if FeaturesUtils.is_contains_hyphen(word):
            feature_dict['contains_hyphen'] = 'True'

    @staticmethod
    def add_prev_tags_features(feature_dict, i, tags_list):
        if i > 0:
            prev_tag = tags_list[i - 1]
            feature_dict['pt'] = prev_tag
            if i > 1:
                prev_prev_tag = tags_list[i - 2]
                feature_dict['ppt'] = prev_prev_tag
                feature_dict['ppt_pt'] = '{0},{1}'.format(prev_prev_tag, prev_tag)

    @staticmethod
    def add_prev_next_words(feature_dict, i, words_list):
        if i + 1 < len(words_list):
            FeaturesUtils.features(feature_dict, words_list[i + 1], 'nw')
            if i + 2 < len(words_list):
                FeaturesUtils.features(feature_dict, words_list[i + 2], 'nnw')

        if i > 0:
            FeaturesUtils.features(feature_dict, words_list[i - 1], 'pw')
            if i > 1:
                FeaturesUtils.features(feature_dict, words_list[i - 1], 'ppw')

    @staticmethod
    def add_any_word_features(feature_dict, i, tags_list, words_list):
        FeaturesUtils.features(feature_dict, words_list[i], 'curr')
        FeaturesUtils.add_prev_tags_features(feature_dict, i, tags_list)
        FeaturesUtils.add_prev_next_words(feature_dict, i, words_list)

    @staticmethod
    def get_word_features(i, words_list, tags_list, is_rare):
        feature_dict = dict()
        if is_rare:
            FeaturesUtils.add_rare_word_features(feature_dict, words_list[i])
        else:
            feature_dict['form'] = words_list[i]
        FeaturesUtils.add_any_word_features(feature_dict, i, tags_list, words_list)

        return feature_dict

    @staticmethod
    def features(feature_dict, word, type_word_string):
        FeaturesUtils.add_prefixes_features(feature_dict, word, type_word_string)
        FeaturesUtils.add_suffixes_features(feature_dict, word, type_word_string)
        feature_dict[type_word_string + '_len'] = str(len(word))
