import requests
from hashlib import md5
from base64 import b64encode
from datetime import datetime

class LvlUpLife:
	def __init__(self) -> None:
		self.first_api = "https://lvluplife.com"
		self.second_api = "https://api1.lvluplife.com"
		self.headers = {
			"user-agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G9880 Build/RP1A.2007201.01"
		}
		self.user_id = None
		self.login_key = None

	def md5_hash(self, string: str) -> str:
		return md5(string.encode()).hexdigest()

	def register(
			self,
			username: str,
			password: str) -> dict:
		data = {
			"signup_username": username,
			"signup_pass_encrypted": self.md5_hash(password),
			"signup_type": "REG"
		}
		return requests.post(
			f"{self.first_api}/app/v5/b_signup.php",
			data=data,
			headers=self.headers).json()

	def login(
			self,
			username: str,
			password: str) -> dict:
		data = {
			"username": username,
			"password": password
		}
		response = requests.post(
			f"{self.second_api}/app/v5/a_login.php",
			data=data,
			headers=self.headers).json()
		if "loggedinid" in response["login"][0]:
			self.user_id = response["login"][0]["loggedinid"]
			self.login_key = response["login"][0]["loginkey"]
		return response

	def view_community(self) -> dict:
		return requests.get(
			f"{self.first_api}/app/v5/a_activity_2018.php?whoview=community&loggedinid={self.user_id}",
			headers=self.headers).json()

	def get_comments(self, task_id: int) -> dict:
		return requests.get(
			f"{self.first_api}/app/v5/a_comments_2018.php?loggedinid={self.user_id}&taskid={task_id}",
			headers=self.headers).json()

	def add_comment(
			self,
			user_id: int,
			task_id: int,
			comment: str) -> dict:
		data = {
			"whostask": user_id,
			"loggedinid": self.user_id,
			"usertaskid": task_id,
			"comment": comment,
			"loginkey": self.login_key
		}
		return requests.post(
			f"{self.first_api}/app/v3/b_addcomment.php",
			data=data,
			headers=self.headers).json()

	def get_profile_info(self, username: str) -> dict:
		return requests.get(
			f"{self.first_api}/app/v5/a_profileinfo_2018.php?loggedinid={self.user_id}&profiler={username}",
			headers=self.headers).json()

	def report_user(
			self,
			user_id: int,
			comment: str,
			reason: int = 1) -> dict:
		data = {
			"loggedinid": self.user_id,
			"whobad": user_id,
			"reason": reason,
			"comments": comment
		}
		return requests.post(
			f"{self.first_api}/app/v5/b_reportuser.php",
			data=data,
			headers=self.headers).json()

	def add_friend(self, user_id: int) -> dict:
		data = {
			"loggedinid": self.user_id,
			"dowhat": "addfriend",
			"friend": user_id,
			"loginkey": self.login_key
		}
		return requests.post(
			f"{self.first_api}/app/v3/b_friendaction.php",
			data=data,
			headers=self.headers).json()

	def remove_friend(self, user_id: int) -> dict:
		data = {
			"loggedinid": self.user_id,
			"dowhat": "removefriend",
			"friend": user_id,
			"loginkey": self.login_key
		}
		return requests.post(
			f"{self.first_api}/app/v3/b_friendaction.php",
			data=data,
			headers=self.headers).json()

	def get_user_activity(self, username: str) -> dict:
		return requests.get(
			f"{self.first_api}/app/v5/a_activity_2018.php?whoview=me&loggedinid={self.user_id}&profiler={username}",
			headers=self.headers).json()

	def get_friends(self) -> dict:
		return requests.get(
			f"{self.second_api}/app/v5/a_friends.php?loggedinid={self.user_id}",
			headers=self.headers).json()

	def search_friend(self, username: str) -> dict:
		return requests.get(
			f"{self.second_api}/app/v5/a_friends.php?loggedinid={self.user_id}&friendsearch={username}",
			headers=self.headers).json()

	def get_high_scores(self) -> dict:
		return requests.get(
			f"{self.first_api}/app/v5/a_highscores_2018.php?loggedinid={self.user_id}",
			headers=self.headers).json()

	def set_goal(self, task_number: int, remove: str = "no") -> dict:
		data = {
			"loggedinid": self.user_id,
			"remove": remove,
			"tasknum": task_number,
			"loginkey": self.login_key
		}
		return requests.post(
			f"{self.first_api}/app/v3/b_goalset.php",
			data=data,
			headers=self.headers).json()

	def create_new_task(
			self,
			description: str,
			task_number: int,
			gained_xp: int,
			cha: int,
			str: int,
			cul: int,
			int: int,
			env: int,
			tal: int,
			rotatedegrees: int = 0,
			vnum: int = 67) -> dict:
		data = {
			"CHA": cha,
			"STR": str,
			"editornew": "new",
			"tasknum": task_number,
			"gainedxp": gained_xp,
			"rotatedegrees": rotatedegrees,
			"loginkey": self.login_key,
			"vnum": vnum,
			"when_edited": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
			"datetime": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
			"CUL": cul,
			"INT": int,
			"loggedinid": self.user_id,
			"newdesc": description,
			"ENV": env,
			"TAL": tal
		}
		return requests.post(
			f"{self.first_api}/app/v5/b_taskeditornew.php",
			data=data,
			headers=self.headers).json()

	def delete_task(self, task_id: int) -> dict:
		data = {
			"usertaskid": task_id,
			"loggedinid": self.user_id,
			"when_deleted": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
			"loginkey": self.login_key
		}
		return requests.post(
			f"{self.first_api}/app/v5/b_deletetask.php",
			data=data,
			headers=self.headers).json()

	def change_profile_image(self, image: str) -> dict:
		data = {
			"loggedinid": self.user_id,
			"loginkey": self.login_key,
			"image": b64encode(open(image, "rb").read()).strip().decode()
		}
		return requests.post(
			f"{self.first_api}/app/v3/b_profilepic.php",
			data=data,
			headers=self.headers).json()

	def get_notifications(self) -> dict:
		return requests.get(
			f"{self.first_api}/app/v5/a_notifications_2018.php?loggedinid={self.user_id}",
			headers=self.headers).json()

	def change_email(self, email: str) -> dict:
		data = {
			"loggedinid": self.user_id,
			"val": email,
			"key": "pref_emailset",
			"loginkey": self.login_key
		}
		return requests.post(
			f"{self.first_api}/app/v5/b_settingchange.php",
			data=data,
			headers=self.headers).json()

	def reset_password(self, username: str) -> dict:
		return requests.get(
			f"{self.first_api}/app/v5/b_passreset.php?logininfo={username}",
			headers=self.headers).json()
