# Crossword scraper

## Usage

Script for parsing data from a crossword website into a database

## Installation

1. Clone repository: `git clone https://github.com/JackSoer/crossword-scraper.git`

2. Create a virtual environment (venv):

Use the following command to create a virtual environment:

python -m venv venv

If you are using Python version 3.3 or older, use virtualenv instead of venv:

virtualenv venv

3. Activate the virtual environment:

On the Windows command line:

source venv\Scripts\activate

In a Unix terminal:

source venv/bin/activate

You will see that your command line now starts with (venv).

3. Install dependencies from the requirements.txt file:

pip install -r requirements.txt

4. Create mysql and redis databases

5. Create a .env file in your project root folder.

Copy the variables from the .env.example file there and write down the data for connections to your mysql and redis databases.

6. Go to your project's Spiders folder:

cd crosswordscraper/crosswordscraper/spiders

7. Run these scripts:

scrapy crawl redisurlsspider
scrapy crawl crosswordspider

Now you can check your data in the MySQL database.
