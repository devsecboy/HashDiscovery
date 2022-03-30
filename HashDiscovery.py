
from itertools import permutations
import argparse
from Algorithm.MD5HashAlgo import MD5HashAlgo

class HashDiscovery:
	def __init__(self):
		self.filePath=''
		self.secretsFilePath=''
		self.data=[]
		self.md5HashAlgo=MD5HashAlgo()
		self.oriHash=''
		self.saltCheck=False
		self.algorithm=''

	def IniializeVariable(self, filePath, secretsFilePath, oriHash, saltCheck, algorithm):
		self.filePath=filePath
		self.secretsFilePath=secretsFilePath
		self.oriHash=oriHash
		self.saltCheck=saltCheck
		self.algorithm=algorithm

	def create_cli_parser(self):
		self.parser = argparse.ArgumentParser(add_help=False, description="Hash Discovery")
		self.parser.add_argument('-h', '-?', '--h', '-help', '--help', action="store_true", help=argparse.SUPPRESS)
		input_options = self.parser.add_argument_group('Usage')
		input_options.add_argument('--file', metavar='FilePath', default="", help='File contains all value used in Hash Generator')
		input_options.add_argument('--secretsfile', metavar='SecretsFilePath', default="", help='File contains salts value to bruteforce')
		input_options.add_argument('--hash', metavar='HashValue', default="", help='Hash value to test against data')
		input_options.add_argument('--algorithm', metavar='Hashing Algorithm', default="", help='Hashing algorithm used')
		input_options.add_argument('--saltcheck', default=False, action='store_true', help='Test with salt value')
		args = self.parser.parse_args()
		return args

	def LoadFileDataInList(self):
		self.data=[]
		file=open(self.filePath, 'r')
		for line in file:
			self.data.append(line.strip())
		file.close()

	def BruteForceHashAndCompare(self):
		permData = permutations(self.data)
		bFound=False
		for i in list(permData):
			strData=''.join(i)
			if self.saltCheck:
				if self.SaltValueCheck(strData):
					bFound = True
					break
			else:
				if self.CompareGeneratedHash(strData):
					bFound = True
					break
		if not bFound:
			print ("\nNo hash found!\n")

	def SaltValueCheck(self, strData):
		file = open(self.secretsFilePath, 'r')
		bFound=False
		for line in file:
			if self.CompareGeneratedHash(line.strip()+strData):
				bFound = True
				break
			else:
				if self.CompareGeneratedHash(strData+line.strip()):
					bFound = True
					break
		file.close()
		return bFound

	def CompareGeneratedHash(self, strData):
		bFound=False
		hashVal=''
		print (strData)
		if self.algorithm == "md5":
			hashVal=self.md5HashAlgo.GenerateMD5Hash(strData)
		if hashVal == self.oriHash:
			print ("\nHash Found: \nData = {} \nHash = {}".format(strData, hashVal))
			bFound = True
		return bFound

if __name__ == "__main__":
	hashDiscovery=HashDiscovery()
	cli_parsed = hashDiscovery.create_cli_parser()
	hashDiscovery.IniializeVariable(cli_parsed.file, 
									cli_parsed.secretsfile,
									cli_parsed.hash,
									cli_parsed.saltcheck,
									cli_parsed.algorithm)
	hashDiscovery.LoadFileDataInList()
	hashDiscovery.BruteForceHashAndCompare()