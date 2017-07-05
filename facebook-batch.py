#!/usr/bin/env python

import json
import os
import errno
import urlparse
import pickle
import robobrowser
from urllib import quote
import re
from commonutils import parse_arguments, output_result

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

def search_users_divs_matching(name, browser):
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

def save_html_div(html_div, dir_prefix, filename_base, filename_index):
	html_filename = dir_prefix + "/" + quote(filename_base, safe='') + "-" + str(filename_index) + ".html"
	if not os.path.exists(os.path.dirname(html_filename)):
		try:
			os.makedirs(os.path.dirname(html_filename))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
	with open(html_filename, 'wb+') as html_file:
		html_file.write(str(html_div))
	return html_filename

if __name__ == '__main__':

	# 0A. Parse command line options and arguments
	command, optionsDict, remainingArguments = parse_arguments(["search","like","message"], ["v","s"], ["verbose","stdin"], ["l","c","j","h","e","p"], ["inline-csv","csv","json","html","email","password"])
	# 0B. Grab option values or use default if none provided
	verbose = optionsDict.get("verbose", False)
	stdInput = optionsDict.get("stdin", False)
	inlineCsv = optionsDict.get("inline-csv", None)
	jsonInput = optionsDict.get("json", None)
	csvInput = optionsDict.get("csv", None)
	fbEmail = optionsDict.get("email", "")
	fbPassword = optionsDict.get("password", "")
	outputType = optionsDict.get("output", "stdout")
	htmlOutput = optionsDict.get("html", "file") #for search
	# if htmlOutput not in ["raw", "file"]:
	# 	assert False, "unhandled output : " + html_output			
	# 0C. Get input data (from stdin, JSON or CSV)
	if inlineCsv:
		inputData = inlineCsv.split(',')
	elif jsonInput:
		inputData = []
		with open(jsonInput) as json_input:
			for json_object in json.load(json_input):
				inputData.append(json_object['name'])
				#TODO : handle all input fields
	elif csvInput:
		inputData = []
		#TODO : loads CSV file
	else: #if stdInput:
		# print "reading all (remaining) non-option arguments : '" + ", ".join(map(str, remainingArguments)) + "' as input"
		inputData = remainingArguments
	
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
			matchingUsersHtmlDivsRaw = search_users_divs_matching(searchedName, fbBrowser)
			if htmlOutput is "file":
				matchingUsersHtmlDivsFilenames = []
				for index, matchingUserHtmlDivRaw in enumerate(matchingUsersHtmlDivsRaw):
					matchingUsersHtmlDivFilename = save_html_div(matchingUserHtmlDivRaw, "output", searchedName, index)
					matchingUsersHtmlDivsFilenames.append(matchingUsersHtmlDivFilename)
				searchedResult = { "searched_user" : searchedName, "matching_users_divs_filenames" : matchingUsersHtmlDivsFilenames}
			else:
				searchedResult = { "searched_user" : searchedName, "matching_users_divs" : matchingUsersHtmlDivsRaw}
			results.append(searchedResult)
	elif command is "like":
		#TODO
		print "batch like not implemented yet"
	elif command is "message":
		#TODO
		print "batch message not implemented yet"
		
	# 4. Output result in desired format
	output_result(results, "stdout")






