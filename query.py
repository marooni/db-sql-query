
import argparse
import warnings

import sqlalchemy
import pandas as pd
import numpy as np
import configparser
import os


def setupArgParser():

	parser = argparse.ArgumentParser()	
	parser.add_argument('sql_file', help='a text file containing the SQL statement to execute')
	parser.add_argument('--csv', default=False, action='store_true', help='Output the query result as csv')
	parser.add_argument('--noop', default=False, action='store_true', help='Do nothing, just print configuration and exit')
	return parser


def validateArguments():

	global sql_file
	if not os.path.isfile(sql_file):
		print('[error]: file not found: {0}'.format(sql_file))
		exit()


def readSqlStatement(sql_file):
	sql = ''
	with open(sql_file, 'r') as myfile:
		sql = myfile.read()

	sql = sql.replace('%', '%%')
	return sql


def executeSqlStatement(sql, connection):
	#with warnings.catch_warnings():
	#	warnings.simplefilter("ignore", category=Warning)
	df = pd.read_sql(sql, connection)
	return df


if __name__ == '__main__':

	# command-line options
	parser = setupArgParser()
	args = parser.parse_args()

	sql_file = args.sql_file	
	csv = args.csv
	noop = args.noop
	
	validateArguments()

	sql = readSqlStatement(sql_file)

	# read external configuration
	config = configparser.ConfigParser()
	config.read('config.ini')

	# exit if noop
	if noop:
		print('noop. Exiting.')
		exit()	

	# create database connection
	engine = sqlalchemy.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(config['DATABASE']['USER'], config['DATABASE']['PASS'], config['DATABASE']['HOST'], config['DATABASE']['PORT'], config['DATABASE']['NAME']))
	connection = engine.connect()

	# execute query
	data = executeSqlStatement(sql, connection)	
	if csv:		
		print(data.to_csv(sep=',', index=False))
	else:
		print(data)

