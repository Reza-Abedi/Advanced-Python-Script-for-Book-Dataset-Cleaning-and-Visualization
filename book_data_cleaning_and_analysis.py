# Data Cleaning Script For book data
# Input Dir: dataset/input
# Output Dir: dataset/clean

# Importing necessary libraries
from functools import reduce
import numpy as np
import pandas as pd
import string
import matplotlib.pyplot as plt

# Function to remove non-ASCII characters
def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i) < 128)

# Reading data from Excel file
df_book = pd.read_excel("dataset/input/books.xlsx")
df_book.head()

# Columns to drop from the dataframe
to_drop = ['Edition Statement', 'Corporate Author', 'Corporate Contributors',
           'Former owner', 'Engraver', 'Contributors', 'Issuance type', 'Shelfmarks']
df_book.drop(columns=to_drop, inplace=True)

# Cleaning Date of Publication
regex = r'^.*(\d{4}).*'
date_regex = r'(\D)(\d{4})(.$)'
date_num = df_book['Date of Publication'].str.replace(date_regex, r'\2')  # extracting group 2- 4 digi date
date_num = df_book['Date of Publication'].str.replace('\s\[.*\]', "")  # removing extras chars and date with []
date_num = date_num.str.replace('.*(\d{4}).*', r'\1')  # removing extras leading and trailing chars
df_book['Date of Publication'] = date_num  # assigning cleaned data to date'
df_book["Date Extracted From PP"] = df_book['Place of Publication'].str.extract("(\d{4})")  # Some date data are found in place of pulbicaiton so, extracting those from and stroing in new date column
df_book['Date of Publication'].fillna(df_book['Date Extracted From PP'], inplace=True)  # filling the old date column's null cell from new date column
df_book = df_book[df_book['Date of Publication'].str.contains('^(\d{4})')]

# Cleaning Place Of Publication
pub = df_book['Place of Publication']
df_book['Place of Publication'] = np.where(pub.str.contains('London'), 'London',
                                           np.where(pub.str.contains('Oxford'), 'Oxford',
                                                    np.where(pub.eq('Newcastle upon Tyne'),
                                                             'Newcastle-upon-Tyne', df_book['Place of Publication'])))
df_book['Place of Publication'] = np.where(pub.str.contains('London'), 'London',
                                           np.where(pub.str.contains('Oxford'), 'Oxford',
                                                    pub.str.replace('-', ' ')))
df_book['Place of Publication'] = df_book['Place of Publication'].apply(remove_non_ascii)  # Removing non-ascii chars
# df_book = df_book[df_book['Place of Publication'].str.contains(r'^[A-Za-z]+$')]
pub_place_key = df_book[df_book['Place of Publication'].str.contains(r'^[A-Za-z]+$')]['Place of Publication'].tolist()
df_filter = df_book['Place of Publication'].apply(lambda x: pub_place_key[pub_place_key.index(x)] if x in pub_place_key else x)
df_book['Place of Publication'] = df_filter
df_book['Place of Publication'] = df_book['Place of Publication'].str.replace(r'^[\[\]\\_+!@#$?^ \d]+', '')
df_book['Place of Publication'] = df_book['Place of Publication'].str.replace(r'^[ ]+', '')
df_book['Place of Publication'] = df_book['Place of Publication'].str.replace(r'[ ]+$', '')
df_book['Place of Publication'] = df_book['Place of Publication'].str.replace(r'[\[\]\\_+!@#$?^ \d]+$', '')
df_book['Place of Publication'] = df_book['Place of Publication'].str.replace(r'.*?:.*([A-Z][a-z]+).*', r'\1')
df_book['Place of Publication'] = df_book['Place of Publication'].str.replace(r'.*([A-Z][a-z]+);.*', r'\1')
df_book['Place of Publication'] = df_book['Place of Publication'].str.replace(r'.*([A-Z][a-z]+.*),.*', r'\1')
df_book['Place of Publication'] = df_book['Place of Publication'].str.replace(r'^([a-z][ ]).*', '')
df_book['Place of Publication'] = df_book['Place of Publication'].str.replace(r'.*([A-Z].*)', r'\1')

# df_book['Place of Publication'] = df_book['Place of Publication'].str.replace(r'(\w)+([,])+(.*)', r'\1')
# df_book['Place of Publication'] = df_book['Place of Publication'].str.replace(r'(.*)(\s)+(.*)', r'\2')
df_book = df_book[df_book['Place of Publication'].notna()]

import re

# Cleaning Title and Extracting Author From Title
author_from_title = df_book['Title'].str.extract(r'\[[bB]y (.*?)\]')
author_from_title = author_from_title[author_from_title[0].notna()]
df_book['Author'].fillna(author_from_title[0], inplace=True)  # filling the old date column's null cell from new date column

author_from_title1 = df_book['Title'].str.extract(r'\[.*i\.e\. (.*?)\]')
author_from_title1 = author_from_title1[author_from_title1[0].notna()]
df_book['Author'].fillna(author_from_title1[0], inplace=True)  # filling the old date column's null cell from new date column

author_from_title2 = df_book['Title'].str.extract(r'\[.*?[bB]y (.*?)\]')
author_from_title2 = author_from_title2[author_from_title2[0].notna()]
df_book['Author'].fillna(author_from_title2[0], inplace=True)  # filling the old date column's null cell from new date column

author_from_title3 = df_book['Title'].str.extract(r'\[.*?[bB]y (.*?)\]')
author_from_title3 = author_from_title3[author_from_title3[0].notna()]
df_book['Author'].fillna(author_from_title3[0], inplace=True)  # filling the old date column's null cell from new date column

author_from_title4 = df_book['Title'].str.extract(r'\[(.*?)\]')
author_from_title4 = author_from_title4[author_from_title4[0].notna()]
df_book['Author'].fillna(author_from_title4[0], inplace=True)  # filling the old date column's null cell from new date column
df_book = df_book[df_book['Author'].apply(lambda x: len(str(x)) <= 35)]  # Assuming 35 be max author name

df_book['Title'] = df_book['Title'].str.title()  # Title Case
df_book['Title'] = df_book['Title'].str.replace(r'(.*)(By)(.*)', r'\1')  # Delimit the Title 'By' to separate Title part from other aux. info.
df_book['Title'] = df_book['Title'].str.replace(r'([\w ]{4})(\.)(.*)', r'\1.')  # Title Part Before First Period
df_book['Title'] = df_book['Title'].str.replace(r'\[|\]|^\[|\[$', '')  # Removing extra & enclosing [] braces
df_book['Title'] = df_book['Title'].str.replace(r'[\[\]\_+!@#$?^]+$', '')  # Removing extra leading and trailing chars
df_book['Title'] = df_book['Title'].str.replace(r'^\.', '')  # Removing Leading Period
df_book['Title'] = df_book['Title'].apply(remove_non_ascii)  # Removing non-ascii chars
df_book = df_book[df_book.Title.str.contains('^[\w]+\.*')]  # Removing any char not beginning with \w

# Cleaning Author
def clean_author_names(item):
    author = str(item.loc['Author'])

    if author == 'nan':
        return np.NaN

    author = author.split(',')

    if len(author) == 1:
        name = filter(lambda x: x.isalpha(), author[0])
        return reduce(lambda x, y: x + y, name)

    last_name, first_name = author[0], author[1]

    first_name = first_name[:first_name.find('-')] if '-' in first_name else first_name

    if first_name.endswith(('.', '.|')):
        parts = first_name.split('.')

        if len(parts) > 1:
            first_occurrence = first_name.find('.')
            final_occurrence = first_name.find('.', first_occurrence + 1)
            first_name = first_name[:final_occurrence]
        else:
            first_name = first_name[:first_name.find('.')]

    last_name = last_name.capitalize()
    last_name = remove_non_ascii(last_name)
    first_name = remove_non_ascii(first_name)

    return f'{first_name} {last_name}'

# Final cleaning and dropping NA values
df_book['Author'] = df_book.apply(clean_author_names, axis=1)
df_book.drop('Date Extracted From PP', axis=1, inplace=True)
df_book.to_excel('dataset/clean/book_cleaned.xlsx', index=False)
print('\nNote: Clean Dataset is saved under: dataset/clean/book_cleaned.xlsx')
# print(df_book.isna().sum())  # -> It checks sum  of NA value in each column

# Making Graph To Visualize Date of Publication and No of Publication
def pub_date_graph():
    # plt.clear("all")
    x = df_book['Date of Publication'].tolist()
    x = list(set(x))
    y = df_book.pivot_table(index=['Date of Publication'], aggfunc='size')

    fig, ax = plt.subplots()
    ax.plot(y)
    x_tick = [x[i] if int(x[i]) % 36 == 0 else 0 for i in range(len(x))]
    x_tick = list(filter(lambda a: a != 0, x_tick))
    ax.xaxis.set_ticks(x_tick)
    plt.title("Plotting Graph Showing No of Publication Over Year")
    plt.ylabel('No of Publication')
    plt.xlabel("Year of Publication")
    plt.show()

# Making Graph to Visualize No of Books Per Author
def author_graph():
    print(
        "It's a huge dataset, enter a range (lower and higher limit, e.g., 10, 20 - it will pick data from index 10 to 20). Max, you can visualize 20 data at a time, higher limit - " + str(
            df_book.shape[0] - 1))
    limit1 = int(input("Enter lower limit: "))
    limit2 = int(input("Enter higher limit: "))
    if (limit2 - limit1 > 20):
        raise Exception("Max 20 Record at a time allowed!")
        return
    y = df_book.pivot_table(index=['Author'], aggfunc='size').to_frame()
    y_lim = y.iloc[limit1:limit2]
    y_lim = y_lim.squeeze()
    y_lim.plot.barh()
    plt.title("Horizontal Bar Graph Showing No Of Books Per Author")
    plt.xlabel("No of books")
    plt.ylabel("Author Name")
    plt.show()

def book_place_graph():
    print(
        "It's a huge dataset, enter a range (lower and higher limit, e.g., 10, 20 - it will pick data from index 10 to 20). Max, you can visualize 20 data at a time, higher limit - " + str(
            df_book.shape[0] - 1))
    limit1 = int(input("Enter lower limit: "))
    limit2 = int(input("Enter higher limit: "))
    if (limit2 - limit1 > 20):
        raise Exception("Max 20 Record at a time allowed!")
        return
    # plt.clear("all")
    y = df_book.pivot_table(index=['Place of Publication'], aggfunc='size').to_frame()
    y_lim = y.iloc[limit1:limit2]
    y_lim = y_lim.squeeze()
    y_lim.plot.barh()
    plt.title("Horizontal Bar Graph Showing No Of Books Per Author")
    plt.xlabel("No of books")
    plt.ylabel("Publishing City")
    plt.show()

def visualize_choice():
    choice = int(
        input("\n1: Graph Over Publication Year\n2: Number of books per author\n3: No of books per city\n4: Exit Program\nEnter Your Choice:"))
    if (not isinstance(choice, int) and choice not in [1, 2, 3]):
        raise Exception("Enter a number between 1-3!")
        return
    if choice == 4:
        exit()
    print("It may take time to draw a graph, please be patient!\nPlease close before you provide new input for drawing a new graph\n")
    if choice == 1:
        pub_date_graph()
    elif choice == 2:
        author_graph()
    elif choice == 3:
        book_place_graph()
    else:
        raise Exception("Input Error!")

# Main loop for continuous user interaction
while True:
    visualize_choice()
