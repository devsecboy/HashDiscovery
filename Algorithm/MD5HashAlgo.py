
# Python 3 code to demonstrate the 
# working of MD5 (string - hexadecimal)
  
import hashlib
 
class MD5HashAlgo(object):
	def GenerateMD5Hash(self, data):
		return hashlib.md5(data.encode('utf-8')).hexdigest()