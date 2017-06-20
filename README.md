**facebook-scraper** is a python script which grabs the Facebook attributes for a list of users (provided as CSV, JSON or as command line arguments) and outputs them as desired : by adding the fields to the input file or by creating an output file.

# why

When targeting multiple people it can be useful to quickly get some data about them from Facebook, most notably the Facebook ID can be used to send an email to a Facebook user (facebook_ID@facebook.com) which will appear as a regular Facebook message to this user (see http://smallbusiness.chron.com/email-address-facebook-id-53471.html).

# Use

Facebook access token is required. A quick way to get one : 

- Go to the [Graph API Explorer](https://developers.facebook.com/tools/explorer)
- Click on the Get Token button in the top right of the Explorer.
- Choose the option Get User Access Token.
- In the following dialog don't check any boxes, just click the blue Get Access Token button.
- You'll see a Facebook Login Dialog, click OK to proceed.

source : https://developers.facebook.com/docs/graph-api/overview/



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


# ressources

- https://stackoverflow.com/questions/43192556/using-jq-with-bash-to-run-command-for-each-object-in-array
- https://stackoverflow.com/questions/31988171/facebook-graph-api-simple-search-for-users-by-name
- https://stackoverflow.com/questions/23428498/get-username-field-in-facebook-graph-api-2-0
- https://stackoverflow.com/questions/12943819/how-to-python-prettyprint-a-json-file
- https://stackoverflow.com/questions/20199126/reading-json-from-a-file
- https://stackoverflow.com/questions/1695183/how-to-percent-encode-url-parameters-in-python
- https://stackoverflow.com/questions/4184108/python-json-dumps-cant-handle-utf-8

# code


## contributing

This project adheres to the Contributor Covenant [code of conduct](code-of-conduct.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior to monkeydri@github.com.
