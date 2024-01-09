# Blinq
**A data analysis exercise**

This repository contains code related to a test provided by [Blinq](https://blinq.me) in the technical phase of its interviewing process for a Senior Data Engineer role.

## Overview
The required solution is a command prompt utility that reads data from a [public API](https://data.gov.au/data/api/1/util/snippet/api_info.html?resource_id=55ad4b1c-5eeb-44ea-8b29-d410da431be3), which provides data about business name registrations in Australia.

The tool should provide some parameters for filtering and result visualisation, as described further below.

## Requirements
- Python 3.x

## Set up
Clone the repository and enter the created directory:

`git clone https://github.com/paulofelipe84/blinq.git`

`cd blinq`

To install dependencies, run: 

`pip install -r requirements.txt`

## Usage

```
python business_names.py [-h] [--registration_date_from REGISTRATION_DATE_FROM] [--registration_date_to REGISTRATION_DATE_TO] (--business_name BUSINESS_NAME | --business_name_similar_to BUSINESS_NAME_SIMILAR_TO) [--limit LIMIT] [--display_format {table,graph}]
```

### Options
* `--registration_date_from` (date): Initial date (DD/MM/YYYY) of a range of business registration dates.
* `--registration_date_to` (date): Final date (DD/MM/YYYY) of a range of business registration dates.
* `--business_name` (text): Name of the business to be searched (exact match/case insensitive).
* `--business_name_similar_to` (text): Text for a search on similar business names (case insensitive).
* `--limit` (number) Limit number of records in the results. Default is 10.
* `--display_format` (text) Display format of the result. Choices: 
    * `table` (default): displays results in a tabular format
    * `graph`: displays results as a trend graph on the number of businesses registered that match the searched criteria, by month.

### Example
To list all businesses with the name containing the word "nourishing" registered after 01/01/2018, run:

`python business_names.py --business_name_similar_to "nourishing" --registration_date_from 01/01/2018`


## Candidate comments
I found this exercise quite interesting and engaging while complex, when considering the desired timeframe of 3 hours.
I spent a good amount of time understanding the [API usage](https://data.gov.au/data/api/1/util/snippet/api_info.html?resource_id=55ad4b1c-5eeb-44ea-8b29-d410da431be3), which is not very well documented (even one example provided is not working). I ended assuming I should use the existing datastore `55ad4b1c-5eeb-44ea-8b29-d410da431be3`.

I chose to use SQL search since it gives more flexibility, while the regular search parameters are not provided in [the documentation](https://docs.ckan.org/en/latest/api/index.html). That caused limitations to meet the third requirement (business name similarity matching, sorted by result similarity). Instead, I implemented a classic `LIKE` condition with the similarity parameter.

Since I wanted to make it easy to use (and did not have enough time for testing) I ended implementing the graph visualisation functionality on the prompt command itself, which limited options for different visualisations. Also, the API dataset results do not have attributes enough for a more 'inspired' visualisation, which also limited my options and made me provide only 2 choices rather than the required 3.

In conclusion, I'm happy with the results achieved even though not meeting all the requirements, and I hope this is enough to drive me to the next interviewing steps.