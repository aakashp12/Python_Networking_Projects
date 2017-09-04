def printCordinate(lat, lon):
	if lat and lon:
		dLat = int(lat[0]) + (int(lat[1])/60.0) + (int(lat[2])/3600.0)
		dLon = int(lon[0]) + (int(lon[1])/60.0) + (int(lon[2])/3600.0)
		print("[+]Image was taken from: ("+str(dLat)+", "+str(dLon)+")")
