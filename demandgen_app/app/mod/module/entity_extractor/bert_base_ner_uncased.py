from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline


class BertBaseNERUncased:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER-uncased")
        self.model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER-uncased")
        self.pipeline = pipeline('ner', model=self.model, tokenizer=self.tokenizer)

    def predict(self, text):
        result = self.pipeline(text)

        person_index = list()
        for res in result:
            if res.get("entity")=="B-PER" and len(person_index)==0:
                person_index.append(res.get("start"))
            elif res.get("entity")=="I-PER":
                person_index.append(res.get("end"))

        return text[person_index[0]: person_index[-1]]

if __name__ == "__main__":
    bert = BertBaseNERUncased()
    print(bert.predict("i am swapnil pote living in kalyan"))
