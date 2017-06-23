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

redirect_url = "https://your-website.com/path/to/facebook-login.html"
fb_app_id = "xxxxxxxxxxxxxxx"

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
	wait_fb_token_queue = Queue.Queue()
	wait_fb_token_thread = threading.Thread(target=wait_for_fb_token, args=[wait_fb_token_queue])
	wait_fb_token_thread.start()
	# Ask user for new token and wait for authorization success
	auth_url = "https://www.facebook.com/dialog/oauth?response_type=token&client_id=" + fb_app_id + "&redirect_uri=" + redirect_url
	webview.create_window("Authorization request", auth_url)
	# Wait for thread to return the token
	wait_fb_token_thread.join()
	return wait_fb_token_queue.get()

def wait_for_fb_token(output_queue):
	authorization_success = wait_until(lambda : webview.get_current_url().startswith(redirect_url), 10)
	url = webview.get_current_url()
	webview.destroy_window()
	if sys.platform == 'darwin':
		from util_cocoa import mouseMoveRelative
		mouseMoveRelative(1, 1)
	if authorization_success:
		# ex : https://your-website.com/path/to/facebook-login.html?#access_token=access-token-here&expires_in=5558
		parsed = urlparse.parse_qs(urlparse.urlparse(url).fragment)
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
	else:
		print "Error : could not get authorization for Facebook Graph API"
		output_queue.put(None)

def wait_until(condition, timeout, period=0.25):
	mustend = time.time() + timeout
	while time.time() < mustend:
		if condition():
			return True
		time.sleep(period)
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
	return facebook_users

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
	
	# 5 . Output result in desired format
	output_result(outputType, fbUsers)





