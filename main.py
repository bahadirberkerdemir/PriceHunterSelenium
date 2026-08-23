from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

driver = webdriver.Chrome()
#driver.maximize_window()

website_dict = {
                "www.amazon.com.tr": ".nav-input.nav-progressive-attribute",
                "www.hepsiburada.com":".searchBarContent-UfviL0lUukyp5yKZTi4k",
                "www.trendyol.com":".search-bar-new-input-active-field"
                }
website_keys = list(website_dict.keys())

sort_class_dict = {
                    ".a-button-text.a-declarative": '[tabindex="0"]',
                   ".horizontalSortingBar-Ce404X9mUYVCRa5bjV4D":".horizontalSortingBar-PkoDOH7UsCwBrQaQx9bn",
                   ".select-box":'[tabindex="-1"]'
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

while search_input.upper() != 'Q':
    search_input = input("Enter what product you want to search (q to exit): ")

    data_dict = {}
    data_name_list = []
    data_price_list = []

    if not search_input.upper() == 'Q':
        with open("PriceList.md", "a+") as f:
            f.write(f"# Top 3 cheapest {search_input} \n\n")

            for website, search_class in website_dict.items():
                i=0
                driver.get(f"https://{website}")

                WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, search_class)))

                search_bar = driver.find_element(By.CSS_SELECTOR, search_class)
                search_bar.send_keys(search_input)
                search_bar.send_keys(Keys.ENTER)
                WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, sort_keys[i])))

                sort_dropdown = driver.find_element(By.CSS_SELECTOR, sort_keys[i])
                sort_dropdown.click()
                WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, sort_values[i])))

                asc_prices_label = driver.find_element(By.CSS_SELECTOR, sort_values[i])
                asc_prices_label.click()

                WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, product_keys[i])))

                data_name_list = driver.find_elements(By.CSS_SELECTOR, f"{product_keys[i]}:nth(-n+3)")
                data_price_list = driver.find_elements(By.CSS_SELECTOR, f"{product_values[i]}:nth(-n+3)")

                print(f"name_list: {data_name_list}\nprice_list: {data_price_list}")

                for ix in range(len(data_name_list)):
                    f.write(f"##**Source:** *{website_keys[i]}*\n")
                    f.write(f"###**Full Description:** {data_name_list[ix]}\n**Price: *{data_price_list[ix]}***\n\n\n")

                i+=1







