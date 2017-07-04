#!/usr/bin/env python

import json

def output_result(results, output_type):
	if output_type == "stdout":
		print json.dumps(results)
	elif output_type == "pretty":
		print json.dumps(results, indent=4, sort_keys=True, ensure_ascii=False, encoding="utf-8")
	elif output_type == "json":
		with open("output.json", 'w+') as output_file:
			json.dump(results, output_file)
	elif output_type == "csv":
		#TODO : write to CSV file
		pass
	else:
		assert False, "unhandled output type : " + output_type