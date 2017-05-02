from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

#  Configuration for Database 
app.config["MONGO_DBNAME"] = "yousician_db"
app.config['MONGO_URI'] = 'mongodb://yousician:asd123@localhost:27017/yousician_db'

mongo = PyMongo(app)

@app.route('/songs', methods=['GET'])
def get_songs():
	page = request.args.get('page')
	limit = request.args.get('limit')

	songs = mongo.db.songs
	result = []

	if page is not None and page.isdigit() and limit is not None and limit.isdigit():
		limit = int(limit)
		skip = (int(page) - 1) * limit

		song_list = songs.find().skip(skip).limit(limit)

	else:
		song_list = songs.find() 
	
	for song in song_list:
		result.append({
			'artist': song['artist'],
			'title': song['title'],
			'difficulty': song['difficulty'],
			'level': song['level'],
			'released': song['released']
			})
	return jsonify(result)

@app.route('/songs/avg/difficulty', defaults={'level': None}, methods=['GET'])
@app.route('/songs/avg/difficulty/<int:level>', methods=['GET'])
def get_avg_difficulty(level):
	level_sum = 0.0
	count = 0

	if level is not None:
		song_list = mongo.db.songs.find({'level': level})
		count = song_list.count()

		for song in song_list:
			level_sum += song['difficulty']
	else:
		song_list = mongo.db.songs.find()
		count = song_list.count()

		for song in song_list:
			level_sum += song['difficulty']
		
	avg_difficulty = float(level_sum / float(count)) if count > 0 else 0

	return jsonify({'average_difficulty': avg_difficulty}) if avg_difficulty > 0 else jsonify({'error': 'No song found with this level.'})

@app.route('/songs/search/<message>', methods=['GET'])
def search_songs(message):
	song_list = mongo.db.songs.find({
			'$or': [
				{'artist': {'$regex': message, '$options': 'i'}},
				{'title': {'$regex': message, '$options': 'i'}}
			]
		})
	result = []

	for song in song_list:
		result.append({
			'artist': song['artist'],
			'title': song['title'],
			'difficulty': song['difficulty'],
			'level': song['level'],
			'released': song['released']
			})

	if len(result) >0:
		return jsonify(result)
	else:
		return jsonify({'error': 'No result found for keyword \'' + message + '\.'})

@app.route('/songs/rating', methods=['POST'])
def post_rating():
	song_id = request.json['song_id']
	rating = request.json['rating']

	if rating is None or (float(rating) < 1 or float(rating) > 5 ):
		return jsonify({'error': 'Rating should be between 1 and 5'})	

	if not ObjectId.is_valid(song_id):
		return jsonify({'error': 'Invalid song id.'})
	else:
		try:
			update_rating = mongo.db.songs.update_one(
				{'_id': ObjectId(song_id)},
				{'$push': {'rating': rating}}
			)
			print rating
			if update_rating.matched_count > 0:
				return jsonify({'result': 'Added rating successfully.'})
			else:
				return jsonify({'error': 'No Song found with the id provided.'})
		except:
			return jsonify({'error': 'Error while adding a rating for this song. Please try again.'})
		

@app.route('/songs/avg/rating/<song_id>')
def get_avg_rating(song_id):
	if not ObjectId.is_valid(song_id):
		return jsonify({'error': 'Invalid song id.'})
	else:
		song = mongo.db.songs.find_one({'_id': ObjectId(song_id)})
		
		try:
			ratings = map(float, song['rating'])
		except:
			ratings = []

		if len(ratings) > 0:
			avg = round(sum(ratings) / float(len(ratings)), 2)
			lowest = min(ratings)
			highest = max(ratings)
			return jsonify({'average': avg, 'lowest': lowest, 'highest': highest})
		else:
			return jsonify({'error': 'No rating found for this song'})
		
		

	




