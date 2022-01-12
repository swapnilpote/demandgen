from app.mod.module.entity_extractor.bert_base_ner_uncased import BertBaseNERUncased
from app.mod.module.classifier.domain_classifier import GloveDomainClassifier

class Predict:
    def __init__(self):
        self.bert_base_ner_uncased = BertBaseNERUncased()
        self.glove_domain_classifier = GloveDomainClassifier()

    def result(self, text):
        result = dict()
        domain_result = self.glove_domain_classifier.predict(text)
        result = domain_result

        if domain_result.get("domain") == "dvm":
            ner_result = self.bert_base_ner_uncased.predict(text)
            result["entities"] = ner_result
        elif domain_result.get("domain") == "ivr":
            print("Work in progress")

        return result