import requests
import sqlite3
import json
import random

database = './urbanDictionary/words.db'


def create_table():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS words (word text)")
    conn.commit()
    conn.close()


def get_random_word():
    url = "https://api.urbandictionary.com/v0/random"
    response = requests.get(url)
    data = response.json()
    word = data['list'][0]['word']
    return word

# add the word to local SQLite database words.db


def add_word_to_db(word):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("INSERT INTO words VALUES (?)", (word,))
    conn.commit()
    conn.close()

# check if the word is already in the database


def check_word_in_db(word):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("SELECT * FROM words WHERE word = ?", (word,))
    result = c.fetchone()
    conn.close()
    return result

# get random word from the API and add the word to local SQLite database words.db


def get_random_word_from_api():
    word = get_random_word()
    result = check_word_in_db(word)
    if result is None:
        add_word_to_db(word)
        return word
    else:
        get_random_word_from_api()


def get_definition(word):
    url = "https://api.urbandictionary.com/v0/define?term=" + word
    response = requests.get(url)
    data = response.json()
    return data


def getData():
    create_table()
    return get_definition(get_random_word_from_api())


# on run get_random_word_from_api and print the word
if __name__ == '__main__':
    create_table()
    word = get_random_word_from_api()
    print(word)
