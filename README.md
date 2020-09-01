# snowmass-loi-scraper

Scrape Snowmass LOI information from the Snowmass website. This script is provide as-is with **no** support.

### Installation

This package provides a standalone python script `scrape.py`. You can grab this repository with:
```
git clone https://github.com/kadrlica/snowmass-loi-scraper.git
```
You could also grab the script directly with:
```
wget https://github.com/kadrlica/snowmass-loi-scraper.git
```

### Execution

To generate a CSV file that parses out all the topical groups from the filename, run:
```
python scrape.py
```

You can also scrape a specific frontier
```
python scrape.py -f CF
```
This will produce a CSV file with the filename, frontier, submission number, and topical groups. You can parse and filter this CSV as you wish.

### Dependencies

* Python 2/3
* requests
* lxml
* numpy
* pandas
