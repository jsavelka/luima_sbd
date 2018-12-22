from __future__ import division
import luima_sbd.config as config
import pycrfsuite
import re
import os


LOWER_CHAR = re.compile('[a-z]')
UPPER_CHAR = re.compile('[A-Z]')
SINGLE_DIGIT = re.compile('\\d')
WS = re.compile('^[ \\t]]+$')
LB_WS = re.compile('^[\\n\\r\\v\\f]+$')


def text2sentences(text, offsets=False):
    tokenizer = re.compile(config.TOKENIZATION_STRING)
    matches = [match for match in tokenizer.finditer(text)]
    preds = tokens2preds([match.group() for match in matches])
    indices = preds2sentences(matches, preds)
    if offsets:
        return indices
    else:
        return [text[indice[0]:indice[1]] for indice in indices]


def preds2sentences(matches, preds):
    indices = []
    in_annotation = False
    start, end = (0, 0)
    for label, match in zip(preds, matches):
        if label != 'O':
            if in_annotation:
                end = match.end()
            else:
                in_annotation = True
                start = match.start()
                end = match.end()
        else:
            if in_annotation:
                in_annotation = False
                indices.append((start, end))
    if in_annotation:
        indices.append((start, end))
    return indices


def tokens2preds(tokens):
    features = [word2features(tokens, i, config.CRF_WINDOW) for i, token
                in enumerate(tokens)]
    tagger = init_crf_model(config.SIMPLE_MODEL)
    return tagger.tag(features)


def word2features(doc, i, n, extras=None):
    if not extras:
        extras = []
    features = ["bias"]
    for n_idx in range(0, n+1):
        if i+n_idx < len(doc):
            features.extend(token2features(token=doc[i+n_idx], i=n_idx))
        elif i+n_idx == len(doc):
            features.append(str(n_idx) + ':EOS')
    for n_idx in range(-n, 0):
        if i+n_idx >= 0:
            features.extend(token2features(token=doc[i + n_idx], i=n_idx))
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
    token = LOWER_CHAR.sub('c', token)
    token = UPPER_CHAR.sub('C', token)
    token = SINGLE_DIGIT.sub('D', token)
    ws_match = WS.match(token)
    ln_ws_match = LB_WS.match(token)
    if ws_match:
        if ws_match.end()-ws_match.start() < 2:
            token = 'singlehws'
        elif ws_match.end()-ws_match.start() < 5:
            token = 'shorthws'
        elif ws_match.end()-ws_match.start() < 10:
            token = 'hws'
        else:
            token = 'longhws'
    if ln_ws_match:
        if ln_ws_match.end() - ln_ws_match.start() < 2:
            token = 'singlevws'
        elif ln_ws_match.end() - ln_ws_match.start() < 3:
            token = 'doublevws'
        elif ln_ws_match.end() - ln_ws_match.start() < 4:
            token = 'triplevws'
        else:
            token = 'longvws'
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
    model_path = os.path.join(config.MODULE_DIR, config.DATA_DIR, model_type)
    tagger.open(model_path)
    return tagger
