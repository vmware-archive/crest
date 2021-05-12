from transformers import RobertaTokenizer, RobertaForSequenceClassification
import nltk
from crest.config import *


def load_transformer_model():
    roberta_tokenizer = RobertaTokenizer.from_pretrained('gargam/roberta-base-crest')
    model = RobertaForSequenceClassification.from_pretrained('gargam/roberta-base-crest')
    return roberta_tokenizer, model

def crest_init():
    nltk.download('stopwords')
    nltk.download('punkt')
    roberta_tokenizer, transfomer_model = load_transformer_model()
    global_args['model_params']['tokenizer'] =roberta_tokenizer
    global_args['model_params']['transfomer_model'] =transfomer_model
