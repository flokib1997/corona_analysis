from selenium import webdriver

# Initialize driver
driver = webdriver.Chrome()

# Wait up to 10 seconds for an element to load on the page before throwing an exception
driver.implicitly_wait(10)
