import logging

import networkx as nx
import numpy as np
import torch
from django.core.cache import cache
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertJapaneseTokenizer, BertModel

from config.settings import (
    MAX_LENGTH, NUMBER_OF_SENTENCES, PRETRAINED_MODEL, PRETRAINED_TOKENIZER
)

logger = logging.getLogger(__name__)

CACHE_KEY_MODEL = 'model'
CACHE_KEY_TOKENIZER = 'tokenizer'
SEPARATOR = '。'


def create_model():
    model = cache.get(CACHE_KEY_MODEL)
    if model is None:
        logger.info('Model is not cached.')
        model = BertModel.from_pretrained(PRETRAINED_MODEL)
        cache.set(CACHE_KEY_MODEL, model, None)
    else:
        logger.info('Use cached model.')
    return model


def create_tokenizer():
    tokenizer = cache.get(CACHE_KEY_TOKENIZER)
    if tokenizer is None:
        logger.info('Tokenizer is not cached.')
        tokenizer = BertJapaneseTokenizer.from_pretrained(PRETRAINED_TOKENIZER)
        cache.set(CACHE_KEY_TOKENIZER, tokenizer, None)
    else:
        logger.info('Use cached tokenizer.')
    return tokenizer


def summarize(text):
    logger.info(f'Original text: {text}')

    sequences = text.split(SEPARATOR)

    tokenizer = create_tokenizer()
    inputs = tokenizer(sequences,
                       add_special_tokens=True,
                       max_length=MAX_LENGTH,
                       padding='max_length',
                       truncation=True,
                       return_tensors='pt')
    input_ids = inputs['input_ids']
    token_type_ids = inputs['token_type_ids']
    attention_mask = inputs['attention_mask']

    model = create_model()
    model.eval()

    with torch.no_grad():
        outputs = model(input_ids=input_ids,
                        attention_mask=attention_mask,
                        token_type_ids=token_type_ids)

    # Make sentence vectors
    sentence_vectors = torch.mean(outputs.last_hidden_state, dim=1).numpy()

    # Calculate cosine similarity between sentence vectors
    similarity_matrix = cosine_similarity(sentence_vectors)

    # Set diagonal components to zero to get adjacency matrix
    np.fill_diagonal(similarity_matrix, 0)

    # Compute ranking of the nodes by PageRank
    graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(graph)

    # Select important sentences
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sequences)),
                              reverse=True)
    summarized = SEPARATOR.join([ranked_sentences[i][1]
                                 for i in range(NUMBER_OF_SENTENCES)])
    summarized += SEPARATOR

    logger.info(f'Summarized text: {summarized}')
    return summarized
