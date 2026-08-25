import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

driver = webdriver.Chrome()
#driver.maximize_window()

website_dict = {
    "https://www.amazon.com.tr/s?k={}": "Amazon",
    "https://www.hepsiburada.com/ara?q={}": "HepsiBurada",
    "https://www.trendyol.com/sr?q={}": "Trendyol"
    }

website_keys = list(website_dict.keys())
website_values = list(website_dict.values())

sort_class_dict = {
                    ".a-button-text.a-declarative": 'a#s-result-sort-select_1', #value uses tag and id
                   ".horizontalSortingBar-Ce404X9mUYVCRa5bjV4D":".horizontalSortingBar-PkoDOH7UsCwBrQaQx9bn",
                   ".select-box":'li#select-option-PRICE_BY_ASC' #value uses tag and id
                   }

sort_keys= list(sort_class_dict.keys())
sort_values = list(sort_class_dict.values())

product_class_dict = {
                        ".a-size-base-plus.a-spacing-none.a-color-base.a-text-normal":".a-offscreen",
                        ".title-module_titleRoot__dNDiZ":".price-module_finalPrice__LtjvY",
                        ".product-name":'[data-testid="price-section"]',
                    }

product_keys = list(product_class_dict.keys())
product_values = list(product_class_dict.values())


search_input = ''

while True:
        search_input = input("Enter what product you want to search (q to exit): ")
        formatted_search = search_input.replace(" ", "+")

        data_dict = {}
        data_name_list = []
        data_price_list = []
        if search_input.upper() == 'Q':
            break
        with open("PriceList.md", "a+") as f:
            f.write(f"# Top 3 cheapest {search_input} \n\n")
            i = 0
            for website in website_dict:
                #try:
                search_url = website.format(formatted_search)
                driver.get(search_url)

                WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, sort_keys[i])))

                sort_dropdown = driver.find_element(By.CSS_SELECTOR, sort_keys[i])
                driver.execute_script("arguments[0].click();", sort_dropdown)
                WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, sort_values[i])))

                asc_prices_label = driver.find_element(By.CSS_SELECTOR, sort_values[i])
                driver.execute_script("arguments[0].click();", asc_prices_label)
                time.sleep(2)

                WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, product_keys[i])))

                data_name_list = driver.find_elements(By.CSS_SELECTOR, product_keys[i])[:3]
                data_price_list = driver.find_elements(By.CSS_SELECTOR, product_values[i])[:3]

                print(f"name_list: {data_name_list}\nprice_list: {data_price_list}")

                for ix in range(len(data_name_list)):
                    f.write(f"**Source:** *{website_values[i]}*  \n")
                    f.write(f"**Full Description:** {data_name_list[ix].text}  \n**Price: *{data_price_list[ix].get_attribute("textContent").strip()}***  \n  \n  \n")

                i+=1
                """except Exception as e:
                    i+=1
                    print(e)
                    continue"""









time.sleep(10)
