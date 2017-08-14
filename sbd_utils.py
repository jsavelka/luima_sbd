from __future__ import division
import config
import pycrfsuite
import re
import os


def text2sentences(text):
    tokenizer = re.compile(config.TOKENIZATION_STRING)
    tokens = [token.group() for token in tokenizer.finditer(text)]
    preds = tokens2preds(tokens)
    return preds2sentences(tokens, preds)


def preds2sentences(tokens, preds):
    sentences = []
    sentence = ''
    for i, pred in enumerate(preds):
        if pred != 'O':
            sentence += tokens[i]
        else:
            sentences.append(sentence)
            sentence = ''
    sentences.append(sentence)
    return sentences


def tokens2preds(tokens):
    features = [word2features(tokens, i, config.CRF_WINDOW) for i, token
                in enumerate(tokens)]
    # sen tagging
    sen_tagger = init_crf_model(config.SEN_MODEL)
    sen_tags = sen_tagger.tag(features)

    # nsen tagging
    nsen_tagger = init_crf_model(config.NSEN_MODEL)
    nsen_tags = nsen_tagger.tag(features)

    # integrating tagging
    features_x = [word2features(tokens, i, config.CRF_WINDOW,
                                [sen_tags, nsen_tags])
                  for i, token
                  in enumerate(tokens)]
    int_tagger = init_crf_model(config.INTEGRATING_MODEL)

    return int_tagger.tag(features_x)


def word2features(doc, i, n, extras=None):
    if not extras:
        extras = []
    features = ["bias"]
    if i/len(doc) < 0.2:
        features.append("atfront")
    if i/len(doc) > 0.8:
        features.append("atback")
    for n_idx in range(0, n+1):
        if i+n_idx < len(doc):
            features.extend(token2features(token=doc[i+n_idx], i=n_idx))
            for extra in extras:
                features.append(str(n_idx) + ':' + extra[i+n_idx])
        elif i+n_idx == len(doc):
            features.append(str(n_idx) + ':EOS')
    for n_idx in range(-n, 0):
        if i+n_idx >= 0:
            features.extend(token2features(token=doc[i + n_idx], i=n_idx))
            for extra in extras:
                features.append(str(n_idx) + ':' + extra[i+n_idx])
        elif i+n_idx == -1:
            features.append(str(n_idx) + ':BOS')
    return features


def token2features(token, i):
    return [
        str(i) + ":word.lower=" + token.lower(),
        str(i) + ":word.sig=" + create_token_sig(token),
        str(i) + ":word.length=" + get_token_length(token),
        str(i) + ":word.islower=" + str(token.islower()),
        str(i) + ":word.isupper=" + str(token.isupper()),
        str(i) + ":word.istitle=" + str(token.istitle()),
        str(i) + ":word.isdigit=" + str(token.isdigit()),
        str(i) + ":word.iswhitespace=" + str(token.isspace())
    ]


def create_token_sig(token):
    digit = re.compile(r'\d')
    lower_char = re.compile(r'[a-z]')
    upper_char = re.compile(r'[A-Z]')
    ws = re.compile(r'^[ \t\f\v]]+$')
    linebreaking_ws = re.compile(r'^[\n\r]+$')
    token = lower_char.sub('c', token)
    token = upper_char.sub('C', token)
    token = digit.sub('D', token)
    if ws.match(token):
        token = 'hws'
    if linebreaking_ws.match(token):
        token = 'vws'
    return token


def get_token_length(token):
    length = len(token)
    if length < 4:
        return str(length)
    elif length < 7:
        return 'normal'
    else:
        return 'long'


def init_crf_model(model_type):
    tagger = pycrfsuite.Tagger()
    model_path = os.path.join(config.DATA_DIR, model_type)
    tagger.open(model_path)
    return tagger
