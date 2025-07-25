# 🛍️ Best Buy Review Scraper & Rating Predictor

This project uses **Selenium**, **TF-IDF**, and a **Decision Tree Classifier** to scrape reviews from Best Buy and estimate product ratings using Natural Language Processing (NLP). Originally developed as part of my *CSC 360 - Computer Networking* course, this project has since evolved to include techniques from *CSC 427 - Natural Language Processing*.

---

## 🔍 Purpose

Scraped reviews can be misleading due to biased or dishonest entries. This tool provides:

- Scraping of **real user reviews** from Best Buy.
- A **machine learning model** that predicts product ratings based on review content.
- An **estimated average rating** based purely on the text — helpful for determining product quality from genuine user feedback.

---

## 🧠 How It Works

1. **Web Scraping**  
   - Uses Selenium to collect all reviews for a given Best Buy product.

2. **Preprocessing + ML**  
   - Trains a `TfidfVectorizer` on a labeled Amazon laptop review dataset.
   - Builds a `DecisionTreeClassifier` to learn text-rating relationships.

3. **Prediction**  
   - Applies the trained model to newly scraped Best Buy reviews.
   - Outputs a CSV with predicted ratings and review descriptions.
   - Returns the **average predicted rating**.

---

## 🚀 How to Run

> Make sure you have [GeckoDriver](https://github.com/mozilla/geckodriver/releases) installed and Firefox available in PATH.

```bash
# Install dependencies
pip install selenium scikit-learn numpy pandas datasets
```

# Run the script
```bash
python script.py
```

# 🔗 Tech Stack
* Python 3
* Selenium – Web scraping
* scikit-learn – ML model & text vectorization
* HuggingFace Datasets – Labeled data from amazon-laptop-reviews-enriched
* NumPy + Pandas – Data manipulation
* Pickle – Efficient storage of intermediate results

# 📂 Outputs
reviews.pkl: Raw scraped reviews (cached)

tfid_vectorizer.pkl: Trained TF-IDF vectorizer

decision_tree_classifier.pkl: Trained Decision Tree model

reviewRatings.csv: Final CSV with review text and predicted ratings
