import urllib.request, json, os.path


def JsonPostRequest(jsoncontent, url):
	req = urllib.request.Request(url)
	req.add_header('Content-Type', 'application/json; charset=utf-8')
	jsondata = json.dumps(jsoncontent)
	jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
	req.add_header('Content-Length', len(jsondataasbytes))
	return urllib.request.urlopen(req, jsondataasbytes)


def RegisterGame(port, game, gamedisplayname):
	print("Registering '%s'..." % gamedisplayname)

	event = {
	  "game": game,
	  "game_display_name": gamedisplayname
	}

	url = "http://127.0.0.1:"+str(port)+"/game_metadata"
	JsonPostRequest(event, url)


def RegisterEvent(event, port):
	print("Registering event...")
	url = "http://127.0.0.1:"+str(port)+"/register_game_event"
	JsonPostRequest(event, url)


def BindEvent(event, port):
	print("Binding event...")
	url = "http://127.0.0.1:"+str(port)+"/bind_game_event"
	JsonPostRequest(event, url)


def GameEvent(event, port):
	url = "http://127.0.0.1:"+str(port)+"/game_event"
	JsonPostRequest(event, url)


def RemoveEvent(port, game, eventname):
	print("Removing event '%s' for '%s'..." % (eventname, game))	
	event = {
	  "game": game,
	  "event": eventname
	}
	url = "http://127.0.0.1:"+str(port)+"/remove_game_event"
	JsonPostRequest(event, url)


def RemoveGame(port, game):
	print("Removing '%s'..." % game)
	event = {
	  "game": game
	}
	url = "http://127.0.0.1:"+str(port)+"/remove_game"
	JsonPostRequest(event, url)


def GetSSE3ListeningPort(corePropsPath='C:\\ProgramData\\SteelSeries\\SteelSeries Engine 3\\coreProps.json'):
	if os.path.isfile(corePropsPath):
		with open(corePropsPath) as f:
			data = json.load(f)

		addr = data["address"]
		addr.split(":")[1]

		return int(addr.split(":")[1])
	else:
		print("ERROR: File '%s' not found." % corePropsPath)
		return False


def BindHealthEvent(port, game, device_type, zone):
	HealthEvent = {
	  "game": game,
	  "event": "HEALTH",
	  "min_value": 0,
	  "max_value": 100,
	  "icon_id": 1,
	  "handlers": [
	    {
	      "device-type": device_type,
	      "zone": zone,
	      "color": { "gradient": {"zero": {"red": 255, "green": 0, "blue": 0},
                             "hundred": {"red": 0, "green": 255, "blue": 0} } },
	      "mode": "color"
	    }
	  ]
	}

	BindEvent(HealthEvent, port)


def Porcentaje(CurrentHealth, MaxHealth):	
	return (100*CurrentHealth)/MaxHealth