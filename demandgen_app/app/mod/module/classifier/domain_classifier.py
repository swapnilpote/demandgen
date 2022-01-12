import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import json
import numpy as np 

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Embedding
from tensorflow.keras.preprocessing.sequence import pad_sequences

# physical_devices = tf.config.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)


class GloveDomainClassifier:
    def __init__(self):
        self.input_length = 126

        with open(os.path.join(os.getcwd(), "files", "word2idx.json"), "r", encoding="utf8") as f:
            self.word2idx = json.load(f)
        with open(os.path.join(os.getcwd(), "files", "idx2word.json"), "r", encoding="utf8") as f:
            self.idx2word = json.load(f)
        with open(os.path.join(os.getcwd(), "files", "embeddings.npy"), "rb") as f:
            self.embeddings = np.load(f)
        self.model_weight_file = os.path.join(os.getcwd(), "files", "domain_model.h5")

        self.model = self.glove_model()


    def preprocessing(self, text):
        text = text.split()
        text_vec = [self.word2idx.get(word, self.word2idx.get("unknown")) for word in text]
        text_vec = pad_sequences([text_vec], maxlen=self.input_length, dtype="int32", padding="post", truncating="post", value=self.word2idx.get("pad"))

        return text_vec

    def glove_model(self):
        model = Sequential()
        model.add(Embedding(self.embeddings.shape[0], self.embeddings.shape[1], weights=[self.embeddings], input_length=self.input_length, trainable=False))
        model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(126)))
        model.add(Dense(63, activation="relu"))
        model.add(Dense(2, activation="softmax"))
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
        model.load_weights(self.model_weight_file)

        return model

    def predict(self, text):
        class_dict = {"0": "dvm", "1": "ivr"}

        text_vec = self.preprocessing(text)
        result = self.model.predict(text_vec)

        return {"domain": class_dict.get(str(np.argmax(result[0])))}