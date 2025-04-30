import joblib
from model_recommender import SkincareRecommender

# Membuat instansi dari SkincareRecommender
recommender = SkincareRecommender(data_path="D:/Documents/Tugas Akhir/Recommender System/data_cleaned.xlsx",
                                  rev_path="D:/Documents/Tugas Akhir/Recommender System/revword.xlsx")

# Menyimpan model yang sudah dilatih
joblib.dump(recommender, 'rekomendasi_model.pkl')
