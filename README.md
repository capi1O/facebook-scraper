**facebook-scraper** is a  python script to scrap data from Facebook webpages : Facebook id (UID), name, profile picture, Likes number, etc... Input can be CSV, JSON or input from another script. 

# Why

When targeting multiple people it can be useful to quickly get some data about them from Facebook, most notably the Facebook UID which could be used to send an email to a Facebook user via facebook_ID@facebook.com (see http://smallbusiness.chron.com/email-address-facebook-id-53471.html or https://www.matthewbarby.com/emailing-facebook-followers/). It is now deprecated but the Facebook UID is still useful for many plugins or mass marketing tools.

# Use

- input : URL, HTML file path, raw (escaped) HTML data. 
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

## inputs

**facebook-scraper** input can be a file containing a group of elements to scrap, organized in different ways (see provided example JSON files) :
- JSON array of elements
- JSON array of dictionaries containing arrays of elements, so the results are grouped together.

### input = raw HTML string

```
./facebook-scrap.py user-search -o pretty '<div class="_5w3g" data-gt='"'"'{"type":"xtracking","xt":"12.{\"unit_id_click_type\":\"graph_search_results_item_in_module_tapped\",\"click_type\":\"result\",\"module_id\":0,\"result_id\":759052697,\"sid\":\"bbc94eb2ff0132a843b19f786901a7c3\",\"module_role\":\"NONE\",\"unit_id\":\"browse_rl:5a1bfc31f6c1becb1ff4f924119b38eb:c1\",\"browse_result_type\":\"browse_type_user\",\"unit_id_result_id\":759052697,\"module_result_position\":9}"}'"'"' data-vistracking="1" data-xt='"'"'12.{"unit_id_click_type":"graph_search_results_item_in_module_tapped","click_type":"result","module_id":0,"result_id":759052697,"sid":"bbc94eb2ff0132a843b19f786901a7c3","module_role":"NONE","unit_id":"browse_rl:5a1bfc31f6c1becb1ff4f924119b38eb:c1","browse_result_type":"browse_type_user","unit_id_result_id":759052697,"module_result_position":9}'"'"' data-xt-vimp='"'"'{"pixel_in_percentage":70,"duration_in_ms":2000,"subsequent_gap_in_ms":500,"log_initial_nonviewable":true,"should_batch":true,"require_horizontally_onscreen":false}'"'"'><div class="_4g33 _52we"><div class="_5s61" style="margin-bottom:10px;"><a href="/Dragma?refid=46&amp;__xt__=12.%7B%22unit_id_click_type%22%3A%22graph_search_results_item_in_module_tapped%22%2C%22click_type%22%3A%22result%22%2C%22module_id%22%3A0%2C%22result_id%22%3A759052697%2C%22sid%22%3A%22bbc94eb2ff0132a843b19f786901a7c3%22%2C%22module_role%22%3A%22NONE%22%2C%22unit_id%22%3A%22browse_rl%3A5a1bfc31f6c1becb1ff4f924119b38eb%3Ac1%22%2C%22browse_result_type%22%3A%22browse_type_user%22%2C%22unit_id_result_id%22%3A759052697%2C%22module_result_position%22%3A9%7D"><i aria-label="John Smith" class="img _5w3h profpic" role="img" style='"'"'background:#d8dce6 url("https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/c2.0.64.64/p64x64/150981_10151409656362698_1573096695_n.jpg?efg=eyJpIjoibCJ9&amp;oh=5193f524380e9ea12454d77b8a518762&amp;oe=5A0894A2") no-repeat center;background-size:100% 100%;-webkit-background-size:100% 100%;width:64px;height:64px;'"'"'></i></a></div><div class="_4g34"><div class="_10ws"><div class="_2gpa"><div class="_5k8z"><div class="_5tg_"><span class="_5w3i _o9-">John Smith</span></div></div></div><a class="_5w3n" data-sigil="m-graph-search-result-page-click-target" data-store='"'"'{"unit_id_click_type":"graph_search_results_item_in_module_tapped","click_type":"result","module_id":0,"result_id":759052697,"sid":"bbc94eb2ff0132a843b19f786901a7c3","module_role":"NONE","unit_id":"browse_rl:5a1bfc31f6c1becb1ff4f924119b38eb:c1","browse_result_type":"browse_type_user","unit_id_result_id":759052697,"module_result_position":9}'"'"' href="/Dragma?refid=46&amp;__xt__=12.%7B%22unit_id_click_type%22%3A%22graph_search_results_item_in_module_tapped%22%2C%22click_type%22%3A%22result%22%2C%22module_id%22%3A0%2C%22result_id%22%3A759052697%2C%22sid%22%3A%22bbc94eb2ff0132a843b19f786901a7c3%22%2C%22module_role%22%3A%22NONE%22%2C%22unit_id%22%3A%22browse_rl%3A5a1bfc31f6c1becb1ff4f924119b38eb%3Ac1%22%2C%22browse_result_type%22%3A%22browse_type_user%22%2C%22unit_id_result_id%22%3A759052697%2C%22module_result_position%22%3A9%7D"></a></div></div><div class="_5s61"><div class="right _71r _4nfz" data-gt='"'"'{"type":"xtracking","xt":"12.{\"unit_id_click_type\":\"inline_friend_request\",\"click_type\":\"result\",\"module_id\":0,\"result_id\":759052697,\"sid\":\"bbc94eb2ff0132a843b19f786901a7c3\",\"module_role\":\"NONE\",\"unit_id\":\"browse_rl:5a1bfc31f6c1becb1ff4f924119b38eb:c1\",\"browse_result_type\":\"browse_type_user\",\"unit_id_result_id\":759052697,\"module_result_position\":9}"}'"'"' data-sigil="m-add-friend-secondary m-graph-search-result-page-friend-button m-graph-search-result-page-action-button" data-store='"'"'{"unit_id_click_type":"graph_search_results_item_in_module_tapped","click_type":"result","module_id":0,"result_id":759052697,"sid":"bbc94eb2ff0132a843b19f786901a7c3","module_role":"NONE","unit_id":"browse_rl:5a1bfc31f6c1becb1ff4f924119b38eb:c1","browse_result_type":"browse_type_user","unit_id_result_id":759052697,"module_result_position":9}'"'"' data-vistracking="1" data-xt='"'"'12.{"unit_id_click_type":"inline_friend_request","click_type":"result","module_id":0,"result_id":759052697,"sid":"bbc94eb2ff0132a843b19f786901a7c3","module_role":"NONE","unit_id":"browse_rl:5a1bfc31f6c1becb1ff4f924119b38eb:c1","browse_result_type":"browse_type_user","unit_id_result_id":759052697,"module_result_position":9}'"'"' data-xt-vimp='"'"'{"pixel_in_percentage":70,"duration_in_ms":2000,"subsequent_gap_in_ms":500,"log_initial_nonviewable":true,"should_batch":true,"require_horizontally_onscreen":false}'"'"' id="u_0_3" style="margin-right: 0px; margin-top: -15px;"><div data-sigil="m-add-friend-flyout"><a aria-label="Add Friend" class="touchable right _41g3" data-sigil="touchable m-add-friend" data-store='"'"'{"hf":"browse","id":759052697,"sc":-1,"so":"pyu","pl":null,"searchlog":null,"et":"","at":"","ed":"","fref":"none","pymk_group_id":null,"el":null,"floc":"","frefs":[]}'"'"' href="/a/mobile/friends/add_friend.php?id=759052697&amp;hf=browse&amp;fref=none&amp;gfid=AQDFXn-mOnFK2lik&amp;refid=46&amp;__xt__=12.%7B%22unit_id_click_type%22%3A%22inline_friend_request%22%2C%22click_type%22%3A%22result%22%2C%22module_id%22%3A0%2C%22result_id%22%3A759052697%2C%22sid%22%3A%22bbc94eb2ff0132a843b19f786901a7c3%22%2C%22module_role%22%3A%22NONE%22%2C%22unit_id%22%3A%22browse_rl%3A5a1bfc31f6c1becb1ff4f924119b38eb%3Ac1%22%2C%22browse_result_type%22%3A%22browse_type_user%22%2C%22unit_id_result_id%22%3A759052697%2C%22module_result_position%22%3A9%7D" role="button"><i class="touched_hide _4iru img sp_THrB2DDAoX4 sx_429dae"></i><i class="_4iru touched_show img sp_THrB2DDAoX4 sx_7e3f0d"></i></a></div><div class="_2so _2sq _2ss img _50ch _5d0w" data-animtype="3" data-sigil="m-loading-indicator-root load" id="u_0_4" style="display:none"><div class="_2sr" data-sigil="m-loading-indicator-animate"></div></div><a aria-label="Undo" class="touchable right _58x3" data-sigil="touchable check m-cancel-request" data-store='"'"'{"id":759052697,"ref_param":"unknown","floc":"","frefs":[]}'"'"' role="button" style="display:none"><i class="touched_hide _4irt img sp_THrB2DDAoX4 sx_644cf7"></i><i class="_4irt touched_show img sp_THrB2DDAoX4 sx_737f51"></i></a></div><iframe class="fbEmuTracking" frameborder="0" height="0" scrolling="no" src="/xti.php?xt=12.%7B%22unit_id_click_type%22%3A%22inline_friend_request%22%2C%22click_type%22%3A%22result%22%2C%22module_id%22%3A0%2C%22result_id%22%3A759052697%2C%22sid%22%3A%22bbc94eb2ff0132a843b19f786901a7c3%22%2C%22module_role%22%3A%22NONE%22%2C%22unit_id%22%3A%22browse_rl%3A5a1bfc31f6c1becb1ff4f924119b38eb%3Ac1%22%2C%22browse_result_type%22%3A%22browse_type_user%22%2C%22unit_id_result_id%22%3A759052697%2C%22module_result_position%22%3A9%7D" width="0"></iframe></div></div></div>' -i raw
```

```
[
	{
		"fb_customized_url": "Dragma",
		"fb_name": "John Smith",
		"fb_uid": "759052697",
		"picture_url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/c2.0.64.64/p64x64/150981_10151409656362698_1573096695_n.jpg?efg=eyJpIjoibCJ9&oh=5193f524380e9ea12454d77b8a518762&oe=5A0894A2"
	}
]
```


### input = array of elements

`facebook-scrap.py user-search "search-results-array.json" -i json` => scrap user attributes from HTML block of a result from a search on Facebook :

```
{
	"fb_customized_url": "JohnJohn.Doe",
	"fb_name": "John-john Doe",
	"fb_uid": "100000016191070",
	"picture_url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/e15/q65/c0.13.64.64/p64x64/1920462_779525028724696_446426524_n.jpg?efg=eyJpIjoibCJ9&oh=f0ae9a0e5e743da1c1326144343da3f8&oe=59E1F6F1"
}
```
### input = dict array of elements

`facebook-scrap.py user-search "search-results-dicts.json" -i json --key="searched_user"` => scrap user attributes from HTML block of a result from a search on Facebook :

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
```

## Specify output (JSON to console, JSON file or CSV file)

- `facebook-scrap.py user-search "input/John%20Smith-8.html" "input/John%20Smith-9.html" --output=stdout` or `-o stdout` => serialized array of dicts to stdout (default)
- `facebook-scrap.py user-search "input/John%20Smith-8.html" "input/John%20Smith-9.html" --output=csv` or `-o csv` => save as a CSV file *not implemented yet*
- `facebook-scrap.py user-search "input/John%20Smith-8.html" "input/John%20Smith-9.html" --output=json` or `-o json` => save as a JSON file

# Code

## Contributing

This project adheres to the Contributor Covenant [code of conduct](code-of-conduct.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior to monkeydri@github.com.
