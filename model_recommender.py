import pandas as pd
import numpy as np
import re, string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from scipy.sparse import hstack

class SkincareRecommender:
    def __init__(self, data_path, rev_path):
        # Download NLTK packages
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger_eng')

        # Load data
        self.df = pd.read_excel(data_path)
        rev_data = pd.read_excel(rev_path)
        self.rev_dict = dict(zip(rev_data['Kata'].astype(str), rev_data['Revisi'].astype(str)))

        # Initialize tools
        self.stop_words = set(stopwords.words('english') + stopwords.words('indonesian'))
        self.stemmer = StemmerFactory().create_stemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.wordnet_map = {"N": wordnet.NOUN, "V": wordnet.VERB, "J": wordnet.ADJ, "R": wordnet.ADV}

    def preprocess_benefit(self, text):
        if pd.isnull(text): return ""
        try:
            text = re.sub(r'\d+', '', text)
            text = text.strip(' "\'')
            text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
            text = re.sub(r"\s+", " ", text).lower()
            text = text.encode("ascii", "ignore").decode()
            tokens = word_tokenize(text)
            tokens = [t for t in tokens if t not in self.stop_words and len(t) > 1]
            tokens = [self.stemmer.stem(t) for t in tokens]
            tagged = pos_tag(tokens)
            tokens = [self.lemmatizer.lemmatize(w, self.wordnet_map.get(p[0], wordnet.NOUN)) for w, p in tagged]
            return " ".join([self.rev_dict.get(t, t) for t in tokens])
        except:
            return ""

    def preprocess_ingredients(self, text):
        if pd.isnull(text): return ""
        text = text.lower()
        text = re.sub(r'[\x00-\x1F\x7F]', '', text)
        text = re.sub(r'[^\x00-\x7F]', '', text)
        text = text.strip(' "\'')
        text = re.sub(r'\d+', '', text)
        text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
        text = re.sub(r'\s+', ' ', text)
        return text

    def recommend(self, input_benefit, input_ingredients, input_subcat, jumlah):
        # Preprocess input
        Benefit_Clean = self.preprocess_benefit(input_benefit)
        cleaned_ingredient = self.preprocess_ingredients(input_ingredients)
        sub_category = input_subcat.lower()

        # Add user input to DataFrame
        temp_df = self.df.copy()
        temp_df = pd.concat([temp_df, pd.DataFrame([{
            'produk': 'Inputan User',
            'Benefit_Clean': Benefit_Clean,
            'cleaned_ingredient': cleaned_ingredient,
            'sub-category': sub_category
        }])], ignore_index=True)

        # Fill NaN values with empty string
        temp_df[['Benefit_Clean', 'cleaned_ingredient', 'sub-category']] = temp_df[['Benefit_Clean', 'cleaned_ingredient', 'sub-category']].fillna("")

        # TF-IDF Vectorization
        tfidf_benefit = TfidfVectorizer(ngram_range=(1, 2))
        tfidf_ing = TfidfVectorizer(ngram_range=(1, 3))
        tfidf_subcat = TfidfVectorizer(ngram_range=(1, 3))

        mat_benefit = tfidf_benefit.fit_transform(temp_df['Benefit_Clean'])
        mat_ing = tfidf_ing.fit_transform(temp_df['cleaned_ingredient'])
        mat_subcat = tfidf_subcat.fit_transform(temp_df['sub-category'])

        # Combine matrices
        combined = hstack([mat_benefit * 0.25, mat_ing * 0.25, mat_subcat * 0.5])

        # Euclidean distance calculation
        dist = euclidean_distances(combined, combined)
        input_index = len(temp_df) - 1
        distance_scores = list(enumerate(dist[input_index]))
        distance_scores = sorted(distance_scores, key=lambda x: x[1])

        # Get top 'jumlah' similar products
        top_indices = [i for i, _ in distance_scores[1:int(jumlah) + 1]]
        rekom = temp_df.iloc[top_indices][['name', 'brand', 'rating', 'price', 'sub-category','cleaned_ingredient','Benefit_Clean']].copy()
        rekom['euclidean_distance'] = [distance_scores[i][1] for i in range(1, int(jumlah) + 1)]
        return rekom.reset_index(drop=True)
