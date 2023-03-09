import csv
import os
import pymongo
from dotenv import load_dotenv
from notion.client import NotionClient

load_dotenv()

try:
    dbURL = os.environ['MONGO_DB']
    notion_token = os.environ['NOTION_API_KEY   ']
except:
    load_dotenv()
    dbURL = os.getenv('MONGO_DB')
    notion_token = os.getenv('NOTION_API_KEY')

myclient = pymongo.MongoClient(dbURL)
prod_db = myclient["Twitter"]
myDB = myclient["Twitter"]
db_scraped_tweets = myDB["scraped_tweets"]
db_generated_tweets = myDB["generated_tweets"]



# ALl functions for interacting with the database
# ----------------------------------------------------------------------#
# Function to write to database
# Inputs: db - the database to write to
#         query - the query to write to the database
# Outputs: None
def write_to_db(db, query):
    myDB[db].insert_one(query)

# Funtion to remove from database
# Inputs: dict - dictionary of tweet attributes
# Outputs: None
def remove_from_db(db, query):
    myDB[db].delete_one(query)

def remove_all_from_db(db):
    myDB[db].delete_many({})

# Function to read from database
# Inputs: None
# Outputs: db_data - array of data in dict form
def read_from_db(db):
    db_data = []
    for x in myDB[db].find():
        db_data.append(x)
    return db_data

# Function to find a document in the database
# Inputs: query - the query to search for
# Outputs: document - the document that matches the query
def find_document(db, query):
    document = myDB[db].find_one(query)
    return document

# Function to find all documents in the database
# Inputs: query - the query to search for
# Outputs: count - the number of documents that match the query
def find_all_documents(db, query):
    documents = []
    for data in list(myDB[db].find(query)):
        # Find the 'text' attribute in the document
        documents.append(data['text'])
    count = len(list(myDB[db].find(query)))
    return count, documents

# Function to find all documents in the database
# Inputs: query - the query to search for
# Outputs: none
def delete_all_documents(db, query):
    count = len(list(myDB[db].find(query)))
    myDB[db].delete_many(query)
    return count

def update_document(db, query, new_values):
    myDB[db].update_one(query, new_values)


# ----------------------------------------------------------------------#


# Functions for interacting with notion.so
# ----------------------------------------------------------------------#
# Function for adding an idea to notion
# Inputs: name - the name of the project it relates too
#         idea - the idea
#         status - the status of the idea
# Outputs: None
def add_to_notion(name, idea, status, message):
    client = NotionClient(token_v2=notion_token)

    db = client.get_collection_view('https://www.notion.so/f976fa217e324095b3f2b52743780a0c?v=6dfa2826b6974a3882f8a34d5b9507da')

    row = db.collection.add_row()
    row.name = name
    row.idea = idea
    row.status = status
    row.message = message



# Function to find all the other users that our bot follows, then add any new ones to the DB.
# Uses those users to output a list of users to scrape
# input: List of users from twitter
# output: list of users to scrape
def find_users_to_scrape(list_of_follows):
    # Get the list of users from the DB
    list_of_users = []
    for all_users in read_from_db('users'):
        list_of_users.append(all_users['user'])
    # Check if the user is in the DB
    for follows in list_of_follows:
        if follows not in list_of_users:
            # Add the user to the DB
            write_to_db('users', {'user': follows})
            # Add the user to the list of users to scrape
            list_of_users.append(follows)
    # Return the list of users to scrape
    return list_of_users

# Function to open the csv file
# Inputs:  csv_name - the name of the csv file
# Outputs: list_of_tweets_ - a list of tweets
def open_csv(csv_name):
    # If is not empty
    if os.stat(csv_name).st_size != 0:
        # Open the csv file
        with open(csv_name, 'r', encoding = 'utf-8') as file:
            # Create a list of tweets
            returned_array = []
            # Create a csv reader
            reader = csv.reader(file)
            # Skip the header
            next(reader)
            # For each row in the csv file
            for row in reader:
                # Add the row to the list of tweets
                returned_array.append(row)
        return returned_array
    else:
        return []

# Function to write to the csv file
# Inputs:  csv_name - the name of the csv file
#          list_of_tweets_ - a list of tweets
def write_csv(csv_name, list_of_tweets_):
    # Open the csv file
    with open(csv_name, 'w', encoding = 'utf-8') as file:
        # Create a csv writer
        writer = csv.writer(file)
        # Write the header
        # writer.writerow(headings)
        # For each tweet in the list of tweets
        for tweet in list_of_tweets_:
            tweet_in_row_form = []
            tweet_in_row_form.clear()
            # Write the tweet to the csv file
            for attribute in vars(tweet):
                tweet_in_row_form.append(getattr(tweet, attribute))
            if len(tweet_in_row_form) != 0:
                writer.writerow(tweet_in_row_form)


