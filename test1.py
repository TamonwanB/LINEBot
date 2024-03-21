import mysql.connector
import pandas as pd
from pythainlp import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

user_answer = input("Input your question: ")

# Connect to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="031244",
    database="linebot"
)

cursor = connection.cursor()
cursor.execute("SELECT * FROM questionanswer")
data = cursor.fetchall()

df = pd.DataFrame(data, columns=['question', 'answer', 'question_en', 'answer_en'])

tokens_user_answer = word_tokenize(user_answer)
user_answer_str = " ".join(tokens_user_answer)

tokens_an = [word_tokenize(question) for question in df['question_en']]
docs_an = [" ".join(tokens) for tokens in tokens_an]
tokens_docs = [word_tokenize(question) for question in df['question']]
docs_str = [" ".join(tokens) for tokens in tokens_docs]

# all_docs = user_answer_str
all_docs = [user_answer_str] + docs_str
all_an = [user_answer_str] + docs_an

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(all_docs)

vector_an = TfidfVectorizer()
tfidf_an = vector_an.fit_transform(all_an)

cosine_similarities = cosine_similarity(tfidf_matrix[1:],tfidf_an[1:])[0]
# cosine_similarities = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:])[0]

most_similar_index = cosine_similarities.argmax()

most_similar_answer = df['answer'][most_similar_index]
most_similar_answer = df['answer_en'][most_similar_index]

print("Most similar answer:", most_similar_answer)
