#!/usr/bin/env python

import json
import getopt, sys
import os
import threading
import Queue
import time
import urlparse
import pickle
import robobrowser
from urllib import quote

def parse_arguments(sys_args):
	try:
		opts, non_opts_args = getopt.gnu_getopt(sys_args, "hj:c:o:v:e:p", ["help", "json=", "csv=", "output=", "verbose", "email=", "password="])
		
		# defaults
		input_type = ""
		output_type = "stdin"
		verbose = False
		fb_email = ""
		fb_password = ""
		
		input_file = False
		input_data = ""
		
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
			elif option in ("-e", "--email"):
				fb_email = arg
			elif option in ("-p", "--password"):
				fb_password = arg
			else:
				assert False, "unhandled option : " + option
		# if no JSON or CSV options provided, get non-option arguments if provided (names)
		if input_file == False:
			print "no input file provided, reading all non-option arguments as strings : '" + ", ".join(map(str, non_opts_args)) + "'"
			input_type = "strings"
			input_data = non_opts_args
		return [input_type, input_data, output_type, verbose, fb_email, fb_password]
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

def get_fb_cookies():
	# Check if user token from previous session
	cookies_file = 'cookies.pk'
	if os.path.exists(cookies_file):
		with open(cookies_file, 'rb') as fi:
			try:
				saved_cookies = pickle.load(fi)
				return saved_cookies
			except EOFError:
				print "No saved cookies in file : ", fi
				return None

def fb_log_browser(browser, fb_email, fb_password):
	# Load Facebook website
	url = 'https://m.facebook.com'
	browser.open(url)
	# Send credentials to login form
	login_form = browser.get_form(id='login_form')
	login_form['email'] = fb_email
	login_form['pass'] = fb_password
	browser.submit_form(login_form)
	# TODO : Check if correctly logged in
	if True:
		return True
	else:
		print "Error : could not login"
		return False

def get_fb_users(browser, names=[]):
	facebook_users = []
	# Get Facebook users matching name(s) provided
	for name in names:
		encoded_name = quote(name, safe='')
		print encoded_name
		try:
			url = 'https://m.facebook.com/search/people/?q=' + encoded_name + '&tsid&source=filter&isTrending=0'
			print url
			browser.open(url)
			root_div = browser.select('div#root')
			print browser.parsed
			# TODO : Scrap each user row
			user_divs = []
			for user_div in user_divs:
				facebook_users.append(user_div)
		except:
			print "Error while loading URL"
	return facebook_users

def get_fb_uid(fb_user_data, browser):
	# 1. Try to follow link (need to be logged in)
	fb_user_profile_url = fb_user_data["link"]
	response = browser.session.get(fb_user_profile_url, stream=True)
	# 2. Check if final URL is Customized Profile URL (https://www.facebook.com/custom.user.name) or Non-customized Profile URL (https://www.facebook.com/profile.php?id=xxxxxxxxxxxxxxx)
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
	inputType, inputData, outputType, verbose, fbEmail, fbPassword = parse_arguments(sys.argv[1:])
		
	# 1. Get input names (strings, JSON file or csv file)
	inputNames = get_input_names(inputType, inputData)
	
	fbBrowser = robobrowser.RoboBrowser()

	# 2A. Try to reuse cookies (if any) from previous session
	fbCookies = get_fb_cookies()
	if fbCookies:
		print "Cookies found, no need to log in"
		fbBrowser.session.cookies = fbCookies
		#TODO : check if valid
		logged_in = True
		if not logged_in:
			# Clear cookies, if any saved
			try:
				os.remove('cookies.pk')
			except OSError:
				pass
	# 2B . Try to login using credentials
	else:
		if fb_log_browser(fbBrowser, fbEmail, fbPassword):
			# Save cookies for future session
			fb_cookies = fbBrowser.session.cookies
			if fb_cookies:
				cookies_file = 'cookies.pk'
				with open(cookies_file, 'wb+') as fi:
					pickle.dump(fb_cookies, fi)
			else:
				print "Error : could not get cookies"
		else:
			print "Access Denied - not logged in, try again"
			sys.exit(2)
	
	# 4 . Search for matching facebook users
	fbUsers = get_fb_users(fbBrowser, inputNames)
	
	# 5. Extract the FB id for each user by following the link to their profile
	#fbUsers = add_field_to_users(fbUsers, "fb_uid", lambda user : get_fb_uid(user, fbBrowser))
	
	# 6 . Output result in desired format
	output_result(outputType, fbUsers)





