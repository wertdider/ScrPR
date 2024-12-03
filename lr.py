from seleniumbase import Driver  # For Cloudflare bypass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Initialize the driver with undetected mode
driver = Driver(uc=True)

def save_to_csv(data, filename="vacancies.csv"):
    """
    Saves job data to a CSV file.
    """
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Job Title", "Company Name", "Location", "Salary"])  # CSV header
            writer.writerows(data)
        print(f"Data saved to {filename}.")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def extract_one_job_data(driver):
    """
    Extract details of one job listing.
    """
    print("Extracting one job listing...")
    try:
        # Wait for job title element to be present and extract it using XPath
        job_title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[@class='jobsearch-JobInfoHeader-title']"))
        )
        job_title = job_title_element.text

        # Extract company name
        try:
            company_name_element = driver.find_element(By.CSS_SELECTOR, "div.jobsearch-InlineCompanyRating div:first-child")
            company_name = company_name_element.text
        except Exception as e:
            print(f"Error extracting company name: {e}")
            company_name = "Not specified"

        # Extract location
        try:
            location_element = driver.find_element(By.CSS_SELECTOR, "div.jobsearch-InlineCompanyRating div:nth-child(2)")
            location = location_element.text
        except Exception as e:
            print(f"Error extracting location: {e}")
            location = "Not specified"

        # Extract salary (broader approach with XPath)
        try:
            salary_element = driver.find_element(By.XPATH, "//div[contains(@class, 'jobsearch-JobMetadataHeader-item')]")
            salary = salary_element.text
        except Exception as e:
            print(f"Error extracting salary: {e}")
            salary = "Not specified"

        print(f"Extracted: {job_title}, {company_name}, {location}, {salary}")
        return [[job_title, company_name, location, salary]]  # Return as a list of lists
    except Exception as e:
        print(f"Error extracting job info: {e}")
        return []  # Return an empty list if extraction fails


def main():
    """
    Main function to search and extract job data.
    """
    try:
        print("Navigating to Indeed...")
        driver.get("https://www.indeed.com")
        time.sleep(5)  # Wait for Cloudflare bypass

        # Enter search criteria
        print("Performing job search...")
        driver.find_element(By.ID, "text-input-what").send_keys("Data Engineer")
        where_elem = driver.find_element(By.ID, "text-input-where")
        where_elem.clear()  # Clear the location field
        where_elem.send_keys("USA")
        where_elem.submit()  # Submit the search form
        time.sleep(5)  # Wait for results to load

        # Extract one job listing
        job_data = extract_one_job_data(driver)
        if job_data:
            # Save data to CSV
            save_to_csv(job_data)
        else:
            print("No data to save.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Closing the browser...")
        driver.quit()


if __name__ == "__main__":
    main()
