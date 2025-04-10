import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("movies.csv")


for feature in ['genres', 'director', 'cast', 'keywords']:
    df[feature] = df[feature].fillna('')


def combine_features(row):
    return f"{row['genres']} {row['director']} {row['cast']} {row['keywords']}"

df["combined_features"] = df.apply(combine_features, axis=1)


vectorizer = CountVectorizer()
feature_matrix = vectorizer.fit_transform(df["combined_features"])


similarity = cosine_similarity(feature_matrix)


def get_title_from_index(index):
    return df.iloc[index]["title"]


def get_index_from_title(title):
    result = df[df.title.str.lower() == title.lower()]
    if not result.empty:
        return result.index.values[0]
    return None


def recommend(movie_title, top_n=5):
    index = get_index_from_title(movie_title)
    if index is None:
        return f"Movie '{movie_title}' not found in dataset."
    
    sim_scores = list(enumerate(similarity[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]  
    
    recommendations = [get_title_from_index(i[0]) for i in sim_scores]
    return recommendations


if __name__ == "__main__":
    user_input = input("Enter a movie title: ")
    recs = recommend(user_input)
    print("\nTop Recommendations:")
    for i, movie in enumerate(recs, 1):
        print(f"{i}. {movie}")
