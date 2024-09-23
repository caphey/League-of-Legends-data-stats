from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGODB_URI)
db = client['api-project']
collection = db['riot']


def save_user_data(user_data):
    user_data_for_update = user_data.copy()
    user_data_for_update.pop('_id', None)
    return collection.find_one_and_update(
        {'game_name': user_data['game_name'],
            'tag_line': user_data['tag_line']},
        {'$set': user_data_for_update},
        upsert=True,
        return_document=True
    )


def get_user_data(game_name, tag_line):
    return collection.find_one({'game_name': game_name, 'tag_line': tag_line})
