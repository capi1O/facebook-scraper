**facebook-scraper** is a set of python scripts to perform batch requests to Facebook and scrap data from it. Can search for multiple users or Pages at once, send messages or posts to multiple users, like multiple Facebook Pages... Scraped data can be Facebook id (UID), name, profile picture, Likes number, etc... Input can be CSV, JSON or input from another script. 

This tool does not use the Graph API as it is limited in the number of requests that can be made, also not all the data is available from the Graph API.

# Why

When targeting multiple people it can be useful to quickly get some data about them from Facebook, most notably the Facebook UID which could be used to send an email to a Facebook user via facebook_ID@facebook.com (see http://smallbusiness.chron.com/email-address-facebook-id-53471.html or https://www.matthewbarby.com/emailing-facebook-followers/). It is now deprecated but the Facebook UID is still useful for many plugins or mass marketing tools.

# Use

## Scrap data : `facebook-scrap.py`

input : list of URLs (or local HTML files paths)
output : JSON to stdout or file, CSV file

### Scrap Facebook user attributes from a search result

- `facebook-scrap.py user-search "input/John%20Smith-8.html" "input/John%20Smith-9.html"` => scrap user attributes from HTML block of a result from a search on Facebook :

```
{
	"fb_customized_url": "JohnJohn.Doe",
	"fb_name": "John-john Doe",
	"fb_uid": "100000016191070",
	"picture_url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/c0.13.64.64/p64x64/1920462_779525028724696_446426524_n.jpg?efg=eyJpIjoibCJ9&oh=f0ae9a0e5e743da1c1326144343da3f8&oe=59E1F6F1"
}
```
### Scrap Facebook user attributes from Facebook Profile or Facebook Page

- `facebook-scrap.py profile "https://facebook.com/JohnJohn.Doe"` => scrap user attributes from a Facebook profile HTML  *not implemented yet*:

```
{
	"fb_customized_url": "JohnJohn.Doe",
	"fb_name": "John-john Doe",
	"fb_uid": "100000016191070",
	"friends_number": "112"
	"picture_url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/c0.13.64.64/p64x64/1920462_779525028724696_446426524_n.jpg?efg=eyJpIjoibCJ9&oh=f0ae9a0e5e743da1c1326144343da3f8&oe=59E1F6F1"
}
```

- `facebook-scrap.py page "https://facebook.com/TheCocaColaCo" "input/nike-7.html"` => scrap user attributes from a Facebook Page HTML *not implemented yet* :

```
{
	"fb_customized_url": "TheCocaColaCo",
	"fb_name": "Coca Cola",
	"fb_uid": "100000016191070",
	"likes": "7980542"
	"picture_url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/c0.13.64.64/p64x64/1920462_779525028724696_446426524_n.jpg?efg=eyJpIjoibCJ9&oh=f0ae9a0e5e743da1c1326144343da3f8&oe=59E1F6F1"
},
{
	"fb_customized_url": "nike",
	"fb_name": "Nike",
	"fb_uid": "10321191219",
	"likes": "123756"
	"picture_url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/c0.13.64.64/p64x64/1920462_779525028724696_446426524_n.jpg?efg=eyJpIjoibCJ9&oh=f0ae9a0e5e743da1c1326144343da3f8&oe=59E1F6F1"
}
```

### Specify output (JSON to console, JSON file or CSV file)

- `facebook-scrap.py user-search "input/John%20Smith-8.html" "input/John%20Smith-9.html" --output=stdout` or `-o stdout` => serialized array of dicts to stdout (default)
- `facebook-scrap.py user-search "input/John%20Smith-8.html" "input/John%20Smith-9.html" --output=csv` or `-o csv` => save as a CSV file *not implemented yet*
- `facebook-scrap.py user-search "input/John%20Smith-8.html" "input/John%20Smith-9.html" --output=json` or `-o json` => save as a JSON file

## Batch Requests : `facebook-batch.py`

input : list of strings, CSV file, JSON file
output : serialized array of dicts to stdout

### Provide credentials

On first connection `facebook-batch` needs your credentials (for next connections it uses cookies). If none are given you will be prompted to enter them; to avoid that provide them as arguments :

`facebook-batch.py --email="your.email@example.com" --password="xxxxxxxx"` or `-e "your.email@example.com" -p "xxxxxxxx"`

### Search Facebook users 

- `facebook-batch.py search "John Doe" "John Smith"` => get raw HTML data for all Facebook users matching names John Doe and John Smith :

```
[{"searched_user": "John Doe", "matching_users_divs_files": ["output/John%20Doe-0.html", "output/John%20Doe-1.html", "output/John%20Doe-2.html", "output/John%20Doe-3.html", "output/John%20Doe-4.html", "output/John%20Doe-5.html", "output/John%20Doe-6.html", "output/John%20Doe-7.html", "output/John%20Doe-8.html", "output/John%20Doe-9.html"]}, {"searched_user": "John Smith", "matching_users_divs_files": ["output/John%20Smith-0.html", "output/John%20Smith-1.html", "output/John%20Smith-2.html", "output/John%20Smith-3.html", "output/John%20Smith-4.html", "output/John%20Smith-5.html", "output/John%20Smith-6.html", "output/John%20Smith-7.html", "output/John%20Smith-8.html", "output/John%20Smith-9.html"]}]
```

This is useless as such unless you parse it to get actual data from it. The output can be parsed with `facebook-scrap.py` thanks to a handy `pipe-mapper.py` script which maps the output of `facebook-bash.py` to the input of `facebook-scrap.py` :

`python facebook-batch.py search "John Doe" "John Smith" --email="your.email@example.com" --password="xxxxxxxx" | python pipe-mapper.py -o facebook-scrap.py -c user-search` : 

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
	]},
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
	]}
]
```

### Like Facebook Pages 

- `facebook-batch.py like "TheCocaColaCo" "nike"` => like all Pages matching customized URL or Facebook UIDs provided. *not implemented yet*

### Send messages to Facebook users 

- `facebook-batch.py message "100000016191070" "674345013"` => send a message to all Facebook users matching customized URL or Facebook UIDs provided. *not implemented yet*

### Use a file as input (list of strings, JSON file or CSV file)

- `facebook-batch.py search --strings "John Doe" "John Smith"` or `-s "John Doe" "John Smith"` => list of names to search as non-option arguments (one or more) (default)
- `facebook-batch.py search --inline-csv "John Doe,John Smith"` or `-l "John Doe,John Smith"` => list of names to search as comma-separated strings.
- `facebook-batch.py search --csv=names.csv` or `-c names.csv` => list of names to search in a CSV file. *not implemented yet*
- `facebook-batch.py search --json=names.json` or `-j names.json` => JSON array of names to search in a file. See provided `names.json` example file.
- `facebook-batch.py like --json=pages.json` or `-j pages.json` => JSON array of pages to like in a file. See provided `pages.json` example file.
- `facebook-batch.py like --json=posts.json` or `-j posts.json` => JSON array of posts to like in a file. See provided `posts.json` example file.
- `facebook-batch.py message --json=uids.json` or `-j uids.json` => JSON array of Facebook UIDs to send a message to in a file. See provided `uids.json` example file.

# Dependancies

- `facebook-scrap.py`
	- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) `pip install bs4`

- `facebook-batch.py`
	- [robobrowser](https://github.com/jmcarp/robobrowser) `pip install robobrowser`

# Ressources used

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
- https://stackoverflow.com/questions/5864485/how-can-i-split-this-comma-delimited-string-in-python
- http://www.bogotobogo.com/python/python_serialization_pickle_json.php
- https://stackoverflow.com/questions/2831597/processing-command-line-arguments-in-prefix-notation-in-python
- https://stackoverflow.com/questions/1504717/why-does-comparing-strings-in-python-using-either-or-is-sometimes-produce
- https://stackoverflow.com/questions/522563/accessing-the-index-in-python-for-loops
- https://stackoverflow.com/questions/40529848/python-beautifulsoup-how-to-write-the-output-to-html-file
- https://stackoverflow.com/questions/4429966/how-to-make-a-python-script-pipeable-in-bash
- https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
- https://stackoverflow.com/questions/38028384/beautifulsoup-is-there-a-difference-between-find-and-select-python-3-x
- https://stackoverflow.com/questions/4547274/convert-a-python-dict-to-a-string-and-back
- https://stackoverflow.com/questions/9787024/extracting-data-from-html-files-with-beautifulsoup-and-python
- https://stackoverflow.com/questions/29928168/why-json-loads-is-returning-a-unicode-object-instead-of-string
- https://stackoverflow.com/questions/3781851/run-a-python-script-from-another-python-script-passing-in-args
- https://stackoverflow.com/questions/1904394/read-only-the-first-line-of-a-file
- https://stackoverflow.com/questions/3503879/assign-output-of-os-system-to-a-variable-and-prevent-it-from-being-displayed-on 

# Code

## Contributing

This project adheres to the Contributor Covenant [code of conduct](code-of-conduct.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior to monkeydri@github.com.
