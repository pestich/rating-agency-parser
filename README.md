# Rating Agencies Press Release Parser

This project is a web scraper designed to extract data from press releases published by rating agencies. It utilizes the Selenium and BeautifulSoup4 libraries. The primary goal of the project is to collect data for subsequent analysis. The obtained data will be used for building a machine learning classification model and identifying key constructs within the text.

## Why is this necessary?

Rating agencies regularly release press releases containing information about their ratings, analytical reviews, and assessments of companies and financial instruments. This data can be highly valuable for market analysis, evaluating the financial stability of companies, and other financial research purposes.

## How does the parser work?

1. **Selenium**: We use the Selenium library to automate web browsing. This enables us to navigate to the websites of rating agencies, authenticate (if required), and access pages with press releases.

2. **BeautifulSoup4**: After loading the pages with press releases, we employ the BeautifulSoup4 library to parse the HTML and extract the necessary information. This includes headlines, press release text, publication dates, and other relevant data.

3. **Data Storage**: The extracted data is saved in a structured format that can be used for analysis and training a machine learning model.
