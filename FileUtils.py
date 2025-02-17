import pickle


class FileUtils:

    @staticmethod
    def read_lines(file_name):
        lines = []
        with open(file_name, 'r') as file:
            for line in file:
                lines.append(line)
        return [line.strip() for line in lines]

    @staticmethod
    def read_sentences(file_name):
        sentences = list()
        max_sentence_len = 0
        with open(file_name, 'r') as file:
            for sentence in file:
                sentences.append(list())
                words = sentence.strip().split(" ")
                for word in words:
                    sentences[-1].append(word)
                if len(sentences[-1]) > max_sentence_len:
                    max_sentence_len = len(sentences[-1])
        return sentences, max_sentence_len

    @staticmethod
    def add_new_features(all_tags_features, tag, tag_features):
        if tag not in all_tags_features.keys():
            all_tags_features[tag] = list()
        all_tags_features[tag].append(tag_features)

    @staticmethod
    def read_features(file_name):
        labels = list()
        all_features = list()
        with open(file_name, 'r') as file:
            for line in file:
                line = line.strip().split(' ')
                labels.append(line[0])
                features_dict = dict()
                for feature in line[1:]:
                    feature_key, feature_value = feature.split('=', 1)
                    features_dict[feature_key] = feature_value

                all_features.append(features_dict)

        return all_features, labels

    @staticmethod
    def write_events_count(file_name, dictionary):
        with open(file_name, 'w') as mle_file:
            for key, value in dictionary.items():
                if isinstance(key, tuple):
                    mle_file.write('{0}\t{1}\n'.format(' '.join(str(x) for x in key), value))
                else:
                    mle_file.write('{0}\t{1}\n'.format(key, value))

    @staticmethod
    def write_tagged_text(file_name, tagged_text):
        with open(file_name, 'w') as file:
            for tagged_sentence in tagged_text:
                tuples = ['{0}/{1}'.format(tuple[0], tuple[1]) for tuple in tagged_sentence]
                file.write(' '.join(tuples) + '\n')

    @staticmethod
    def write_features(file_name, features):
        with open(file_name, 'w') as file:
            for word_feature_dict in features:
                line = word_feature_dict['tag']
                for feature_key, feature_value in word_feature_dict.items():
                    if feature_key != 'tag':
                        line += ' {0}={1}'.format(feature_key, feature_value)

                file.write(line + '\n')

    @staticmethod
    def write_logistic_regression_model(file_name, model):
        # print to model_file
        with open(file_name, "wb") as file:
            pickle.dump(model, file, fix_imports=True)

    @staticmethod
    def read_logistic_regression_model(file_name):
        with open(file_name, 'rb') as model_file:
            (clf, vec) = pickle.load(model_file)
        return clf, vec

    @staticmethod
    def write_feature_map(feature_map_file, features_map, counters_dict):
        with open(feature_map_file, "w") as file:
            for index in range(len(features_map)):
                file.write('{0} : {1} \n'.format(features_map[index], index))

            for word, counter in counters_dict.items():
                file.write('{0}={1}\n'.format(word, counter))

    @staticmethod
    def write_prediction(file_name, sentences, sentences_predictions):
        with open(file_name, 'w') as file:
            for sentence, sentence_predictions in zip(sentences, sentences_predictions):
                tuples = ['{0}/{1}'.format(word, prediction) for word, prediction in
                          zip(sentence, sentence_predictions)]
                file.write(' '.join(tuples) + '\n')
