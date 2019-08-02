#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Imports

from nose.tools import assert_equal

from lexnlp.nlp.en.segments.sentences import get_sentence_list, build_sentence_model, \
    pre_process_document, post_process_sentence
from lexnlp.tests import lexnlp_tests

__author__ = "ContraxSuite, LLC; LexPredict, LLC"
__copyright__ = "Copyright 2015-2019, ContraxSuite, LLC"
__license__ = "https://github.com/LexPredict/lexpredict-lexnlp/blob/master/LICENSE"
__version__ = "0.2.7"
__maintainer__ = "LexPredict, LLC"
__email__ = "support@contraxsuite.com"


def test_sentence_segmenter_empty():
    """
    Test basic sentence segmentation.
    """
    _ = get_sentence_list("")


def test_sentence_segmenter():
    lexnlp_tests.test_extraction_func_on_test_data(get_sentence_list)


def test_titles_in_post_process_sentence1():
    sentence = '''This is a title

And this is the next sentence.
'''

    text = '''Something. ''' + sentence + ''' That's it.'''
    start = text.index(sentence)
    span = (start, start + len(sentence))

    actual = [text[start:end].strip() for start, end in post_process_sentence(text, span)]
    expected = ['This is a title', 'And this is the next sentence.']
    assert_equal(expected, actual)


def test_ocr_artifacts_in_post_process_sentence1():
    sentence = '''~~``~~~~```~~
    
    >>
    
    <<
    
    ""'''
    text = '''Something. ''' + sentence + '''That's it.'''
    start = text.index(sentence)
    span = (start, start + len(sentence))

    actual = [text[start:end] for start, end in post_process_sentence(text, span)]
    expected = []
    assert_equal(expected, actual)


def test_ocr_artifacts_in_post_process_sentence2():
    sentence = '''\\
    
    ______f
    hello hello
      
    '''
    text = '''Something. ''' + sentence + '''That's it.'''
    start = text.index(sentence)
    span = (start, start + len(sentence))

    actual = [text[start:end] for start, end in post_process_sentence(text, span)]
    expected = ['______f\n    hello hello']
    assert_equal(expected, actual)


def test_ocr_artifacts_in_post_process_sentence3():
    sentence = '''\\
    
    ba
     
    Ba bal
    
    Q
    
    F

    '''
    text = '''Something. ''' + sentence + '''That's it.'''
    start = text.index(sentence)
    span = (start, start + len(sentence))

    actual = [text[start:end] for start, end in post_process_sentence(text, span)]
    expected = []
    assert_equal(expected, actual)


def test_build_sentence_model():
    """
    Test the custom Punkt model.
    :return:
    """
    # Setup training text and model
    training_text = "The I.R.C. is a large body of text produced by the U.S. Congress in D.C. every year."
    sentence_segmenter = lexnlp_tests.benchmark_extraction_func(build_sentence_model, training_text)
    num_sentences_custom = len(
        sentence_segmenter.tokenize("Have you ever cited the U.S. I.R.C. to your friends?"))
    assert_equal(num_sentences_custom, 1)


def test_pre_process_document():
    lexnlp_tests.test_extraction_func_on_test_data(pre_process_document, actual_data_converter=lambda text: [text])
