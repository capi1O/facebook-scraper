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
		opts, args = getopt.getopt(sys_args, "hjc:v", ["help", "json=", "csv="])
	except getopt.GetoptError as err:
		print(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	input_file = False
	input_type = ""
	input_data = ""
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
		elif option == "-v":
			verbose = True
		else:
			assert False, "unhandled option"
	# if no JSON or CSV options provided, get non-option arguments if provided (names)
	if input_file == False:
		print "no file provided, reading all non-option arguments as strings"
		input_type = "strings"
		input_data = args
	return [input_type, input_data]

def get_input_names(input_type, input_data):
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
	while not webview.get_current_url().startswith(redirect_url):
		time.sleep(1)
	url = webview.get_current_url()
	# ex : https://your-website.com/path/to/facebook-login.html?#access_token=access-token-here&expires_in=5558
	parsed = urlparse.parse_qs(urlparse.urlparse(url).fragment)
	user_token = parsed['access_token'][0]
	# TODO : use try
	if user_token:
		# Close the window 
		webview.destroy_window()
		# Save user token for future sessions
		token_file = 'user_token.pk'
		with open(token_file, 'wb+') as fi:
			pickle.dump(user_token, fi)
		output_queue.put(user_token)
	else:
		print "Error : could not get user token for Facebook Graph API"

def test_fb_token(fb_user_token):
	# Init facepy graph API
	graph = GraphAPI(fb_user_token)
	# Make dummy request
	try:
		result = graph.get('me')
		return True
	except OAuthError as err:
		print "invalid token : ", err
		return False

def get_fb_users(fb_user_token, names=[]):
	# Init facepy graph API
	graph = GraphAPI(fb_user_token)
	# Get Facebook users matching name(s) provided
	for name in names:
		encoded_name = name.encode('utf8')
		print encoded_name
		try:
			result = graph.get('search?q={' + encoded_name + '}&type=user')
			data = result['data'] #decode('utf8')
			return data
		except OAuthError as err:
			print(err)
			print "invalid token, after test : ", err
			return None

if __name__ == '__main__':

	# 0. Parse Arguments
	inputType, inputData = parse_arguments(sys.argv[1:])
		
	# 1. Get input names (strings, JSON file or csv file)
	inputNames = get_input_names(inputType, inputData)
	
	# 2 . Get authorization from user to Facebook Graph API
	fbUserToken = get_fb_token()
	
	# 3 . Test Facebook User token
	if not test_fb_token(fbUserToken):
		print "Access Denied - Invalid token, try again"
		# Remove saved token
		os.remove('user_token.pk')
		sys.exit(2)
		
	# 4 . Scrap matching facebook users
	fbUsers = get_fb_users(fbUserToken, inputNames)
	
	# 5 . Output result in desired format
	print json.dumps(fbUsers, indent=4, sort_keys=True, ensure_ascii=False, encoding="utf-8")





