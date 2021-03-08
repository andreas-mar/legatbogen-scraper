from get_all_links import get_all_links
from parse_page import LegatbogenPage
import pandas as pd
import os

filename = 'legatbogen.xlsx'
all_links = get_all_links()
counter = 0


if os.path.exists(filename):
    current_df = pd.read_excel(filename, engine='openpyxl')
    current_values = current_df['Grant id'].values
    all_links = all_links[~all_links['grant_id'].isin(current_values)]
    all_data = current_df
    all_data = all_data[
        ['Link', 'Grant id', 'Firm name', 'Grant name', 'Avg annual amount', 'Portion size', 'Apply before',
         'Apply open', 'Response date', 'Payout date', 'Documentation required', 'Supported',
         'Not supported', 'Application method']]
else:
    all_data = pd.DataFrame()

for link in all_links['Page'].values:
    print(link)
    page = LegatbogenPage(link)
    page = page.get_data()
    all_data = pd.concat([all_data, page])
    # Save a checkpoint for every 50 iterations. Legatbogen does not have any mentionworthy security and throttling is not needed
    if counter % 50 == 0:
        all_data.to_excel(filename)
    counter += 1
