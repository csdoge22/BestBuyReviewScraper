# 🛒 Best Buy Review Scraper & Sentiment Analyzer

This project is a **web scraping + machine learning pipeline** that estimates genuine product ratings using review data from Best Buy. Originally created for my CSC 360: *Computer Networking* course, I have since extended it with Natural Language Processing (NLP) techniques from CSC 427: *Natural Language Processing*.

---

## 📌 Project Overview

Many product reviews online can be **inconsistent, biased, or spammy**. This tool aims to:

- ✅ **Scrape reviews** from a Best Buy product page using Selenium
- ✅ **Preprocess the review text** and analyze sentiment using a trained classifier
- ✅ **Predict an average rating** for the product based on its review content
- ✅ **Export results** to a CSV for transparency and further analysis

---

## ⚙️ How It Works

1. **Web Scraping (Selenium + Firefox)**  
   Automatically navigates to a Best Buy product page and scrapes all user reviews across multiple pages.

2. **Model Training (NLP + scikit-learn)**  
   Trains a `DecisionTreeClassifier` on enriched Amazon laptop reviews from the `datasets` library using `TfidfVectorizer`.

3. **Rating Prediction**  
   Applies the trained model to the scraped Best Buy reviews and predicts their likely ratings (1–5 scale).

4. **Output**  
   - Saves predictions and original review text to `reviewRatings.csv`
   - Prints the **average predicted rating** to the console

---

## 🚀 Getting Started

### 🔧 Prerequisites

Make sure the following Python packages are installed:

```bash
pip install selenium scikit-learn pandas numpy datasets
