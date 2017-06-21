**facebook-scraper** is a python script which grabs the Facebook attributes for a list of users (provided as CSV, JSON or as command line arguments) and outputs them as desired : by adding the fields to the input file or by creating an output file.

# why

When targeting multiple people it can be useful to quickly get some data about them from Facebook, most notably the Facebook ID can be used to send an email to a Facebook user (facebook_ID@facebook.com) which will appear as a regular Facebook message to this user (see http://smallbusiness.chron.com/email-address-facebook-id-53471.html).

# Use

## Facebook App setup

Facebook user access token is required to search users through the Graph API.
A Facebook app is necessary to send this token to **facebook-scraper**, thus a Facebook app needs to be created so this script can retrieve the user token.

- Upload the content of the directory webpage to a web server.
- Go to the [Facebook dev website](https://developers.facebook.com/apps/)
- Click "My Apps" drop-down then "Add a New App".
- Click add platform and select "web", fill "Site URL" with the address of the web page you have uploaded : https://your-website.com/path/to/facebook-login.html
- Fill the field "App Domains" with the base URL of this web page : https://your-website.com
- Copy the Facebook app ID and set the value of `fb_app_id` in facebook-scraper.py.
- Set the value of `redirect_url` in facebook-scraper.py : https://your-website.com/path/to/facebook-login.html

You will be prompted to grant access to this Facebook app once running the script. 

## provide list of names as non-option arguments (one or more)
	
`facebook-parser.py "John Doe"`
	
output :

```
[
	{
		"id": "109571456326532",
		"name": "Doe John"
	},
	{
		"id": "140568483146921",
		"name": "Doe John"
	},
	{
		"id": "276266322840319",
		"name": "Jonathan Doe"
	},
	{
		"id": "1646054118943956",
		"name": "John Pazdan"
	},
	...
]
```

## provide list of names in a file (JSON or CSV)

### CSV

`facebook-parser.py --csv=people.csv` or `facebook-parser.py -c=people.csv`

### JSON

`facebook-parser.py --json=people.json` or `facebook-parser.py -j=people.json`.

See provided `people.json` example file.


# dependancies

- [facepy](https://github.com/jgorset/facepy) `pip instal facepy`
- [pywebview](https://github.com/r0x0r/pywebview) `pip install pywebview`


# ressources

- https://stackoverflow.com/questions/43192556/using-jq-with-bash-to-run-command-for-each-object-in-array
- https://stackoverflow.com/questions/31988171/facebook-graph-api-simple-search-for-users-by-name
- https://stackoverflow.com/questions/23428498/get-username-field-in-facebook-graph-api-2-0
- https://stackoverflow.com/questions/12943819/how-to-python-prettyprint-a-json-file
- https://stackoverflow.com/questions/20199126/reading-json-from-a-file
- https://stackoverflow.com/questions/1695183/how-to-percent-encode-url-parameters-in-python
- https://stackoverflow.com/questions/4184108/python-json-dumps-cant-handle-utf-8
- https://stackoverflow.com/questions/21310648/facebook-app-this-must-be-derived-from-canvas-url-secure-canvas-url
- https://stackoverflow.com/questions/8802860/checking-whether-a-string-starts-with-xxxx
- https://stackoverflow.com/questions/3221655/python-threading-string-arguments
- https://stackoverflow.com/questions/31891286/keeping-the-data-of-a-variable-between-runs-of-code
- https://www.daniweb.com/programming/software-development/threads/259751/function-returning-a-value-multi-thread

# code


## contributing

This project adheres to the Contributor Covenant [code of conduct](code-of-conduct.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior to monkeydri@github.com.
