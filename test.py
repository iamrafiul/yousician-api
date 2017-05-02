import unittest
from flask import json, jsonify
from app import app


class YousicianAPITestCase(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		self.app = app.test_client()

	def test_songs_content_and_pagination(self):
		# Song Content checking
		rv = self.app.get('/songs')
		result = json.loads(rv.data)
		self.assertTrue('artist' in result[0])
		self.assertTrue('title' in result[0])
		self.assertTrue('difficulty' in result[0])
		self.assertTrue('level' in result[0])
		self.assertTrue('released' in result[0])

		# Pagination Checking
		rv = self.app.get('/songs?page=1&limit=3')
		result = json.loads(rv.data)
		self.assertEqual(len(result), 3)

		rv = self.app.get('/songs?page=1&limit=5')
		result = json.loads(rv.data)
		self.assertEqual(len(result), 5)

		rv = self.app.get('/songs?page=1&limit=15')
		result = json.loads(rv.data)
		self.assertEqual(len(result), 11)

		rv = self.app.get('/songs?page=3&limit=3')
		result = json.loads(rv.data)
		self.assertEqual(len(result), 3)

		rv = self.app.get('/songs?page=3&limit=5')
		result = json.loads(rv.data)
		self.assertEqual(len(result), 1)

		# Checking if two pages have common data with same limit
		rv_1 = self.app.get('/songs?page=1&limit=2')
		rv_2 = self.app.get('/songs?page=2&limit=2')
		result_1 = json.loads(rv_1.data)
		result_2 = json.loads(rv_2.data)
		self.assertNotIn(result_1[0], result_2)
		self.assertNotIn(result_1[1], result_2)

	def test_songs_average_difficulty(self):
		rv = self.app.get('songs/avg/difficulty')
		result = json.loads(rv.data)
		self.assertTrue('average_difficulty' in result)

		rv = self.app.get('songs/avg/difficulty/13')
		result = json.loads(rv.data)
		self.assertTrue('average_difficulty' in result)

		rv = self.app.get('songs/avg/difficulty/9')
		result = json.loads(rv.data)
		self.assertTrue('average_difficulty' in result)

		rv = self.app.get('songs/avg/difficulty/20')
		result = json.loads(rv.data)
		self.assertTrue('error' in result)

		rv = self.app.get('songs/avg/difficulty/100')
		result = json.loads(rv.data)
		self.assertTrue('error' in result)

	def test_songs_search(self):
		rv = self.app.get('/songs/search/Viv')
		result = json.loads(rv.data)
		self.assertTrue('artist' in result[0])
		self.assertTrue('title' in result[0])
		self.assertTrue('difficulty' in result[0])
		self.assertTrue('level' in result[0])
		self.assertTrue('released' in result[0])

		rv = self.app.get('/songs/search/viv')
		result = json.loads(rv.data)
		self.assertTrue('artist' in result[0])
		self.assertTrue('title' in result[0])
		self.assertTrue('difficulty' in result[0])
		self.assertTrue('level' in result[0])
		self.assertTrue('released' in result[0])

		rv = self.app.get('/songs/search/Viv')
		result = json.loads(rv.data)
		self.assertTrue('artist' in result[0])
		self.assertTrue('title' in result[0])
		self.assertTrue('difficulty' in result[0])
		self.assertTrue('level' in result[0])
		self.assertTrue('released' in result[0])

		rv = self.app.get('/songs/search/bot')
		result = json.loads(rv.data)
		self.assertTrue('error' in result)

	def test_songs_rating(self):
		rv = self.app.post(
			'/songs/rating',
			data=json.dumps(
				dict(
					song_id='5905b02a11c820f8c66978ca',
					rating='4.5'
				)),
				content_type='application/json'
			)
		result = json.loads(rv.data)
		self.assertTrue('result' in result)
		
		rv = self.app.post(
			'/songs/rating',
			data=json.dumps(
				dict(
					song_id='5905b02a11c820f8c66978ca',
					rating='7'
				)),
				content_type='application/json'
			)
		result = json.loads(rv.data)
		self.assertTrue('error' in result)

	'''
		This test is commented out as I have tested it inserting extra data in the database.
	'''
	# def test_songs_average_rating(self):
	# 	rv = self.app.get('songs/avg/rating/5905b02a11c820f8c66978ca')
	# 	result = json.loads(rv.data)
	# 	self.assertTrue('average' in result)
	# 	self.assertTrue('highest' in result)
	# 	self.assertTrue('lowest' in result)



if __name__ == '__main__':
	unittest.main()









