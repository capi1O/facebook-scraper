**facebook-scraper** is a  python script to scrap data from Facebook webpages : Facebook id (UID), name, profile picture, Likes number, etc... Input can be CSV, JSON or input from another script. 

# Why

When targeting multiple people it can be useful to quickly get some data about them from Facebook, most notably the Facebook UID which could be used to send an email to a Facebook user via facebook_ID@facebook.com (see http://smallbusiness.chron.com/email-address-facebook-id-53471.html or https://www.matthewbarby.com/emailing-facebook-followers/). It is now deprecated but the Facebook UID is still useful for many plugins or mass marketing tools.

# Use

- input : URL, HTML file path, escaped HTML data. 
- output : JSON to stdout, JSON file or CSV file.

## Scrap Facebook user attributes from a search result

`./facebook-scrap.py user-search "input/John%20Smith-8.html" "input/John%20Smith-9.html"` => scrap user attributes from HTML block of a result from a search on Facebook :

```
{
	"fb_customized_url": "JohnJohn.Doe",
	"fb_name": "John-john Doe",
	"fb_uid": "100000016191070",
	"picture_url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/c0.13.64.64/p64x64/1920462_779525028724696_446426524_n.jpg?efg=eyJpIjoibCJ9&oh=f0ae9a0e5e743da1c1326144343da3f8&oe=59E1F6F1"
}
```

## Scrap Facebook user attributes from Facebook Profile or Facebook Page

`facebook-scrap.py profile "https://facebook.com/JohnJohn.Doe"` => scrap user attributes from a Facebook profile HTML  *not implemented yet*:

```
{
	"fb_customized_url": "JohnJohn.Doe",
	"fb_name": "John-john Doe",
	"fb_uid": "100000016191070",
	"friends_number": "112"
	"picture_url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/c0.13.64.64/p64x64/1920462_779525028724696_446426524_n.jpg?efg=eyJpIjoibCJ9&oh=f0ae9a0e5e743da1c1326144343da3f8&oe=59E1F6F1"
}
```

## Scrap Facebook user attributes from Facebook Page

`facebook-scrap.py page "https://facebook.com/TheCocaColaCo" "input/nike-7.html"` => scrap user attributes from a Facebook Page HTML *not implemented yet* :

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

## multi-inputs

**facebook-scraper** input can be a file containing a group of elements to scrap, organized in different ways (see provided example JSON files) :
- JSON array of elements
- JSON array of dictionaries containing arrays of elements, so the results are grouped together.

### input = array of elements

`facebook-scrap.py user-search "search-results-array.json"` => scrap user attributes from HTML block of a result from a search on Facebook :

```
{
	"fb_customized_url": "JohnJohn.Doe",
	"fb_name": "John-john Doe",
	"fb_uid": "100000016191070",
	"picture_url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/c0.13.64.64/p64x64/1920462_779525028724696_446426524_n.jpg?efg=eyJpIjoibCJ9&oh=f0ae9a0e5e743da1c1326144343da3f8&oe=59E1F6F1"
}
```
### input = dict array of elements

`facebook-scrap.py user-search "search-results-dicts.json" --key="searched_user"` => scrap user attributes from HTML block of a result from a search on Facebook :

```
"searched_user": "John Smith",
"matching_users_attributes":
[
	{
			"fb_name": "John Smith",
			"fb_uid": "100009172756372",
			"picture_url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/p64x64/15181176_1712647975717611_9091052979118252446_n.jpg?efg=eyJpIjoibCJ9&oh=e3a2f9b79b66716086c958888027f03d&oe=5A06DA05"
	},
	{
			"fb_customized_url": "teste.smith.507",
			"fb_name": "John Smith",
			"fb_uid": "100014191692436",
			"picture_url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/p64x64/16711476_185636188586103_6542105539833592941_n.jpg?efg=eyJpIjoibCJ9&oh=d3ac902a7e385e7c0bfe8aee634e78f6&oe=59D4B1A4"
	},
	{
			"fb_name": "John Smith",
			"fb_uid": "1211347411",
			"picture_url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/c19.0.64.64/p64x64/10354686_10150004552801856_220367501106153455_n.jpg?efg=eyJpIjoibCJ9&oh=d8472400e63b67b3d0a61447137a7f5a&oe=59D260FC"
	},
	{
			"fb_name": "John Smith",
			"fb_uid": "100007384814243",
			"picture_url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/p64x64/18622587_1780866002169543_108408991042153430_n.jpg?efg=eyJpIjoibCJ9&oh=16f21eb65adcd35bb4b6f187a78df914&oe=59CE3769"
	},
	{
			"fb_customized_url": "Dragma",
			"fb_name": "John Smith",
			"fb_uid": "759052697",
			"picture_url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/c2.0.64.64/p64x64/150981_10151409656362698_1573096695_n.jpg?efg=eyJpIjoibCJ9&oh=5193f524380e9ea12454d77b8a518762&oe=5A0894A2"
	}
]
}
]
```

## Specify output (JSON to console, JSON file or CSV file)

- `facebook-scrap.py user-search "input/John%20Smith-8.html" "input/John%20Smith-9.html" --output=stdout` or `-o stdout` => serialized array of dicts to stdout (default)
- `facebook-scrap.py user-search "input/John%20Smith-8.html" "input/John%20Smith-9.html" --output=csv` or `-o csv` => save as a CSV file *not implemented yet*
- `facebook-scrap.py user-search "input/John%20Smith-8.html" "input/John%20Smith-9.html" --output=json` or `-o json` => save as a JSON file

# Code

## Contributing

This project adheres to the Contributor Covenant [code of conduct](code-of-conduct.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior to monkeydri@github.com.
