#!/usr/bin/env python

import json
import getopt, sys
import os
import errno
import urlparse
import pickle
import robobrowser
from urllib import quote
import re

def get_input_data(sys_args):
	input_data = []
	try:
		opts, non_opts_args = getopt.gnu_getopt(sys_args, "hvsl:c:j:e:p:", ["help", "verbose", "stdin", "inline-csv=", "csv=", "json=", "email=", "password="])
		
		# take the first non-optional argument as the command name
		command = non_opts_args.pop(0)
		#TODO : handle error if 0 non-optional argument
		# print command
		if command not in ["search", "like", "message"]:
			assert False, "unhandled command : " + command
					
		# default optional arguments
		input_type = "stdin"
		verbose = False
		fb_email = ""
		fb_password = ""
				
		for option, arg in opts:
			if option in ("-h", "--help"):
				print "help needed"
				# TODO
			elif option in ("-v", "--verbose"):
				verbose = True
			elif option in ("-s", "--stdin"):
				pass
			elif option in ("-l", "--inline-csv"):
				input_type = "inline-csv"
				input_data = arg.split(',')
			elif option in ("-j", "--json"):
				input_type = "json"
				with open(arg) as json_input:
					for json_object in json.load(json_input):
						input_data.append(json_object['name'])
						#TODO : handle other input fields
			elif option in ("-c", "--csv"):
				input_type = "csv"
				#TODO : loads CSV file
			elif option in ("-e", "--email"):
				fb_email = arg
			elif option in ("-p", "--password"):
				fb_password = arg
			else:
				assert False, "unhandled option : " + option
				
		if input_type is "stdin":
			# reading all (remaining) non-option arguments as strings 
			# print "remaining non-option arguments : '" + ", ".join(map(str, non_opts_args)) + "'"
			input_data = non_opts_args
		return [command, input_data, fb_email, fb_password]
	except getopt.GetoptError as err:
		sys.stderr.write(err)
		usage()
		sys.exit(2)

def get_fb_cookies():
	# Check if user token from previous session
	cookies_file = 'cookies.pk'
	if os.path.exists(cookies_file):
		with open(cookies_file, 'rb') as fi:
			try:
				saved_cookies = pickle.load(fi)
				return saved_cookies
			except EOFError:
				sys.stderr.write("No saved cookies in file : " + cookies_file)
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
		sys.stderr.write("Error : could not login")
		return False

def search_users_matching(name, browser):
	encoded_name = quote(name, safe='')
	#print encoded_name
	try:
		url = 'https://m.facebook.com/search/people/?q=' + encoded_name + '&tsid&source=filter&isTrending=0'
		browser.open(url)
		results_div = browser.select('div#BrowseResultsContainer')
		user_div_match_string = r'^{"type":"xtracking","xt":"12.{\\"unit_id_click_type\\":\\"graph_search_results_item_in_module_tapped\\"'
		user_divs = browser.find_all(attrs={"data-gt": re.compile(user_div_match_string)})
		return user_divs
	except:
		sys.stderr.write("Error while searching for users matching : " + name)
		return None

def output_result(results):
	results_type = "searched_user"
	results_data = "matching_users_divs"
	results_files = "matching_users_divs_files"
	#TODO : use generic key names
	for result in results:
		result[results_files] = []
		html_results = result[results_data]
		for i, html_result in enumerate(html_results):
			# Write HTML to file
			html_result_filename= "output/" + quote(result[results_type], safe='') + "-" + str(i) + ".html"
			if not os.path.exists(os.path.dirname(html_result_filename)):
				try:
					os.makedirs(os.path.dirname(html_result_filename))
				except OSError as exc: # Guard against race condition
					if exc.errno != errno.EEXIST:
						raise
			with open(html_result_filename, 'wb+') as html_result_file:
				html_result_file.write(str(html_result))
			# Add filename to results array
			result[results_files].append(html_result_filename)
		# Remove raw HTML from results
		result.pop(results_data, None)
	# Print results array to stdout
	print json.dumps(results) #, ensure_ascii=False, encoding="utf-8"

if __name__ == '__main__':

	# 0. Get input data (strings, JSON file or csv file)
	command, inputData, fbEmail, fbPassword = get_input_data(sys.argv[1:])
	
	# 1. Setup the scraper browser
	fbBrowser = robobrowser.RoboBrowser(parser="html.parser")
	fbBrowser.session.headers['User-Agent'] = 'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53'

	# 2A. Try to reuse cookies (if any) from previous session
	fbCookies = get_fb_cookies()
	if fbCookies:
		# print "Cookies found, no need to log in"
		fbBrowser.session.cookies = fbCookies
		#TODO : check if valid
		logged_in = True
		if not logged_in:
			# Clear cookies, if any saved
			try:
				os.remove('cookies.pk')
			except OSError:
				pass
	# 2B. Try to login using credentials
	else:
		# ask credentials if not provided as CL args
		if not fbEmail :
			#TODO: get fb mail
			print "no email provided"
		if not fbPassword :
			#TODO: get fb password
			print "no password provided"
		if fb_log_browser(fbBrowser, fbEmail, fbPassword):
			# Save cookies for future session
			fb_cookies = fbBrowser.session.cookies
			if fb_cookies:
				cookies_file = 'cookies.pk'
				with open(cookies_file, 'wb+') as fi:
					pickle.dump(fb_cookies, fi)
			else:
				sys.stderr.write("Error : could not get cookies")
		else:
			sys.stderr.write("Access Denied - not logged in, try again")
			sys.exit(2)
	
	results = []
	# 3A. Find matching Facebook users for each name provided
	if command == "search":
		# print "searching..."
		for searchedName in inputData:
			matchingUsersDivs = search_users_matching(searchedName, fbBrowser)
			searched_result = { "searched_user" : searchedName, "matching_users_divs" : matchingUsersDivs}
			results.append(searched_result)
		
	elif command is "like":
		#TODO
		print "batch like not implemented yet"
	elif command is "message":
		#TODO
		print "batch message not implemented yet"
		
	# 4. Output result in desired format
	output_result(results)






