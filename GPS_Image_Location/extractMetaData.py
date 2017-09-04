import argparse
from PIL import Image
from PIL.ExifTags import TAGS

def getMetaData(imgName, out):
	try:
		metaData = {}

		imgFile = Image.open(imgName)
		info = imgFile._getexif()

		if info:
			print("[+]Found Meta Data...")
			for (tag, value) in info.items():
				tagname = TAGS.get(tag, tag)
				metaData[tagname] = value
				if not out:
					print(tagname, value)
			if out:
				with open(out, 'w') as outFile:
					for (tagname, value) in metaData.items():
						outFile.write(str(tagname) + "\t" +\
									  str(value) + "\n")

	except:
		print("[-]Image info not found...")
		exit(0)

def Main():
	parser = argparse.ArgumentParser()
	parser.add_argument("img", help="Name of image File")
	parser.add_argument("--output", "-o", help="dump data out to file")

	args = parser.parse_args()
	if args.img:
		getMetaData(args.img, args.output)
	else:
		print("/****************USUAGE******************/")
		print(parser.usage)
		print("/****************USUAGE******************/")
	

if __name__ == "__main__":
	Main()
