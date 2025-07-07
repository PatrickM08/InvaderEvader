import sqlite3


class Database:
	def __init__(self):
		self.conn = sqlite3.connect("playerdatabase.db")
		self.cursor = self.conn.cursor()

	def binary_search(self,elements,target):
		left = 0
		right = len(elements) - 1
		
		if left <= right:
			middle = (left + right) // 2
			
			if elements[middle][0] == target:
				return True
			if elements[middle][0] < target:
				return self.binary_search(elements[middle + 1:],target)
			if elements[middle][0] > target:
				return self.binary_search(elements[:middle],target)
		
		return False

	# a merge sort algorithm, that is comprised of two methods, merge_sort and merge.
	# in the merge sort method we complete the first step of the algorithm,
	# we continuously split the array into two halves using recursion until each subsequent array only consists of one item.
	def merge_sort(self,array):
		# if the length of the array is one we cannot split it up anymore and it is sorted so we return it.
		# if the length is zero we cannot perform a merge sort so we return it.
		if len(array) == 1 or len(array) == 0:
			return array
		# split the array into two halves.
		middle = len(array)//2
		# stores the left arrays that are going to merged.
		left_array = self.merge_sort(array[:middle])
		# stores the right arrays that are going to be merged.
		right_array = self.merge_sort(array[middle:])
		# returns the sorted left hand arrays to left_array, the sorted right hand arrays to right_array, 
		# and eventually the entire sorted array back to where the method was orinally called.
		return self.merge(left_array,right_array)
	
	# in the merge method the two halves passed into the method are merged into an array that is sorted.
	def merge(self,left,right):
		# create a new list to store the array created by merging the two halves passed in.
		merged_array = []
		# two counters to keep track of whether all the items from the two halves have been merged into the new array.
		left_counter = 0
		right_counter = 0
		# we compare the items in each list until either of the lists have no more items to compare.
		while len(left) > left_counter and len(right) > right_counter:
			# if the left item is greater then we append it to the new array and increment the left counter.
			if left[left_counter][1] > right[right_counter][1]:
				merged_array.append(left[left_counter])
				left_counter += 1
			# if the right item is greater then we append it to the new array and increment the right counter.
			else:
				merged_array.append(right[right_counter])
				right_counter += 1
		# This last while loop is used to append any remaining items to the new array.
		# These items are at the end of the arrays meaning they must be the lowest numbers, therefore we do not have
		# to make any comparisons.
		# there are going to be items remaining in only one of the halves.
		while left_counter < len(left) or right_counter < len(right):
			# we try to append the next item in the left half to the merged array.
			try:
				merged_array.append(left[left_counter])
				left_counter += 1
			# if we get an index error we then know that the items remaining are in the right half instead.
			except IndexError:
				merged_array.append(right[right_counter])
				right_counter += 1
		# we return the new merged array.
		return merged_array


class LoginDatabase(Database):
	def __init__(self):
		super().__init__()
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS logins (
							username text,
							password text,
							userid integer PRIMARY KEY
							)""")
		self.conn.commit()

	def register(self,username,password):
		self.cursor.execute("SELECT max(userid) FROM logins")
		self.last_user_id = self.cursor.fetchone()
		# If there are no other users, userID is set to 1.
		try:
			self.last_user_id = self.last_user_id[0]
			self.user_id = self.last_user_id + 1
		except TypeError:
			self.user_id = 1

		# adds new login to login table
		self.cursor.execute("INSERT INTO logins VALUES (?, ?, ?)",(username,password,self.user_id))
		self.conn.commit()
		
	def login(self,username,password):
		self.cursor.execute("SELECT * FROM logins")
		self.login_table = self.cursor.fetchall()
		for i in range(len(self.login_table)):
			if self.login_table[i][0] == username and self.login_table[i][1] == password:
				return "correct"
		return "incorrect"

	# finds if username has been taken, using a binary search.
	def username_available(self,username_entered):
		self.cursor.execute("SELECT username FROM logins ORDER BY username")
		self.taken_usernames = self.cursor.fetchall()
		return not(self.binary_search(self.taken_usernames,username_entered))


class LeaderboardDatabase(Database):
	def __init__(self):
		super().__init__()
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS leaderboard (
			username text,
			score integer
			)""")
		self.conn.commit()

	# inserts scores into the table when called.
	def insert_scores(self, username, score):
		self.cursor.execute("INSERT INTO leaderboard VALUES (?,?)",(username,score))
		self.conn.commit()

	# retrieves the table when called.
	def retrieve_table(self):
		self.cursor.execute("SELECT * FROM leaderboard")
		self.leaderboard = self.merge_sort(self.cursor.fetchall())
		return(self.leaderboard[:5])

