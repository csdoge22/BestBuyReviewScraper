import time
import random
from selenium import webdriver
import bias_parser
import os
from os import path
import pandas as pd

# we want to ensure that the file is removed to prevent duplicate data across sessions
if(path.exists("reviews.json")):
    os.remove("reviews.json")
def run_script():
    """
    This is the universal method to run:
    """

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

    # The final result will be stored in a Pandas Dataframe
    def scrape_reviews() -> pd.DataFrame:
        """
        This method will scrape all properties of each review. The fields will be: \n
         | Name | Description | Rating Value |
        """
        try:
            nameList = []
            descriptionList = []
            ratingNumbers = []
            average = 0

            # in a range for loop, the last index is never included (so 1 is added to the number of pages)
            for i in range(1,numPages+1):
                currentPage = base_website+"&page="+str(i)
                driver.get(currentPage)
                # we will sum all the anticipated reviews
                names = driver.find_elements(by="xpath",value="//div[@class='ugc-author v-fw-medium body-copy-lg']")
                if names != []:
                    print("Located Names")
                else:
                    driver.quit()
                    return
                
                descriptions = driver.find_elements(by="xpath",value="//div[@class='review-item-content col-xs-12 col-md-9']//p[@class='pre-white-space']")
                if descriptions != []:
                    print("Located Descriptions")
                else:
                    driver.quit()
                    return
                    
                # it is guaranteed that each review will have a name, description, and rating number
                for name in names:
                    # we do not want to add empty strings
                    if name.text!='':
                        nameList.append(name.text)
                print("There are ",len(nameList)," names")
                for description in descriptions:
                    descriptionList.append(description.text)
                    # we will use our determineRating function to add to the reviews
                    ratingNumbers.append(bias_parser.determineRating(description.text))
                # to prevent bot detection, loading each web-page 
                print("There are ",len(descriptionList)," descriptions")
                for description in descriptions:
                    print(description.text)
                    time.sleep(1)
                if(len(nameList)!=len(descriptionList)):
                    print("WARNING: Mismatched Lengths")
                    driver.quit()
                    return


                time.sleep(random.random())
            driver.quit()
            print("PANDAS: Converting to dataset")
            
            dataset = {
                "name": nameList,
                "description": descriptionList,
                "rating value": ratingNumbers
            }
            # print(len(nameList))
            # print(len(descriptionList))
            # print(len(ratingNumbers))
            # print(nameList)
            # print(ratingNumbers)
            # if len(nameList) != len(descriptionList) or len(nameList) != len(ratingNumbers) or len(descriptionList) != len(ratingNumbers):
            #     print("WARNING: Mismatched lengths for names and descriptions!")
            #     return
            frame = pd.DataFrame(dataset)
            print(frame)
            average = 1.0
            for number in ratingNumbers:
                average += number
            average/=len(frame)
            print("AVERAGE: ",average)
            # print("JSON: Storing file")
            frame.to_json("reviews.json",orient="records")
            return frame
        except:
            print("ERROR: We ran into an error midway")
        finally:
            driver.quit()
    
    print(scrape_reviews())

# run the application
run_script()