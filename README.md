# Overview
This project has some scripts to download weekly auction results from https://domain.com.au.

A sample of the data is in `sample.csv`

# Setup
Run the below to intall the requirerd packages.

```$pip install -r requirements.txt```

# Use
To download auction results from `startdate` to `enddate` use the command below:

```$python download_auction_results.py --startdate 2019-02-02 --enddate 2019-03-02 --outcsv test.csv```

Make sure startdate is a Saturday, which is the day when results are published.

(To be updated)
