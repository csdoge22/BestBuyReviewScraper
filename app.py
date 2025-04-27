import time
import random
import numpy as np
from selenium import webdriver
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier

import os
from os import path
import pandas as pd
import pickle

from datasets import load_dataset

# we want to ensure that the file is removed to prevent duplicate data across sessions
if(path.exists("reviews.json")):
    os.remove("reviews.json")

def run_script():
    """
    This is the universal method to run:
    """
    if not os.path.exists("./reviews.pkl"):
        # url of the website
        base_website = 'https://www.bestbuy.com/site/reviews/asus-rog-zephyrus-g16-16-oled-240hz-gaming-laptop-intel-core-ultra-9-32gb-lpddr5x-nvidia-geforce-rtx-4090-2tb-ssd-eclipse-gray/6570220?variant=A'

        # service = Service(executable_path=path)
        
        # To gather data, we will use Firefox
        driver = webdriver.Firefox()
        driver.get(base_website)
        pageLine = driver.find_element(by="xpath",value="//span[@class='message']").text
        pageTokens = pageLine.split(" ")
        
        # the second to last index of the page number will show the number of reviews
        numPages = int(pageTokens[len(pageTokens)-2])//20
        
        descriptionList = []

        # in a range for loop, the last index is never included (so 1 is added to the number of pages)
        for i in range(1,numPages+1):
            currentPage = base_website+"&page="+str(i)
            driver.get(currentPage)
            
            descriptions = driver.find_elements(by="xpath",value="//div[@class='review-item-content col-xs-12 col-md-9']//p[@class='pre-white-space']")
            if descriptions != []:
                print("Located Descriptions")
            else:
                driver.quit()
                return

            for description in descriptions:
                descriptionList.append(description.text)
            # to prevent bot detection, loading each web-page 
            for description in descriptions:
                print(description.text)
                time.sleep(random.random()*5)

            time.sleep(random.random())
        
        with open("reviews.pkl", "wb") as file:
            pickle.dump(descriptionList, file)
    else:
        with open("reviews.pkl", "rb") as file:
            descriptionList = pickle.load(file)
    return descriptionList

def train_test_model():
    if not os.path.exists("decision_tree_classifier.pkl") or not os.path.exists("tfid_vectorizer.pkl"):
        dataset = load_dataset("naga-jay/amazon-laptop-reviews-enriched", split="train")
        
        data = np.asarray(dataset["text"])
        labels = np.asarray(dataset["rating"])        
        
        vectorizer = TfidfVectorizer()
        data = vectorizer.fit_transform(data)
        
        classifier = DecisionTreeClassifier()
        classifier.fit(data, labels)
        
        new_reviews = run_script()
        data_new = vectorizer.transform(new_reviews)
        predicted = classifier.predict(data_new)
        
        with open("tfid_vectorizer.pkl", "wb") as file:
            pickle.dump(vectorizer, file)
        with open("decision_tree_classifier.pkl", "wb") as file:
            pickle.dump(classifier, file)
    else:
        with open("tfid_vectorizer.pkl", "rb") as file:
            vectorizer = pickle.load(file)
        with open("decision_tree_classifier.pkl", "rb") as file:
            classifier = pickle.load(file)
        
        new_reviews = run_script()
        data_new = vectorizer.transform(new_reviews)
        predicted = classifier.predict(data_new)
    
    format_preds = {
        "descriptions": new_reviews,
        "predicted_ratings": list(predicted)
    }
    frame = pd.DataFrame(format_preds)
    frame.to_csv("reviewRatings.csv")
    return predicted

def find_rating():
    predictions = np.array(train_test_model())
    return np.average(predictions)

# run the application
print(find_rating())