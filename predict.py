from transformers import pipeline

pretrained_name = "w11wo/indonesian-roberta-base-sentiment-classifier"

nlp = pipeline("sentiment-analysis", model=pretrained_name, tokenizer=pretrained_name)
