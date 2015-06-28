#!/usr/bin/python
"""Change the mouse sensitivity in Borderlands.

Usage:
python set_mouse_sensitivity.py [sensitivity]

profile.bin will be backed up at the start of the script.

If sensitivity is given, it should be a hexadecimal value between
00 and ff, giving the sensitivity that you want to set the mouse to.
If no sensitivity is given, the program will prompt you for one.
"""

import binascii
import datetime
import hashlib
import os
import shutil
import sys

profile_path = "profile.bin"

class InvalidProfileException(Exception):
	pass

class ProfileData(object):
	"""The data in the Borderlands profile.bin file."""
	def __init__(self, data):
		# Which byte in the data contains the mouse sensitivity.
		self._mouse_sensitivity_offset = 0x9e
		self._data = data
		
		# Check that the data is valid.
		
		# Length.
		if len(data) != 197:
			raise InvalidProfileException(
				"Incorrect file length. If your mouse sensitivity is set to minimum, please increase it, then return to the main menu and try again.")
		
		# Check the SHA-1 hash at the start of the file is correct.
		hash = hashlib.sha1(data[20:])
		if hash.digest() != data[:20]:
			raise InvalidProfileException(
				"Expected SHA-1 hash {}, found {}.".format(
					hash.hexdigest(), binascii.hexlify(data[:20])))
		
	def __str__(self):
		return str(self._data)
		
	def set_hash(self):
		hash = hashlib.sha1(self._data[20:])
		self._data[:20] = hash.digest()
		
	def get_mouse_sensitivity(self):
		return self._data[self._mouse_sensitivity_offset]
		
	def set_mouse_sensitivity(self, sensitivity):
		self._data[self._mouse_sensitivity_offset] = sensitivity
		self.set_hash()

def get_desired_sensitivity(current_sensitivity):
	"""Get the desired mouse sensitivity."""
	sensitivity_str = ""
	sensitivity = None
	if len(sys.argv) > 1:
		sensitivity_str = sys.argv[1]
	
	while True:
		try:
			sensitivity = int(sensitivity_str, 16)
		except ValueError:
			print("Invalid sensitivity: {}".format(sensitivity_str))
		
		if sensitivity is not None:
			break
			
		print("Please enter a desired mouse sensitivity in hexadecimal")
		sensitivity_str = raw_input("between 0 and ff (current: {:x}):".format(
			current_sensitivity))
	
	return sensitivity

def backup_profile():
	"""Backup the profile file to the same directory."""
	if not os.path.isfile(profile_path):
		print("Could not find file {}.".format(profile_path))
		print("Please make sure this script is in the Borderlands save directory. e.g:")
		print(r"D:\Users\somebody\Documents\my games\borderlands\savedata")
		exit(1)
		
	backup_path = "{}.{:%Y%m%d-%H%M%S}.bak".format(profile_path, datetime.datetime.now())
	shutil.copyfile(profile_path, backup_path)
	print("Backed up {} to {}.".format(profile_path, backup_path))

def get_profile_data():
	"""Return (ProfileData) the contents of the profile file."""
	with open(profile_path, 'rb') as profile_file:
		contents = bytearray(profile_file.read())
	
	try:
		data = ProfileData(contents)
	except InvalidProfileException as e:
		print("Invalid profile data: " + e.message)
		print("If there has been an update to Borderlands, this script may no longer work.")
		exit(1)
	
	return data

def set_profile_data(data):
	"""Set the contents of the profile file."""
	with open(profile_path, 'wb') as profile_file:
		profile_file.write(data)

def main():
	backup_profile()
	profile_data = get_profile_data()
	new_sensitivity = get_desired_sensitivity(profile_data.get_mouse_sensitivity())
	profile_data.set_mouse_sensitivity(new_sensitivity)
	set_profile_data(str(profile_data))
	print("")
	print("Finished.")
	print("Please restart Borderlands for the change to take effect.")

if __name__ == "__main__":
	main()
