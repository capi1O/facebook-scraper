#!/usr/bin/env python

from facepy import GraphAPI, OAuthError
import json
import getopt, sys
import os
import webview
import threading
import Queue
import time
import urlparse
import pickle
import robobrowser

redirect_url = "https://your-website.com/path/to/facebook-login.html"
fb_app_id = "xxxxxxxxxxxxxxx"
window_closed = True

def parse_arguments(sys_args):
	try:
		opts, non_opts_args = getopt.gnu_getopt(sys_args, "hj:c:o:v", ["help", "json=", "csv=", "output=", "verbose"])
		input_file = False
		input_type = ""
		input_data = ""
		output_type = "stdin"
		verbose = False
		for option, arg in opts:
			if option in ("-h", "--help"):
				print "help needed"
			elif option in ("-j", "--json"):
				print "JSON file provided"
				input_file = True
				input_type = "json"
				input_data = arg
			elif option in ("-c", "--csv"):
				print "CSV file provided"
				input_file = True
				input_type = "csv"
				input_data = arg
			elif option in ("-o", "--output"):
				output_type = arg
			elif option in ("-v", "--verbose"):
				verbose = True
			else:
				assert False, "unhandled option : " + option
		# if no JSON or CSV options provided, get non-option arguments if provided (names)
		if input_file == False:
			print "no input file provided, reading all non-option arguments as strings : '" + ", ".join(map(str, non_opts_args)) + "'"
			input_type = "strings"
			input_data = non_opts_args
		return [input_type, input_data, output_type, verbose]
	except getopt.GetoptError as err:
		print(err)
		usage()
		sys.exit(2)

def get_input_names(input_type, input_data = []):
	input_names=[]
	if input_type == "strings":
		input_names = input_data
	elif input_type == "json":
		# json_file_path = os.getcwd() + '/' + input_data
		# print json_file_path
		with open(input_data) as json_data:
			people_json = json.load(json_data)
		for person in people_json:
			input_names.append(person['name'])
	elif input_type == "csv":
		#TODO : loads CSV file
		pass
	else:
		assert False, "unhandled input type : " + input_type
	return input_names

def get_fb_token():
	global window_closed
	# Check if user token from previous session
	token_file = 'user_token.pk'
	if os.path.exists(token_file):
		with open(token_file, 'rb') as fi:
			try:
				saved_fb_user_token = pickle.load(fi)
				return saved_fb_user_token
			except EOFError:
				print "No saved Facebook user token in file : ", fi

	# Launch a thread which will wait for the Facebook user token
	window_closed = False
	wait_fb_token_queue = Queue.Queue()
	wait_fb_token_thread = threading.Thread(target=wait_for_fb_token, args=[wait_fb_token_queue])
	wait_fb_token_thread.start()
	# Ask user for new token and wait for authorization success
	auth_url = "https://www.facebook.com/dialog/oauth?response_type=token&client_id=" + fb_app_id + "&redirect_uri=" + redirect_url
	webview.create_window("Authorization request", auth_url) # block until window is closed
	print "window was closed"
	window_closed = True
	# Get result from wait_fb_token_thread
	wait_fb_token_thread.join()
	return wait_fb_token_queue.get()

def wait_for_fb_token(output_queue):
	authorization_success = wait_until(lambda : webview.get_current_url().startswith(redirect_url), lambda : window_closed is True, 10)

	if authorization_success is None:
		print "Error : window closed before authorization for Facebook Graph API"
		output_queue.put(None)
	else:
		if authorization_success:
			url = webview.get_current_url()
			# ex : https://your-website.com/path/to/facebook-login.html?#access_token=access-token-here&expires_in=5558
			parsed = urlparse.parse_qs(urlparse.urlparse(url).fragment)
			try:
				user_token = parsed['access_token'][0]
				if user_token:
					# Save user token for future sessions
					token_file = 'user_token.pk'
					with open(token_file, 'wb+') as fi:
						pickle.dump(user_token, fi)
					output_queue.put(user_token)
				else:
					print "Error : could not get user token for Facebook Graph API"
					output_queue.put(None)
			except KeyError:
				print "Error : could not get user token for Facebook Graph API"
				output_queue.put(None)
		else:
			print "Error : could not get authorization for Facebook Graph API"
			output_queue.put(None)
		# Close the window
		webview.destroy_window()
		if sys.platform == 'darwin':
			from util_cocoa import mouseMoveRelative
			mouseMoveRelative(1, 1)

def wait_until(success_condition, stop_condition, timeout, period=0.25):
	mustend = time.time() + timeout
	while time.time() < mustend and not stop_condition():
		if success_condition():
			return True
		time.sleep(period)
	if stop_condition():
		return None
	else:
		return False
	
def fb_token_valid(fb_user_token):
	if fb_user_token and fb_user_token is not None:
		# Init facepy graph API
		graph = GraphAPI(fb_user_token)
		# Make dummy request
		try:
			result = graph.get('me')
			return True
		except OAuthError as err:
			print "Error : invalid user token for Facebook Graph API : ", err
			return False
	else:
		print "Error : no user token for Facebook Graph API"
		return False


def get_fb_users(fb_user_token, verbose, names=[]):
	# Init facepy graph API
	graph = GraphAPI(fb_user_token)
	facebook_users = []
	# Get Facebook users matching name(s) provided
	for name in names:
		encoded_name = name.encode('utf8')
		print encoded_name
		try:
			fields = "name,link,picture"
			if verbose:
				fields += ",birthday,email,work,hometown"
			result_pages = graph.get('search?q={' + encoded_name + '}&type=user&fields=' + fields, True)
			result_data = []
			for result_page in result_pages:
				result_data += result_page["data"]
			facebook_users.append(result_data)
		except OAuthError as err:
			print(err)
			print "invalid token for request of user " + name + ", error : ", err
	return facebook_users[0]
	
def fb_logged_browser(fb_email, fb_password):
	url = 'https://m.facebook.com'
	browser = robobrowser.RoboBrowser()
	browser.open(url)
	login_form = browser.get_form(id='login_form')
	login_form['email'] = fb_email
	login_form['pass'] = fb_password
	browser.submit_form(login_form)
	return browser

def get_fb_uid(fb_user_data, browser):
	# 1. Try to follow link (need to be logged in)
	fb_user_profile_url = fb_user_data["link"]
	response = browser.session.get(fb_user_profile_url, stream=True)
	# 2. Check if link could be followed
	if "app_scoped_user_id" in response.url:
		print "Reached Graph API request limit"
		return None
	# 3. Check if final URL is Customized Profile URL (https://www.facebook.com/custom.user.name) or Non-customized Profile URL (https://www.facebook.com/profile.php?id=xxxxxxxxxxxxxxx)
	# Non-customized Profile URL, must parse the webpage
	if "profile.php?id=" in response.url:
		parsed = urlparse.parse_qs(urlparse.urlparse(response.url).query)
		try:
			fb_uid = parsed['id'][0]
			return fb_uid
		except KeyError:
			print "Error : could not get UID from non-customized Profile URL"
			return None
	# Customized Profile URL, must parse the webpage
	else:
		# TODO : Analyse browser.parsed
		return None

def add_field_to_users(fb_users, key, lambda_value):
	updated_fb_users = []
	for fb_user_data in fb_users:
		fb_uid = lambda_value(fb_user_data)
		if fb_uid and fb_uid is not None:
			fb_uid_dict = {key: fb_uid}
			fb_user_data.update(fb_uid_dict)
			updated_fb_users.append(fb_user_data)
	return updated_fb_users

def output_result(output_type, facebook_users):
	if output_type == "stdin":
		print json.dumps(facebook_users, indent=4, sort_keys=True, ensure_ascii=False, encoding="utf-8")
	elif output_type == "json":
		# json_file_path = os.getcwd() + '/' + "output.json"
		# print json_file_path
		with open("output.json", 'w+') as output_file:
			json.dump(facebook_users, output_file)
	elif output_type == "csv":
		#TODO : write to CSV file
		pass
	else:
		assert False, "unhandled output type : " + output_type

if __name__ == '__main__':

	# 0. Parse Arguments
	inputType, inputData, outputType, verbose = parse_arguments(sys.argv[1:])
		
	# 1. Get input names (strings, JSON file or csv file)
	inputNames = get_input_names(inputType, inputData)
	
	# 2 . Get authorization from user to Facebook Graph API
	fbUserToken = get_fb_token()
	
	# 3 . Test Facebook User token
	if not fb_token_valid(fbUserToken):
		print "Access Denied - Invalid token, try again"
		# Remove saved token if any
		try:
			os.remove('user_token.pk')
		except OSError:
			pass
		sys.exit(2)
	
	# 4 . Scrap matching facebook users
	fbUsers = get_fb_users(fbUserToken, verbose, inputNames)
	
	# 5. Get the FB id for each user by following the link from Graph API in a logged browser
	fbLoggedBrowser = fb_logged_browser("your.email@example.com", "xxxxxxxx")
	fbUsers = add_field_to_users(fbUsers, "fb_uid", lambda user : get_fb_uid(user, fbLoggedBrowser))
	
	# 6 . Output result in desired format
	output_result(outputType, fbUsers)





