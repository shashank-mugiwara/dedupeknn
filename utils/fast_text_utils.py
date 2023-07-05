import logging
from logging.config import dictConfig

from loaders import FastTextModelLoader
from logger import DedupeKnnLogger

logger = logging.getLogger('oden')
dictConfig(DedupeKnnLogger().dict())


# get the loaded model
model = FastTextModelLoader.get_fast_text_model()


def generate_sentence_vector(sentence):
    if sentence is None or sentence == "":
        logger.error("Blank sentence received for vector generation")
        raise Exception

    sentence_vector = model.get_sentence_vector(sentence)
    if sentence_vector is None:
        logger.error("Failed to generate vector representation for the given sentence")
        raise Exception

    return sentence_vector
