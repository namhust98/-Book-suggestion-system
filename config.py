"""
config.py

File cau hinh
"""

# Duong dan toi tap du lieu cho load_data.py
BOOKS_FILE = './Data/books.csv'
RATINGS_FILE = './Data/ratings.csv'

# LSH parameters
BLOCK_SIZE = 3  # ~ r
NUM_BLOCKS = 500 # ~ p
NUM_HASH_FUNCTIONS = 1500 # ~ K = r*p
NUM_NEAREST_NEIGHBORS = 5 # ~ nn
nextPrime = 53437
maxID = 53423
