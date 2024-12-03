from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from seleniumbase import Driver  
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(r"--user-data-dir=C:\Users\user\AppData\Local\Google\Chrome\User Data")  # Adjust this
chrome_options.add_argument(r"--profile-directory=Profile 4")  # Adjust profile as needed

# Initialize SeleniumBase Driver for Cloudflare bypass
driver = Driver(uc=True)  # Enable undetected mode for bypassing Cloudflare.

try:
    print("Navigating to Indeed...")
    url = 'https://www.indeed.com'
    driver.get(url)  # Open the URL
    driver.uc_gui_click_captcha()  # Handle Cloudflare CAPTCHA if present
    time.sleep(5)  # Wait for the page to load after CAPTCHA

    print("Filling out the job search fields...")
    # Enter the job position
    what_elem = driver.find_element(By.ID, 'text-input-what')
    what_elem.send_keys('Data engineer')
    time.sleep(2)

    # Enter the location
    where_elem = driver.find_element(By.ID, 'text-input-where')
    where_elem.clear()  # Clear the location field
    where_elem.send_keys('USA')
    where_elem.send_keys(Keys.ENTER)  # Submit the form

    print("Job search initiated. Waiting for results...")
    time.sleep(10)  # Wait for the results page to load

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    print("Closing the browser...")
   

def extract_job_data(driver):
    job_data = []

    print("Extracting job listings...")
    # Locate all job containers
    job_containers = driver.find_elements(By.CSS_SELECTOR, "div.slider_container")

    if not job_containers:
        print("No job listings found.")
    else:
        for job in job_containers:
            try:
                # Extract job details
                job_title = job.find_element(By.CSS_SELECTOR, "h2.jobTitle").text
                company_name = job.find_element(By.CSS_SELECTOR, "span.companyName").text
                location = job.find_element(By.CSS_SELECTOR, "div.companyLocation").text

                print(f"Job Found: {job_title} at {company_name} in {location}")
                job_data.append([job_title, company_name, location])
            except Exception as e:
                print(f"Error extracting job details: {e}")
    
    return job_data




time.sleep(40)
driver.quit()































