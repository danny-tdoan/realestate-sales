import argparse
import extractor
import pandas as pd
import datetime
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(process)s %(levelname)s %(message)s',
    filename='/tmp/get-domains.log',
    filemode='a'
)

ROOT_URL = 'https://www.domain.com.au/auction-results/melbourne/'
all_results_df = None


def arg_parser():
    parser = argparse.ArgumentParser(
        description='Scrape auction and private sale results from domain.com.au',
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--startdate', type=str, required=True,
                        help='Start date to extract data in format YYYY-mm-dd. Make sure it is a Saturday')
    parser.add_argument('--enddate', type=str, required=True,
                        help='End date to extract data in format YYYY-mm-dd')
    parser.add_argument('--outcsv', type=str, required=False, default='results.csv',
                        help='Output csv location')
    return parser


if __name__ == '__main__':
    args = arg_parser().parse_args()

    startdate = datetime.datetime.strptime(args.startdate, '%Y-%m-%d')
    enddate = datetime.datetime.strptime(args.enddate, '%Y-%m-%d')
    outcsv = args.outcsv

    while startdate < enddate:
        date = startdate.strftime('%Y-%m-%d')
        logging.debug('Extracting data for date {}'.format(date))

        url = ROOT_URL + date
        response = extractor.get_one_page(url)
        all_suburbs = extractor.extract_all_suburbs(response)

        results = []
        for suburb in all_suburbs:
            suburb_name, all_properties = extractor.extract_one_suburb_section(
                suburb)

            for property in all_properties:
                results.append(extractor.extract_one_property(
                    suburb_name, property))

        results_df = pd.DataFrame(results)
        results_df['date'] = date
        if all_results_df is None:
            all_results_df = results_df
        else:
            all_results_df = pd.concat([all_results_df, results_df])

        logging.debug('Extracted {} properties up to {}'.format(
            all_results_df.shape[0], startdate))
        startdate = startdate + datetime.timedelta(days=7)

    all_results_df.to_csv(outcsv, index=False)
