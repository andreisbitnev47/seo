import numpy as np
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('pending.csv')
dataset.head()
filtered = dataset.iloc[:, 6:]

kwds = pd.read_csv('kw_test.csv')
kwds_filtered = kwds.iloc[:, 5:]

dataset_sold = dataset[dataset.sold.str.find('Sold') != -1]
dataset_sold_filtered = dataset_sold.loc[lambda x : x.sold == x.sold]

starting_csv = pd.read_csv('ebay_5.csv').loc[lambda x : x.title != x.title]
start_href = starting_csv.iloc[:, 3]

starting_titles = []
    
for index, row in starting_csv.iterrows():
    title = row['keyword_link-href'].replace("https://app.kwfinder.com/dashboard?keyword=", "")
    title = title.replace("&language_id=0&location_id=0&source_id=0", "")
    title = title.replace("%20", " ")
    starting_titles.append(title)
    
dataset_500 = pd.read_csv('dataset_500.csv').to_csv(index=0).lower().split('\n')
for title in starting_titles:
    if title in dataset_500:
        dataset_500.remove(title)

dataset_500_csv = '\n'.join(dataset_500)

# sort ebay scraped list by price * qnt, return only titles
ebay = pd.read_csv('kws/all_raw.csv')
ebay_unique = ebay.drop_duplicates(subset='title')
ebay_sold = ebay_unique.loc[ebay_unique.sold.str.find('sold') != -1][lambda x : x.sold == x.sold]
ebay_list = []
for index, row in ebay_sold.iterrows():
   ebay_sold.at[index, 'sold'] = int(row['sold'].replace(' sold', '').replace('+', '').replace(',', ''))
   ebay_sold.at[index, 'price'] = float(row['price'].replace('Tap item to see current priceSee Price', '1').replace('$ ', '').replace('$', '').replace(',', '').split(' ')[0])
for index, row in ebay_sold.iterrows():
   # add only items that cost more than 25$
   if row['price'] >= 25:
       ebay_list.append({'title': row['title'], 'price': row['price'], 'sold': row['sold']})
ebay_list.sort(key=lambda x: x['price'] * x['sold'], reverse=True)
ebay_sorted = pd.DataFrame(ebay_list)
ebay_kw_sorted_csv = ebay_sorted.iloc[:, 2].to_csv(index=0)
ebay_sorted_csv = ebay_sorted.to_csv(index=0)

# sort scraped keyword as ininitla_kw => suggested_kws, leave title, volume, cps, ppc kw_difficulty
scraped = pd.read_csv('kws/motors/parts_accessories/scraped_raw.csv')
scraped_ordered = scraped.sort_values(by=['web-scraper-order']).iloc[:, 4:].to_csv(index=0)

# sort out keywords, that were already scraped
used_kws = pd.read_csv('kws/home/improvement/kw_inwork.csv')
scraped_kws = pd.read_csv('kws/home/improvement/scraped_raw.csv')['title'].values.tolist()
unused_kws_list = []
for index, row in used_kws.iterrows():
    if row['title'].lower() not in scraped_kws:
        unused_kws_list.append(row['title'])
unused_kws_csv = pd.DataFrame(unused_kws_list).to_csv(index=0)



# sort scraped list by difficulty
scraped = pd.read_csv('kws/motors/parts_accessories/scraped_raw.csv')
scraped_kw_difficulty = scraped.drop_duplicates(subset='title').sort_values(by=['kw_difficulty'], ascending=True).iloc[:, 4:].to_csv(index=0)

# sort scraped list by volume
scraped = pd.read_csv('kws/industrial/agriculture/scraped_raw.csv')
for index, row in scraped.iterrows():
   scraped.at[index, 'volume'] = int(str(row['volume']).replace('nan', '0').replace(',', ''))
scraped_volume = scraped.drop_duplicates(subset='title').sort_values(by=['volume'], ascending=False).iloc[:, 4:].to_csv(index=0)

# sort ebay data by page
ebay_raw = pd.read_csv('kws/home/baby/raw.csv')
ebay_by_page = ebay_raw.sort_values(by=['page', 'category']).to_csv(index=0)

website_names = dataset.iloc[:, 4]

# import pending expiration domains and sort by tf
domains = []
dataset = pd.read_csv('pending.csv')
dataset_ordered = dataset.sort_values(by=['TF'], ascending=False)
for index, row in dataset_ordered.iterrows():
   # add only items that cost more than 25$
   if row['TR'] < 1.5:
       domains.append({'endDate': row['End Date'], 'BL': row['BL'], 'DP': row['DP'], 'TF': row['TF'], 'CF': row['CF'], 'TR': row['TR'], 'domain': row['Domain']})
domains_dataframe = pd.DataFrame(domains)

# import deleted domains and sort by tf
domains = []
dataset = pd.read_csv('deleted_eu.csv')
dataset_ordered = dataset.sort_values(by=['TF'], ascending=False)
for index, row in dataset_ordered.iterrows():
   # add only items that cost more than 25$
   if row['TR'] < 1.5:
       domains.append({'BL': row['BL'], 'DP': row['DP'], 'TF': row['TF'], 'CF': row['CF'], 'TR': row['TR'], 'domain': row['Domain']})
deleted_domains_dataframe = pd.DataFrame(domains)