import string
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

df = pd.read_csv('train.txt', sep=';', header=None, names=['text', 'emotion'])

emotion_numbers = {}
for i, emo in enumerate(df['emotion'].unique()):
    emotion_numbers[emo] = i
df['emotion'] = df['emotion'].map(emotion_numbers)

def preprocess(txt):
    txt = txt.lower()
    txt = txt.translate(str.maketrans('', '', string.punctuation))
    txt = ''.join(c for c in txt if not c.isdigit())
    txt = ''.join(c for c in txt if c.isascii())
    return txt

df['text'] = df['text'].apply(preprocess)

augmentations = [
    ("i was excited to buy it but it was a huge disappointment", "anger"),
    ("the quality was poor and it did not work properly", "anger"),
    ("this product was a waste of money", "anger"),
    ("the setup was confusing and frustrating", "anger"),
    ("customer support was unhelpful and slow", "anger"),
    ("it caused nothing but frustration", "anger"),
    ("i regret buying this product", "sadness"),
    ("the instructions were unclear and difficult", "anger"),
    ("it broke after one use very disappointed", "sadness"),
    ("the features did not work as advertised", "anger"),
    ("i love this product it works great", "joy"),
    ("amazing quality and very happy with my purchase", "joy"),
    ("exceeded my expectations wonderful product", "joy"),
    ("perfect and works exactly as described", "joy"),
]
for text, emotion in augmentations:
    proc = preprocess(text)
    df.loc[len(df)] = [proc, emotion_numbers[emotion]]

print(f"Added {len(augmentations)} augmented examples")
print(f"Total training samples: {len(df)}")

X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['emotion'], test_size=0.20, random_state=42
)

vectorizer = TfidfVectorizer(
    ngram_range=(1, 3),
    max_df=0.85,
    min_df=2,
    max_features=15000,
    sublinear_tf=True,
)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(
    max_iter=1000,
    class_weight='balanced',
    C=2.0,
    solver='lbfgs',
    random_state=42,
)
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)
acc = accuracy_score(y_test, y_pred)
print(f'Accuracy: {acc:.4f}')
print()
print(classification_report(y_test, y_pred, target_names=list(emotion_numbers.keys())))

EMOTION_MAP = {v: k for k, v in emotion_numbers.items()}

joblib.dump(model, 'backend/model.pkl')
joblib.dump(vectorizer, 'backend/vectorizer.pkl')
joblib.dump(EMOTION_MAP, 'backend/emotion_map.pkl')
print('\nModel saved to backend/ successfully!')
