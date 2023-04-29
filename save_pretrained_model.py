import os
from transformers import BertJapaneseTokenizer, BertModel

PRETRAINED_MODEL_NAME = 'cl-tohoku/bert-base-japanese-whole-word-masking'
OUTPUT_DIR = './pretrained'


def save_pretrained_model():
    # get pretrained model and tokenizer
    model = BertModel.from_pretrained(PRETRAINED_MODEL_NAME)
    tokenizer = BertJapaneseTokenizer.from_pretrained(PRETRAINED_MODEL_NAME)

    # save pretrained model and tokenizer
    model.save_pretrained(os.path.join(OUTPUT_DIR, 'model'))
    tokenizer.save_pretrained(os.path.join(OUTPUT_DIR, 'tokenizer'))

    return


if __name__ == '__main__':
    save_pretrained_model()
