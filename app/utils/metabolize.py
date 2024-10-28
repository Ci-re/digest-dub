# import re
import string
from pandas import DataFrame
from typing import Optional
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


class Texts:
    def __init__(self, data: Optional[DataFrame] = None) -> None:
        self.data: DataFrame = data if data is not None else DataFrame()
        self._prepare_data() if data is not None else DataFrame()

    def _prepare_data(self) -> None:
        columns = ["name","description","course","ingredient"]
        self.data: DataFrame = DataFrame(self.data[columns]) if not self.data.empty else DataFrame()

    @staticmethod
    def is_ascii(s: str) -> bool:
        return all(ord(c) < 128 for c in s)

    def filter_ascii(self) -> 'Texts':
        '''
            This code filters out non-english entries
        '''
        if not self.data.empty:
            self.data = DataFrame(self.data[self.data['name'].apply(self.is_ascii)])
            self.data = DataFrame(self.data[self.data['ingredient'].apply(self.is_ascii)])
        return self

    @staticmethod
    def clean_text(text: str) -> str:
        clean_text =[]
        for t in text.split(' '):
            # cleaned_text = re.sub(r"\d+", '', t)
            cleaned_text = t.lower()
            cleaned_text = cleaned_text.translate(str.maketrans('','',string.digits))
            cleaned_text = cleaned_text.translate(str.maketrans('','',"{}()[]"))
            cleaned_text = cleaned_text.replace(' ', '')
            cleaned_text = cleaned_text.translate(str.maketrans('','', string.punctuation))
            clean_text.append(cleaned_text)
        return ' '.join(clean_text)

    def wordsbag(self, index_col: str) -> DataFrame:
        print("loading wordbag")
        if not self.data.empty:
            self.data = self.data.dropna()
            colnames = self.data.columns
            print(colnames)
            for col in colnames:
                self.data[col] = self.data[col].apply(self.clean_text)
            self.data['bag_of_words'] = self.data[self.data.columns[1:]].apply(lambda x:' '.join(x), axis=1)
            if index_col in self.data.columns:
                self.data.set_index(index_col, inplace=True)
        return self.data

    def generate_vector_embeddings(self, dataframe: DataFrame) -> DataFrame:
        tfidf = TfidfVectorizer(stop_words='english', min_df=5)
        tfidfmat = tfidf.fit_transform(dataframe["bag_of_words"])
        cossim = cosine_similarity(tfidfmat)
        return cossim
