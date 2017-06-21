#!/usr/bin/env python

from facepy import GraphAPI
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
		
def get_input_names(options, arguments):
	input_names=[]
	input_file = False
	verbose = False
	for option, arg in options:
		if option in ("-h", "--help"):
			print "help needed"
		elif option in ("-j", "--json"):
			print "JSON file provided"
			input_file = True
			# json_file_path = os.getcwd() + '/' + arg
			# print json_file_path
			with open(arg) as json_data:
				people_json = json.load(json_data)
			for person in people_json:
				input_names.append(person['name'])
		elif option in ("-c", "--csv"):
			print "CSV file provided"
			input_file = True
		    #TODO : loads CSV file 
		elif option == "-v":
			verbose = True
		else:
			assert False, "unhandled option"
	# if no JSON or CSV options provided, get non-option arguments if provided (names)
	if input_file == False:
		print "no file provided, reading non-option arguments as names"
		input_names=arguments
	return input_names

# Get Facebook user access token (using Facebook app)
def get_fb_token():
	# Check if user token from previous session
	token_file = 'user_token.pk'
	if os.path.exists(token_file):
		with open(token_file, 'rb') as fi:
			try:
				saved_user_token = pickle.load(fi)
				print saved_user_token
				#TODO : check if it is still valid.
				return saved_user_token
			except EOFError:
				print "No saved user token in file : ", fi
	
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
	
def get_fb_users(fb_graph_api_user_token, names=[]):
	# Init facepy graph API
	graph = GraphAPI(fb_graph_api_user_token)
	# Get Facebook users matching name(s) provided
	for name in names:
		encoded_name = name.encode('utf8')
		print encoded_name
		result = graph.get('search?q={' + encoded_name + '}&type=user')
		data = result['data'] #decode('utf8')
		print json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False, encoding="utf-8")

if __name__ == '__main__':
	
	# 0. Get input data (name, JSON file or csv file)
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hjc:v", ["help", "json=", "csv="])
	except getopt.GetoptError as err:
		print(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
		
	# 1 . Get input names
	input_names = get_input_names(opts, args)
	
	# 2 . Get authorization from user to Facebook Graph API
	fb_user_token=get_fb_token()
	
	# 3 . Scrap matching facebook users
	get_fb_users(fb_user_token, input_names)