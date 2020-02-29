#!/usr/bin/python

import getpass
import re

class Config_Generator(object):
	def __init__(self):
		# private ones
		self.__ready_to_write = False
		self.__OUTFILE_NAME = 'db_config_[***whateveryoulike***].php'
		self.__CONFIG_CORE_NAME = 'db_config_core.php'

		# list indices
		self.__INDEX_HOST		= 0
		self.__INDEX_USER		= 1
		self.__INDEX_PASSWORD	= 2
		self.__INDEX_DATABASE	= 3
		self.__INDEX_CLASS_NAME	= 4

		# input prompts
		self.__PROMPTS = [
    		"host: ",
    		"user: ",
    		"password: ",
    		"database: ",
			"class name: "
		]

		# database credential
		self.__credential = []

		self.__CONF_FORMAT = """<?php
	namespace DB_Config {
		define('JUGEMU_JUGEMU_GOGO_NO_SURIKIRE', 'JUGEMU_JUGEMU_GOGO_NO_SURIKIRE');
		include_once('./db_config_core.php');

		class %s extends DB_Config_Core {

			private const DB_CREDENTIAL = array(
				'host' => %s,
				'user' => %s,
				'password' => %s,
				'database' => %s
			);

			private function __construct() {
			}

			public static function get_db_credential() {
				return parent::return_db_credential(self::DB_CREDENTIAL);
			}
		}
	}
?>"""

		self.__DB_CONF_CORE = """<?php
	namespace DB_Config {
		/***** turn off the comment as required
		 * if (!defined('JUGEMU_JUGEMU_GOGO_NO_SURIKIRE')) {
		 *	header('Location: 404');
		 * }
		*****/

		abstract class DB_Config_Core {

			public static function return_db_credential($credential) {
				return $credential;
			}
		}

	}
?>
"""

	def get_db_credential(self):

		print ("\nEnter the database credential\n")

		for index in range(0, len(self.__PROMPTS)):
			prompt = self.__PROMPTS[index]

			if index == self.__INDEX_PASSWORD:
				value = getpass.getpass(prompt)

			elif index == self.__INDEX_CLASS_NAME:
				value = self.get_class_name(prompt)

			else:
				value = input(prompt)

			if index != self.__INDEX_CLASS_NAME:
				if value != "":
					value = "'" + value + "'"
				else:
					value = 'null'

			self.__credential.append(value)

		return


	def get_confirmation (self):
		divide_char = "="
		print("\n%s DB Credential %s\n" % ((divide_char[:1] * 15),  (divide_char[:1] * 15)))

		for index in range(0, len(self.__credential)):
			value = self.__credential[index]

			if index == self.__INDEX_PASSWORD:
				value = self.mask_password(value)

			print ("    %s: %s" % (self.__PROMPTS[index], value))

		print ("\n%s\n" % (divide_char[:1] * 45))

		response = input("Correct? (y/n): ")

		if response.strip().lower() == "y":
			self.__ready_to_write = True


	def mask_password(self, pwd):
		masked = ""

		for index in range(0, len(pwd)):
			if index % 2 == 1:
				masked = masked + "*"
			else:
				masked = masked + pwd[index]

		return masked

	# be aware that this does not check for PHP reserved words
	def get_class_name(self, prompt):
		valid_class_name = False
		pattern = re.compile(r"^[a-zA-Z][a-zA-Z1-9_]*$")

		print ("\n*** You can name the class which will be defined in the config file *** \n\n")

		while valid_class_name == False:
			value = input(prompt)

			if pattern.match(value):
				valid_class_name = True
			else:
				print ('invalid class name "%s"\n' % value)

		return value


	def generate_conf_file(self):
		with open(self.__OUTFILE_NAME, "w") as outf:
			outf.write(self.__CONF_FORMAT % (self.__credential[self.__INDEX_CLASS_NAME], self.__credential[self.__INDEX_HOST], self.__credential[self.__INDEX_USER], self.__credential[self.__INDEX_PASSWORD], self.__credential[self.__INDEX_DATABASE]));

		print("db config file generated.\n");

		want_core = input("By the way ... do you wish a config core file (db_config_core.php)? (y/n): ").lower()

		if want_core == 'y':
			with open(self.__CONFIG_CORE_NAME, "w") as outf:
				outf.write(self.__DB_CONF_CORE)
			print("config core file generated")



	def is_ready(self):
		return self.__ready_to_write


if __name__ == "__main__":

	cg = Config_Generator()

	while (cg.is_ready() == False):
		cg.get_db_credential()
		cg.get_confirmation()

	cg.generate_conf_file();


