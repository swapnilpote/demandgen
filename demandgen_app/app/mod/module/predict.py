from app.mod.module.entity_extractor.bert_base_ner_uncased import BertBaseNERUncased
from app.mod.module.classifier.domain_classifier import GloveDomainClassifier

class Predict:
    def __init__(self):
        self.bert_base_ner_uncased = BertBaseNERUncased()
        self.glove_domain_classifier = GloveDomainClassifier()

    def result(self, text):
        self.glove_domain_classifier.predict(text)
        self.bert_base_ner_uncased.predict(text)

        return True