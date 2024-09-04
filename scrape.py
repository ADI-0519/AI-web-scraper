from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

SBR_WEBDRIVER = 'https://brd-customer-hl_b259e7ce-zone-ai_scraper:e9y0je63v554@brd.superproxy.io:9515'

def scrape_website(website):
    print("launching chrome browser") # Tell what we are doing

    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome') #Set up remote connection to brightdata

    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(website) # Grab data
        # CAPTCHA handling: If you're expecting a CAPTCHA on the target page, use the following code snippet to check the status of Scraping Browser's automatic CAPTCHA solver
        print('Waiting captcha to solve...')
        solve_res = driver.execute('executeCdpCommand', {
         'cmd': 'Captcha.waitForSolve',
         'params': {'detectTimeout': 10000},
         })
        print('Captcha solve status:', solve_res['value']['status'])
        print('Navigated! Scraping page content...')
        html = driver.page_source
        return html
    

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser") #creates a beautiful soup object which takes the HTML content as input
    body_content = soup.body
    if body_content:
        return str(body_content)
    else:
        return ""
    


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script","style"]): # look for any scripts or style and extract them
        script_or_style.extract()

    cleaned_content = soup.get_text(separator = "\n") # separate items by lines
    cleaned_content = "\n".join(

        line.strip() for line in cleaned_content.splitlines() if line.strip()
        
    )

    return cleaned_content

def split_dom_content(dom_content, max_length = 6000):
    return [dom_content[i:i+max_length] for i in range(0,len(dom_content),max_length)]
