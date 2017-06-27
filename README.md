**facebook-scraper** is a python script which grabs the Facebook attributes for a list of users (provided as CSV, JSON or as command line arguments) and outputs them as desired : by adding the fields to the input file or by creating an output file.

# why

When targeting multiple people it can be useful to quickly get some data about them from Facebook, most notably the Facebook UID which could be used to send an email to a Facebook user via facebook_ID@facebook.com (see http://smallbusiness.chron.com/email-address-facebook-id-53471.html or https://www.matthewbarby.com/emailing-facebook-followers/). It is now deprecated but the Facebook UID is still useful for many plugins or mass marketing tools.

# Use

## provide list of names as non-option arguments (one or more)
	
`facebook-parser.py "John Doe" "John Smith"`
	
output :

```
[
	{
	"searched_user": "John Doe",
	"matching_users_attributes": 
		[
			{
				"fb_customized_url": "JohnJohn.Doe",
				"fb_name": "John-john Doe",
				"fb_uid": "100000016191070",
				"picture_url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/c0.13.64.64/p64x64/1920462_779525028724696_446426524_n.jpg?efg=eyJpIjoibCJ9&oh=f0ae9a0e5e743da1c1326144343da3f8&oe=59E1F6F1"
			},
			{
				"fb_customized_url": "johndoe.escobar",
				"fb_name": "John-Doe Escobar",
				"fb_uid": "1125608844",
				"picture_url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/p64x64/18447291_10211252162596279_5275418469254673155_n.jpg?efg=eyJpIjoibCJ9&oh=96fa5cbde90a96c2f8abddb8ae922e88&oe=59E1984E"
			},
			...
		]
	},
	{
	"searched_user": "John Smith",
	"matching_users_attributes": 
		[
			{
				"fb_name": "John Smith",
				"fb_uid": "674345013",
				"picture_url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/p64x64/15697334_10158029528495014_4623996019099638763_n.jpg?efg=eyJpIjoibCJ9&oh=3002b1557ce4961f8afec030ef289435&oe=59E3CAEB"
			},
			{
				"fb_customized_url": "UBetterfollowSmith",
				"fb_name": "John Smith",
				"fb_uid": "692792352",
				"picture_url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/p64x64/17457642_10154255617277353_8169698937347482715_n.jpg?efg=eyJpIjoibCJ9&oh=b8e9e91fb4a6719991e13b74afde5845&oe=59CBBD3F"
			},
			...
		]
	}
]
```

## provide list of names in a file (JSON or CSV)

### CSV

`facebook-parser.py --csv=people.csv` or `facebook-parser.py -c people.csv`

### JSON

`facebook-parser.py --json=people.json` or `facebook-parser.py -j people.json`

See provided `people.json` example file.

## input your credentials

`facebook-parser.py --email="your.email@example.com"` or `facebook-parser.py -e "your.email@example.com"`
`facebook-parser.py --password="xxxxxxxx"` or `facebook-parser.py -p "xxxxxxxx"`

## specify output format (console, JSON file or CSV file)

### Console output

`facebook-parser.py --output=stdin` or `facebook-parser.py -o stdin`

### CSV

`facebook-parser.py --output=csv` or `facebook-parser.py -o csv`

### JSON

`facebook-parser.py --output=json` or `facebook-parser.py -o json`

## specify data

`facebook-parser.py --verbose` or `facebook-parser.py -v` outputs all data fetchable from website (by default it only outputs name, picture and Facebook ID).


# dependancies

- [robobrowser](https://github.com/jmcarp/robobrowser) `pip install robobrowser`

# ressources used

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
- https://stackoverflow.com/questions/2967194/open-in-python-does-not-create-a-file-if-it-doesnt-exist
- https://stackoverflow.com/questions/5627425/what-is-a-good-way-to-handle-exceptions-when-trying-to-read-a-file-in-python
- https://stackoverflow.com/questions/6996603/how-to-delete-a-file-or-folder
- https://www.codecademy.com/en/forum_questions/50ad6fa75a0341fd44001e34
- https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file-in-python
- https://stackoverflow.com/questions/1720421/how-to-append-list-to-second-list-concatenate-lists
- https://github.com/r0x0r/pywebview/issues/46
- https://stackoverflow.com/questions/2785821/is-there-an-easy-way-in-python-to-wait-until-certain-condition-is-true
- https://stackoverflow.com/questions/3605188/communicating-end-of-queue
- https://stackoverflow.com/questions/15652427/variable-or-variable-is-not-none
- https://pymotw.com/2/getopt/
- https://stackoverflow.com/questions/6665082/how-to-pass-an-if-statement-to-a-python-method
- https://github.com/r0x0r/pywebview/blob/c5ff4e136202e1687664518f8de9893f63915f51/tests/util.py
- https://stackoverflow.com/questions/10840533/most-pythonic-way-to-delete-a-file-which-may-not-exist
- https://stackoverflow.com/questions/6665082/how-to-pass-an-if-statement-to-a-python-method
- https://github.com/r0x0r/pywebview/issues/58
- https://stackoverflow.com/questions/19790570/python-global-variable-with-thread
- https://stackoverflow.com/questions/20475552/python-requests-library-redirect-new-url/20475712#20475712
- https://stackoverflow.com/questions/21928368/login-to-facebook-using-python-requests
- https://stackoverflow.com/questions/28560092/download-images-and-pdf-using-python-robobrowser
- https://stackoverflow.com/questions/24300309/get-facebook-profile-url-from-app-scoped-user-id
- https://stackoverflow.com/questions/5214578/python-print-string-to-text-file
- https://stackoverflow.com/questions/5099193/using-beautifulsoup-to-find-all-elements-starting-with-a-given-letter
- https://stackoverflow.com/questions/6109882/regex-match-all-characters-between-two-strings
- https://regex101.com/
- https://stackoverflow.com/questions/41620093/whats-the-difference-between-re-dotall-and-re-multiline
- https://stackoverflow.com/questions/180986/what-is-the-difference-between-pythons-re-search-and-re-match
- https://docs.python.org/2/howto/regex.html#grouping
- https://stackoverflow.com/questions/13202087/beautiful-soup-find-children-for-particular-div
- https://stackoverflow.com/questions/5015483/test-if-an-attribute-is-present-in-a-tag-in-beautifulsoup
- https://stackoverflow.com/questions/1592565/determine-if-variable-is-defined-in-python
- https://stackoverflow.com/questions/11277432/how-to-remove-a-key-from-a-python-dictionary

# code

## contributing

This project adheres to the Contributor Covenant [code of conduct](code-of-conduct.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior to monkeydri@github.com.
