import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

class SpamDetector:
    def __init__(self):
        # Vektörizer ve Model nesnelerini oluştur
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.model = MultinomialNB()
        # Kayıt yolları
        self.model_path = "backend/src/storage/spam_model.pkl"
        self.vectorizer_path = "backend/src/storage/vectorizer.pkl"

    def prepare_data(self, df):
        """Veriyi sayısal vektörlere çevirir ve böler."""
        X = self.vectorizer.fit_transform(df['body'])
        y = df['is_spam']
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train(self, X_train, y_train):
        """Modeli eğitir ve dosyaya kaydeder."""
        self.model.fit(X_train, y_train)
        # Klasör yoksa oluştur
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        # Modelleri kaydet
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.vectorizer, self.vectorizer_path)
        print("Model ve Vektörizer başarıyla kaydedildi!")

    def load_model(self):
        """Kaydedilmiş modeli geri yükler."""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.vectorizer = joblib.load(self.vectorizer_path)
            return True
        return False

    def predict(self, text):
        """Tahmin yürütür."""
        vectorized_text = self.vectorizer.transform([text])
        return self.model.predict(vectorized_text)[0]