import pandas as pd
import requests
import xmltodict


# Read data
def get_all_links(export=False):
    r = requests.get('https://api.legatbogen.dk/api/sitemap')
    xml_data = r.text

    # Parse XML
    xmlDict = xmltodict.parse(xml_data)

    # Empties for later filling
    pages = []
    change_freq = []
    cols = ['Page', 'Change Frequency']

    # Extract data
    for url in xmlDict['urlset']['url']:
        pages.append(url['loc'])
        change_freq.append(url['changefreq'])

    # Slicing data and extracting grant identifier
    df = pd.DataFrame(list(zip(pages, change_freq)), columns=cols)
    df['keep'] = df['Page'].str.contains(pat='stoetteomraade')
    df = df[df['keep'] == True]
    del df['keep']
    df['grant_id'] = df['Page'].apply(lambda x: str(x.split('/')[-1]))

    if export:
        df.to_excel('all_pages_legatbogen.xlsx')

    return df


if __name__ == '__main__':
    print(get_all_links(export=True))
