import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


# Function to extract anchor texts and links from URL
def extract_anchors_from_url(url):
    try:
        response = requests.get(url,timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        anchors = [{'text': a.text.strip().replace('\n',''), 'href': a['href']} for a in soup.find_all('a', href=True)]
        return anchors
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return []
# Function to perform sentiment analysis
def get_sentiment(text):
    if text:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        return polarity
    else:
        return None

def read_text_from_url(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url,timeout=20)
        
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        
        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get the text content from the parsed HTML
        text = soup.get_text(separator='\n', strip=True)
        
        return text
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        print(f"Error fetching data from {url}: {e}")
        return None
def join_url(base_url, *paths):
    """
    Joins a base URL with one or more paths.
    
    :param base_url: The base URL to which paths will be joined.
    :param paths: Additional paths to join to the base URL.
    :return: The resulting URL after joining the base URL with the paths.
    """
    url = base_url
    for path in paths:
        url = urljoin(url, path)
    return url

# Function to calculate TF-IDF
def compute_tfidf(txt):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([txt])
    feature_names = vectorizer.get_feature_names_out()
    dense = tfidf_matrix.todense()
    denselist = dense.tolist()
    tfidf_df = pd.DataFrame(denselist, columns=feature_names)
    return tfidf_df

# Function to calculate sentiment polarity
def compute_sentiment(df):
    df['polarity'] = df['text'].apply(lambda x: TextBlob(x).sentiment.polarity)
    return df

# Function to check if two links are from the same host
def are_same_host(url1, url2):
    #print(urlparse(url2))
    return urlparse(url1).netloc == urlparse(url2).netloc

# Function to process each row
def process_row(row):
    url = row['URL']
    anchors = extract_anchors_from_url(url)
    for anchor in anchors:
        if anchor['href']:
            
            full_url = urljoin(url, anchor['href']) if are_same_host(url, anchor['href']) or urlparse(anchor['href']).netloc == '' else anchor['href']
            txt = read_text_from_url(full_url)
            if txt== None: continue
            try:
                sep = TextBlob(txt).sentiment.polarity
                tfidf_df = compute_tfidf(txt)
            except Exception as e:
                print(f"Error processing URL {url}: {e}")
                continue 
            keywords = ', '.join(tfidf_df.columns)
            print(url,keywords,sep)
            bay.append({'URL': url, 'Anchor': anchor['text'], 'Link': anchor['href'], 'Keywords': keywords, 'Sentiment': sep})

# Function to search for a keyword in the DataFrame
def search_by_keyword(df, keyword):
    keyword = keyword.lower()  # Ensure the keyword search is case-insensitive
    search_result = df[df['Keywords'].str.contains(keyword, case=False, na=False)]
    return search_result

# Function to save a DataFrame to a CSV file
def save_dataframe(df, filename):
    try:
        df.to_csv(filename, index=True)
        print(f"DataFrame saved to {filename}")
    except Exception as e:
        print(f"Error saving DataFrame to {filename}: {e}")

# Function to load a DataFrame from a CSV file
def load_dataframe(filename):
    try:
        df = pd.read_csv(filename, index_col='Sentiment')
        print(f"DataFrame loaded from {filename}")
        return df
    except Exception as e:
        print(f"Error loading DataFrame from {filename}: {e}")
        return None

# Function to search for a keyword in the DataFrame
def search_by_keyword(df, keyword):
    keyword = keyword.lower()  # Ensure the keyword search is case-insensitive
    search_result = df[df['Keywords'].str.contains(keyword, case=False, na=False)]
    return search_result


bay=[]
url = "https://raw.githubusercontent.com/pacobaco/lip/master/f3.txt"
response = requests.get(url)
text_data = response.text

# Split the text data into individual lines
lines = text_data.split("\n")[:20]

# Create a DataFrame
df = pd.DataFrame(lines, columns=["URL"])

# Apply the function to each row
df.apply(process_row, axis=1)

# Convert bay to DataFrame
result_df = pd.DataFrame(bay)

# Set the index to sentiment polarity
result_df.set_index('Sentiment', inplace=True)

# Display the DataFrame
print(result_df)

# Example usage
keyword = "bg"
search_result = search_by_keyword(result_df, keyword)

# Display the search results
print(search_result)


# Example usage
# Save the DataFrame
save_dataframe(result_df, 'result.csv')

# Load the DataFrame
loaded_df = load_dataframe('result.csv')

# Display the loaded DataFrame
print(loaded_df)


# Example usage
keyword = "bg"
search_result = search_by_keyword(result_df, keyword)

# Display the search results
print(search_result)