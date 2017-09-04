import argparse
import extractMetaData
import translateGPS
import re

def inputFile(img):
	file = open('extractGPSInfo.txt', 'r+')
	file.truncate()
	extractMetaData.getMetaData(img, 'extractGPSInfo.txt')
	return None

def getGPSInfo(infile):
	try:
		gps = 0
		with open(infile, 'r') as f:
			for line in f.readlines():
				if 'GPSInfo' in line:
					print("[+]GPS Information Found")
					gps = 1
					gpsInfo = re.findall(r'\(\d+, \d+\), \(\d+, \d+\), \(\d+, \d+\)', line)
					lat = str(gpsInfo[0]).split(', ')
					lon = str(gpsInfo[1]).split(', ')
					seprateCordinateInfo(lat, lon)
			if gps == 0:
				print("[-]No GPS Information Found...")
	except:
		print("[-]Image did not have information")

def seprateCordinateInfo(latitude, longitude):
	i = 0
	dest_lat = [] * 1
	dest_lon = [] * 1
	
	for x in latitude:
		if '(' in x:
			x = x.replace('(', '')
		if ')' in x:
			x = x.replace(')', '')
		if (i % 2) == 0:
			dest_lat.append(x)
		i += 1
	for x in longitude:
		if '(' in x:
			x = x.replace('(', '')
		if ')' in x:
			x = x.replace(')', '')
		if (i % 2) == 0:
			dest_lon.append(x)
		i += 1
	
	try:
		translateGPS.printCordinate(dest_lat, dest_lon)
	except:
		print("[-] Error with latitude and longitude")

def Main():
	parser = argparse.ArgumentParser()
	parser.add_argument("img", help ="Image to get GPS Co-Ordinates from")

	args = parser.parse_args()

	if args.img:
		print("[*]Gathering img info...")
		inputFile(str(args.img))
		print("[+]Info stored in 'extractGPSInfo.txt'...")
		getGPSInfo('extractGPSInfo.txt')
	else:
		print("[-]Image invalid!")

if __name__ == "__main__":
	Main()
