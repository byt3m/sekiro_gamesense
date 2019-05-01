import time, os
from funciones import *
from memory import *


GAME = "SEKIRO"
GAME_DISPLAY = "Sekiro Shadows Die Twice"
DEVICE_TYPE = "keyboard"
ZONE = "main-keyboard"
EVENT = "HEALTH"


SSE3_PORT = GetSSE3ListeningPort()
if not SSE3_PORT:
	print("ERROR: the script was not able to retrieve the Steel Series Engine game sense listening port.")
	os.system("pause")
	exit(1)

# Registering game and binding the health event for displaying health in the keyboard.
#RegisterGame(SSE3_PORT, GAME, GAME_DISPLAY)
#BindHealthEvent(SSE3_PORT, GAME, DEVICE_TYPE, ZONE)
#RemoveGame(SSE3_PORT, GAME)


# Prepare and send game events
m = Memory()

process = "sekiro.exe"

# Getting Base Address
pyHandle = m.GetProcessHandle(process, 1)
modulos = m.EnumModules(pyHandle)
BaseAddress = modulos[0]

# Health
HealthAddr = 0x3B7A2A4 + BaseAddress

# Getting handle for reading and writting
cHandle = m.GetProcessHandle(process, 0)

Health = m.Read_UINT64(cHandle, HealthAddr)
MaxHealth = Health


while True:

	os.system("cls")

	health = int(Porcentaje(m.Read_UINT64(cHandle, HealthAddr), MaxHealth))

	print("Health: %s" % health)

	EventData = {
	"game": GAME,
	"event": EVENT,
	"data": {
	  "value": health
	  }
	}

	GameEvent(EventData, SSE3_PORT)

	health -= 1

	if health < 0:
		print("Game Over.")		

	time.sleep(0.6)