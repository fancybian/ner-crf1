# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import os

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
BROWN_CLUSTERS_FILEPATH = "/media/aj/ssd2a/nlp/corpus/brown/wikipedia-de/brown_c1000_min12/paths"
UNIGRAMS_NAMES_FILEPATH = "" #todo
UNIGRAMS_FILEPATH = "" #todo
LDA_FILEPATH = os.path.join(CURRENT_DIR, "lda-model")
LDA_DICTIONARY_FILEPATH = os.path.join(CURRENT_DIR, "lda-dictionary")
LDA_CACHE_MAX_SIZE = 100000
STANFORD_DIR = "/media/ssd2/nlp/nlpjava/stanford-postagger-full-2013-06-20/stanford-postagger-full-2013-06-20/"
STANFORD_POS_JAR_FILEPATH = os.path.join(STANFORD_DIR, "stanford-postagger-3.2.0.jar")
STANFORD_MODEL_FILEPATH = os.path.join(STANFORD_DIR, "models/german-fast.tagger")
POS_TAGGER_CACHE_FILEPATH = os.path.join(CURRENT_DIR, "pos.cache")
UNIGRAMS_SKIP_FIRST_N = 0
UNIGRAMS_MAX_COUNT_WORDS = 1000
W2V_CLUSTERS_FILEPATH = "/media/aj/ssd2a/nlp/corpus/word2vec/wikipedia-de/classes1000_cbow0_size300_neg0_win10_sample1em3_min50.txt"
LDA_WINDOW_LEFT_SIZE = 5
LDA_WINDOW_RIGHT_SIZE = 5

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("identifier",
                        help="A short name/identifier for your experiment, e.g. 'ex42b'.")
    
    trainer = pycrfsuite.Trainer(verbose=True)
    
    print("Loading examples...")
    features = create_features()
    examples = articles_to_xy(load_articles(ARTICLES_FILEPATH), 50, features, only_labeled_chunks=True)
    
    print("Appending up to %d examples...".format(COUNT_EXAMPLES))
    added = 0
    for (features, labels, tokens) in examples:
        if added > 0 and added % 500 == 0:
            print("Appended %d examples...".format(added))
        trainer.append(features, labels)
        added += 1
        if added == COUNT_EXAMPLES:
            break
    
    print("Training...")
    if MAX_ITERATIONS is not None and MAX_ITERATIONS > 0:
        trainer.set_params({'max_iterations': MAX_ITERATIONS})
    trainer.train(identifier)

def create_features():
    bc = BrownClusters(BROWN_CLUSTERS_FILEPATH)
    gaz = Gazetteer(UNIGRAMS_NAMES_FILEPATH, UNIGRAMS_FILEPATH)
    lda = LdaWrapper(LDA_FILEPATH, LDA_DICTIONARY_FILEPATH, cache_max_size=LDA_CACHE_MAX_SIZE)
    pos = PosTagger(STANFORD_POS_JAR_FILEPATH, STANFORD_MODEL_FILEPATH, cache_dir=POS_TAGGER_CACHE_FILEPATH)
    ug = Unigrams(UNIGRAMS_FILEPATH, skip_first_n=UNIGRAMS_SKIP_FIRST_N, max_count_words=UNIGRAMS_MAX_COUNT_WORDS)
    w2vc = W2VClusters(W2V_CLUSTERS_FILEPATH)
    
    result = [
        StartsWithUppercaseFeature(),
        TokenLengthFeature(),
        ContainsDigitsFeature(),
        ContainsPunctuationFeature(),
        OnlyDigitsFeature(),
        OnlyPunctuationFeature(),
        W2VClusterFeature(w2vc),
        BrownClusterFeature(bc),
        BrownClusterBitsFeature(bc),
        GazetteerFeature(gaz),
        WordPatternFeature(),
        UnigramRankFeature(ug),
        PrefixFeature(),
        SuffixFeature(),
        POSTagFeature(pos),
        LDATopicFeature(lda, LDA_WINDOW_LEFT_SIZE, LDA_WINDOW_LEFT_SIZE)
    ]
    
    return result

if __name__ == "__main__":
    main()
