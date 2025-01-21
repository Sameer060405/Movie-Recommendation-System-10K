# 🎬 Movie Recommender System

A content-based movie recommendation system built with Streamlit that suggests similar movies based on user input and provides an interactive chat interface for personalized recommendations.

## 🌟 Features

- Search-based movie recommendations
- Interactive movie chatbot assistant
- Movie poster visualization using TMDB API
- Beautiful UI with custom background
- Error handling and retry mechanisms
- Responsive layout with dual-column design

## 🛠️ Tech Stack

- Python 3.8+
- Streamlit for web interface
- scikit-learn for content-based filtering
- Pandas for data manipulation
- TMDB API for movie posters
- Pickle for model serialization

## 📁 Project Structure

```
movie-recommender/
├── app.py                  # Main Streamlit application
├── movie_recommendation.ipynb  # Data preprocessing and model training
├── models/
│   ├── movie_dict.pkl     # Serialized movie dictionary
│   ├── movies.pkl         # Processed movie dataset
│   └── similarity.pkl     # Similarity matrix
├── hero1.jpg              # Background image
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/movie-recommender.git
cd movie-recommender
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```

## 📊 Data Preprocessing

The project includes a Jupyter notebook (`movie_recommendation.ipynb`) that demonstrates:
- Data cleaning and preprocessing
- Feature extraction
- TF-IDF vectorization
- Similarity matrix computation
- Model serialization

## 🔑 API Configuration

The system uses TMDB API for fetching movie posters. To run the application:
1. Get an API key from [TMDB](https://www.themoviedb.org/documentation/api)
2. Replace the API key in `app.py`

## 💡 Usage

1. **Search-Based Recommendations:**
   - Select a movie from the dropdown
   - Click "Get Recommendations"
   - View similar movies with posters

2. **Chat Interface:**
   - Type your movie preferences
   - Get personalized recommendations
   - Interact with the movie assistant

## 📝 Dataset

The movie dataset was sourced from Kaggle and includes:
- Movie titles
- Genres
- Cast and crew information
- Plot descriptions
- Release dates
- User ratings

## 🤝 Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- TMDB API for movie data and posters
- Kaggle for the dataset
- Streamlit for the awesome framework
