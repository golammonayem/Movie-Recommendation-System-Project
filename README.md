<<<<<<< HEAD
# Movie-Recommendation-System-Project
=======
# 🎬 Movie Recommendation System

An end-to-end Machine Learning web application that suggests similar movies based on user preferences using content-based filtering and Natural Language Processing (NLP).

## 🚀 Live Demo
[Click Here to View Live App](#) *(Deploy করার পর এখানে তোমার Streamlit-এর লাইভ লিংকটি বসিয়ে দিও)*

---

## 🛠️ Tech Stack & Libraries
* **Language:** Python
* **Machine Learning & NLP:** Scikit-learn, Pandas, NumPy, NLTK/AST
* **Web Framework:** Streamlit
* **Deployment & Version Control:** Git, GitHub, Streamlit Community Cloud

---

## 📊 Methodology & Workflow
1. **Data Preprocessing:** Cleaned and parsed the TMDB 5000 Movies dataset (handling missing values, extracting JSON-like metadata for genres, keywords, cast, and crew).
2. **Feature Engineering:** Combined overview, genres, keywords, cast, and director into a single composite `tags` feature for each movie.
3. **Vectorization:** Converted text data into numerical feature vectors using `CountVectorizer` (limiting to top 5,000 features).
4. **Similarity Computation:** Calculated the cosine distance matrix (`Cosine Similarity`) across all 4,806 movies to determine semantic closeness.
5. **Web Application:** Built an interactive frontend using **Streamlit** where users can select a movie and instantly receive the top 5 recommendations.

---

## 📂 Project Structure
```text
📦 Movie-Recommendation-System-Project
│
├── app.py                # Streamlit web application script
├── code.ipynb            # Jupyter Notebook containing ML pipeline & model building
├── movie_dict.pkl        # Serialized Pandas DataFrame containing movie metadata
├── similarity.pkl        # Precomputed Cosine Similarity matrix
└── requirements.txt      # Required Python packages for deployment
>>>>>>> afc0f6a (Adding md)
