from requests import get, post, delete, put
from datetime import datetime
from flask_app import app


start = datetime.now()

URL = "http://localhost:5000"
USERNAME = app.config["INITIAL_USERS"]["admin"]["username"]
PASSWORD = app.config["INITIAL_USERS"]["admin"]["password"]
HEADERS = {"Accept":"application/json","Content-Type":"application/json"}

######## LOGIN ########

session = post("{}/login/".format(URL), json={
    "username":USERNAME,
    "password":PASSWORD
}).cookies["session"]
cookies = {"session":session}

######## REFEREE ########

cunha = post("{}/api/referee/".format(URL), json={
	"name": "Andres",
	"surname": "Cunha"
}, cookies=cookies).json()

######## MANAGERS ########

river = post("{}/api/club/".format(URL), json={
	"name": "Club Atletico River Plate",
	"stadium": "Estadio Monumental",
	"city": "Ciudad de Buenos Aires"
}, cookies=cookies).json()

boca = post("{}/api/club/".format(URL), json={
	"name": "Club Atletico Boca Juniors",
	"stadium": "La Bombonera",
	"city": "Ciudad de Buenos Aires"
}, cookies=cookies).json()

######## CLUBS ########

gallardo = post("{}/api/manager/".format(URL), json={
	"name": "Marcelo",
	"surname": "Gallardo",
	"club": river["id"]
}, cookies=cookies).json()

schelotto = post("{}/api/manager/".format(URL), json={
	"name": "Guillermo",
	"surname": "Barros Schelotto",
	"club": boca["id"]
}, cookies=cookies).json()

######## RIVER PLAYERS ########

armani = post("{}/api/player/".format(URL), json={
	"name": "Franco",
	"surname": "Armani",
	"position": "GOALKEEPER"
}, cookies=cookies).json()

montiel = post("{}/api/player/".format(URL), json={
	"name": "Gonzalo",
	"surname": "Montiel",
	"position": "DEFENSE"
}, cookies=cookies).json()

maidana = post("{}/api/player/".format(URL), json={
	"name": "Jonatan",
	"surname": "Maidana",
	"position": "DEFENSE"
}, cookies=cookies).json()

pinola = post("{}/api/player/".format(URL), json={
	"name": "Javier",
	"surname": "Pinola",
	"position": "DEFENSE"
}, cookies=cookies).json()

casco = post("{}/api/player/".format(URL), json={
	"name": "Milton",
	"surname": "Casco",
	"position": "DEFENSE"
}, cookies=cookies).json()

enzo = post("{}/api/player/".format(URL), json={
	"name": "Enzo",
	"surname": "Perez",
	"position": "MIDFIELDER"
}, cookies=cookies).json()

ponzio = post("{}/api/player/".format(URL), json={
	"name": "Leonardo",
	"surname": "Ponzio",
	"position": "MIDFIELDER"
}, cookies=cookies).json()

nacho = post("{}/api/player/".format(URL), json={
	"name": "Ignacio",
	"surname": "Fernandez",
	"position": "MIDFIELDER"
}, cookies=cookies).json()

palacios = post("{}/api/player/".format(URL), json={
	"name": "Exequiel",
	"surname": "Palacios",
	"position": "MIDFIELDER"
}, cookies=cookies).json()

pity = post("{}/api/player/".format(URL), json={
	"name": "Gonzalo",
	"surname": "Martinez",
	"position": "MIDFIELDER"
}, cookies=cookies).json()

pratto = post("{}/api/player/".format(URL), json={
	"name": "Lucas",
	"surname": "Pratto",
	"position": "FORWARD"
}, cookies=cookies).json()

lux = post("{}/api/player/".format(URL), json={
	"name": "German",
	"surname": "Lux",
	"position": "GOALKEEPER"
}, cookies=cookies).json()

quarta = post("{}/api/player/".format(URL), json={
	"name": "Lucas",
	"surname": "Martinez Quarta",
	"position": "DEFENSE"
}, cookies=cookies).json()

zuculini = post("{}/api/player/".format(URL), json={
	"name": "Bruno",
	"surname": "Zuculini",
	"position": "MIDFIELDER"
}, cookies=cookies).json()

quintero = post("{}/api/player/".format(URL), json={
	"name": "Juan Fernando",
	"surname": "Quintero",
	"position": "FORWARD"
}, cookies=cookies).json()

mayada = post("{}/api/player/".format(URL), json={
	"name": "Camilo",
	"surname": "Mayada",
	"position": "MIDFIELDER"
}, cookies=cookies).json()

mora = post("{}/api/player/".format(URL), json={
	"name": "Rodrigo",
	"surname": "Mora",
	"position": "FORWARD"
}, cookies=cookies).json()


alvarez = post("{}/api/player/".format(URL), json={
	"name": "Julian",
	"surname": "Alvarez",
	"position": "FORWARD"
}, cookies=cookies).json()

borre = post("{}/api/player/".format(URL), json={
	"name": "Rafael",
	"surname": "Santos Borre",
	"position": "FORWARD"
}, cookies=cookies).json()

put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], armani["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], montiel["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], maidana["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], pinola["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], casco["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], enzo["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], ponzio["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], nacho["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], palacios["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], pity["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], pratto["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], lux["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], quarta["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], zuculini["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], quintero["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], mayada["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], mora["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], alvarez["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, river["id"], borre["id"]), cookies=cookies)

######## BOCA PLAYERS ########

andrada = post("{}/api/player/".format(URL), json={
	"name": "Esteban",
	"surname": "Andrada",
	"position": "GOALKEEPER"
}, cookies=cookies).json()

buffarini = post("{}/api/player/".format(URL), json={
	"name": "Julio",
	"surname": "Buffarini",
	"position": "DEFENSE"
}, cookies=cookies).json()

izquierdoz = post("{}/api/player/".format(URL), json={
	"name": "Carlos",
	"surname": "Izquierdoz",
	"position": "DEFENSE"
}, cookies=cookies).json()

magallan = post("{}/api/player/".format(URL), json={
	"name": "Lisandro",
	"surname": "Magallan",
	"position": "DEFENSE"
}, cookies=cookies).json()

olaza = post("{}/api/player/".format(URL), json={
	"name": "Lucas",
	"surname": "Olaza",
	"position": "DEFENSE"
}, cookies=cookies).json()

nandez = post("{}/api/player/".format(URL), json={
	"name": "Nahitan",
	"surname": "Nandez",
	"position": "MIDFIELDER"
}, cookies=cookies).json()

barrios = post("{}/api/player/".format(URL), json={
	"name": "Wilmar",
	"surname": "Barrios",
	"position": "MIDFIELDER"
}, cookies=cookies).json()

perez = post("{}/api/player/".format(URL), json={
	"name": "Pablo",
	"surname": "Perez",
	"position": "MIDFIELDER"
}, cookies=cookies).json()

villa = post("{}/api/player/".format(URL), json={
	"name": "Sebastian",
	"surname": "Villa",
	"position": "MIDFIELDER"
}, cookies=cookies).json()

benedetto = post("{}/api/player/".format(URL), json={
	"name": "Dario",
	"surname": "Benedetto",
	"position": "FORWARD"
}, cookies=cookies).json()

pavon = post("{}/api/player/".format(URL), json={
	"name": "Cristian",
	"surname": "Pavon",
	"position": "MIDFIELDER"
}, cookies=cookies).json()

rossi = post("{}/api/player/".format(URL), json={
	"name": "Agustin",
	"surname": "Rossi",
	"position": "GOALKEEPER"
}, cookies=cookies).json()

goltz = post("{}/api/player/".format(URL), json={
	"name": "Paolo",
	"surname": "Goltz",
	"position": "DEFENSE"
}, cookies=cookies).json()

jara = post("{}/api/player/".format(URL), json={
	"name": "Leonardo",
	"surname": "Jara",
	"position": "DEFENSE"
}, cookies=cookies).json()

gago = post("{}/api/player/".format(URL), json={
	"name": "Fernando",
	"surname": "Gago",
	"position": "MIDFIELDER"
}, cookies=cookies).json()

wanchope = post("{}/api/player/".format(URL), json={
	"name": "Ramon",
	"surname": "Abila",
	"position": "FORWARD"
}, cookies=cookies).json()

zarate = post("{}/api/player/".format(URL), json={
	"name": "Mauro",
	"surname": "Zarate",
	"position": "FORWARD"
}, cookies=cookies).json()

tevez = post("{}/api/player/".format(URL), json={
	"name": "Carlos",
	"surname": "Tevez",
	"position": "FORWARD"
}, cookies=cookies).json()

put("{}/api/club/{}/addplayer/{}/".format(URL, boca["id"], andrada["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, boca["id"], buffarini["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, boca["id"], izquierdoz["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, boca["id"], magallan["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, boca["id"], olaza["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, boca["id"], nandez["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, boca["id"], barrios["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, boca["id"], perez["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, boca["id"], villa["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, boca["id"], benedetto["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, boca["id"], pavon["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, boca["id"], rossi["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, boca["id"], goltz["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, boca["id"], jara["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, boca["id"], gago["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, boca["id"], wanchope["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, boca["id"], zarate["id"]), cookies=cookies)
put("{}/api/club/{}/addplayer/{}/".format(URL, boca["id"], tevez["id"]), cookies=cookies)

######## TEAMS ########

riverTeam = post("{}/api/team/".format(URL), json={
	"club": river["id"],
	"manager": gallardo["id"],
	"titulars": [
        armani["id"],
        montiel["id"],
        maidana["id"],
        pinola["id"],
        casco["id"],
        enzo["id"],
        ponzio["id"],
        nacho["id"],
        palacios["id"],
        pity["id"],
        pratto["id"]
        ],
	"substitutes": [
        lux["id"],
        quarta["id"],
        zuculini["id"],
        quintero["id"],
        mayada["id"],
        mora["id"],
        alvarez["id"]
        ]
}, cookies=cookies).json()


bocaTeam = post("{}/api/team/".format(URL), json={
	"club": boca["id"],
	"manager": schelotto["id"],
	"titulars": [
        andrada["id"],
        buffarini["id"],
        izquierdoz["id"],
        magallan["id"],
        olaza["id"],
        nandez["id"],
        barrios["id"],
        perez["id"],
        villa["id"],
        benedetto["id"],
        pavon["id"]
        ],
	"substitutes": [
        rossi["id"],
        goltz["id"],
        jara["id"],
        gago["id"],
        wanchope["id"],
        zarate["id"],
        tevez["id"]
        ]
}, cookies=cookies).json()


######## MATCH ########

match = post("{}/api/match/".format(URL), json={
	"teamA": riverTeam["id"],
	"teamB": bocaTeam["id"],
	"dateOfStart": "2018/12/09 16:40:00",
	"referee": cunha["id"]
}, cookies=cookies).json()

######## EVENTS ########

def matchmoment(timestamp, momenttype):
	post("{}/api/match/{}/events/{}/matchmoment/".format(URL, match["id"], timestamp), json={
		"momentType": momenttype
	}, cookies=cookies)

def foul(timestamp, punishment, foultype, perpetrator, victim=None):
	data = {
		"punishment": punishment,
		"foulType": foultype,
		"perpetrator_id": perpetrator["id"]		
	}
	if victim:
		data["victim_id"] = victim["id"]
	post("{}/api/match/{}/events/{}/foul/".format(URL, match["id"], timestamp), cookies=cookies,
		 json=data)

def ongoal(timestamp, shooter, goalkeeper, goal, penalty, assist=None):
	data = {
		"shooter_id": shooter["id"],
		"goalkeeper_id": goalkeeper["id"],
		"goal": goal,
		"penalty": penalty
	}
	if assist:
		data["assist_id"] = assist["id"]
	post("{}/api/match/{}/events/{}/ongoal/".format(URL, match["id"], timestamp), cookies=cookies,
		 json=data)

def highlight(timestamp, description, players):
	post("{}/api/match/{}/events/{}/highlight/".format(URL, match["id"],timestamp), json={
		"description": description,
		"players": [player["id"] for player in players]
	}, cookies=cookies)

def restart(timestamp, restarttype, executor):
	post("{}/api/match/{}/events/{}/restart/".format(URL, match["id"], timestamp), json={
		"restartType": restarttype,
		"executor_id": executor["id"]
	}, cookies=cookies)

def substitution(timestamp, playerOut, playerIn):
	post("{}/api/match/{}/events/{}/substitution/".format(URL, match["id"], timestamp), json={
		"inPlayer_id": playerIn["id"],
		"outPlayer_id": playerOut["id"]
	}, cookies=cookies)

def injury(timestamp, player, severity):
	post("{}/api/match/{}/events/{}/injury/".format(URL, match["id"], timestamp), json={
		"injured_id": player["id"],
		"severity": severity
	}, cookies=cookies)


if True:
	matchmoment("0:00","FIRSTTIMESTART")

	foul("0:41","WARNING","VIOLENTKICK",pratto,victim=perez)

	restart("1:34","FREEKICK",magallan)

	foul("2:30","WARNING","VIOLENTKICK",magallan, victim=nacho)

	restart("3:22","FREEKICK",pity)

	restart("4:07","CORNER",pity)

	restart("4:47","GOALKICK",andrada)

	restart("5:09","THROWIN",olaza)

	restart("5:47","THROWIN",olaza)

	foul("6:18","WARNING","VIOLENTKICK",perez, victim=nacho)

	restart("6:45","FREEKICK",enzo)

	restart("7:50","THROWIN",montiel)

	ongoal("9:18",nandez,armani,False, False)

	restart("10:03","CORNER", villa)

	ongoal("10:06",perez,armani,False, False)

	restart("11:43","THROWIN",montiel)

	restart("12:11","THROWIN",buffarini)

	foul("13:00","WARNING","CHARGEPLAYER",pity, victim=buffarini)

	restart("13:50","THROWIN",maidana)

	restart("14:50","THROWIN",buffarini)

	foul("15:14","YELLOW","VIOLENTKICK",buffarini, victim=pity)

	restart("15:55","FREEKICK",nacho)

	restart("16:32","GOALKICK",andrada)

	restart("17:45","THROWIN",casco)

	restart("18:05","THROWIN",montiel)

	restart("19:10","CORNER", pity)

	ongoal("19:11",nacho,andrada,False, False,assist=pity)

	restart("19:44","GOALKICK",andrada)

	foul("19:50","WARNING","VIOLENTKICK",enzo, victim=perez)

	foul("20:40","WARNING","VIOLENTKICK",pity, victim=perez)

	foul("20:40","WARNING","VIOLENTKICK",perez, victim=pity)

	restart("20:55","FREEKICK",villa)

	ongoal("20:55",villa,armani,False, False)

	ongoal("21:01",nandez,armani,False, False, assist=pavon)

	restart("21:29","CORNER", villa)

	restart("21:45","GOALKICK",armani)

	highlight("22:12","Caño",[villa])

	foul("22:13","WARNING","VIOLENTKICK",maidana, victim=villa)

	restart("23:00","FREEKICK",villa)

	restart("23:39","GOALKICK",armani)

	foul("24:53","WARNING","VIOLENTKICK",nacho, victim=villa)

	restart("25:30","FREEKICK",magallan)

	restart("25:30","THROWIN",olaza)

	foul("26:41","YELLOW","VIOLENTKICK",ponzio, victim=nandez)

	restart("29:38","FREEKICK",benedetto)

	ongoal("29:39",perez,armani,False, False, assist=benedetto)

	restart("31:26","CORNER", pity)

	foul("31:27","WARNING","CHARGEPLAYER",pinola, victim=izquierdoz)

	foul("32:33","WARNING","OFFSIDE",villa)

	restart("32:22","FREEKICK",pinola)

	restart("32:53","THROWIN",buffarini)

	foul("33:27","WARNING","VIOLENTKICK",pity, victim=nandez)

	restart("33:33","FREEKICK",barrios)

	restart("34:51","THROWIN",ponzio)

	restart("36:22","GOALKICK",andrada)

	restart("36:44","THROWIN",montiel)

	restart("37:15","THROWIN",olaza)

	foul("37:24","WARNING","HAND",perez)

	restart("37:28","FREEKICK",ponzio)

	foul("38:10","WARNING","CHARGEPLAYER",pavon, victim=enzo)

	ongoal("38:19",benedetto,armani,False, False, assist=villa)

	ongoal("39:55",pity, andrada,False, False, assist=montiel)

	foul("41:03","WARNING","CHARGEPLAYER",pratto, victim=magallan)

	restart("41:35","FREEKICK",magallan)

	foul("41:58","YELLOW","VIOLENTKICK",perez, victim=enzo)

	restart("42:55","FREEKICK",montiel)

	ongoal("43:21",benedetto,armani,True, False, assist=nandez)

	restart("44:38","KICKOFF",nacho)

	foul("44:53","NONE","VIOLENTKICK",pinola, victim=nandez)

	restart("45+0:45","THROWIN",montiel)

	restart("45+1:57","CORNER",pity)

	matchmoment("45+2:14","FIRSTTIMEEND")

	matchmoment("45:00","SECONTIMESTART")

	restart("45:00","KICKOFF",benedetto)

	restart("45:20","THROWIN",olaza)

	restart("46:29","CORNER",pity)

	ongoal("46:31",maidana,andrada,False, False,assist=pity)

	restart("47:04","GOALKICK",andrada)

	restart("47:27","THROWIN",buffarini)

	foul("48:00","WARNING","VIOLENTKICK",pavon, victim=montiel)

	restart("48:04","FREEKICK",montiel)

	ongoal("48:20",nacho,andrada,False, False,assist=pratto)

	restart("48:50","GOALKICK",andrada)

	restart("50:31","THROWIN",buffarini)

	ongoal("51:22",palacios,andrada,False, False,assist=pity)

	foul("51:55","WARNING","VIOLENTKICK",casco, victim=nandez)

	restart("52:20","FREEKICK", buffarini)

	foul("52:24","WARNING","HAND",pinola)

	restart("54:04","FREEKICK",olaza)

	ongoal("55:02",pratto,andrada,False, False,assist=nacho)

	highlight("55:02","Penal no cobrado, Andrada cargó contra Pratto en una oportunidad clara de gol.",[andrada,pratto])

	foul("55:02","WARNING","CHARGEPLAYER",pratto, victim=andrada)

	substitution("57:51",ponzio,quintero)

	restart("58:16","GOALKICK",andrada)

	foul("58:49","WARNING","CHARGEPLAYER",barrios, victim=palacios)

	restart("59:30","GOALKICK",andrada)

	restart("60:25","CORNER",pity)

	foul("60:26","WARNING","CHARGEPLAYER",pinola, victim=izquierdoz)

	substitution("61:47",benedetto,wanchope)

	restart("62:01","GOALKICK",andrada)

	restart("63:08","GOALKICK",andrada)

	restart("64:45","GOALKICK",andrada)

	ongoal("65:06",pratto,andrada,False, False,assist=casco)

	restart("65:18","GOALKICK",andrada)

	foul("65:29","WARNING","CHARGEPLAYER",wanchope, victim=pinola)

	restart("65:30","FREEKICK",maidana)

	ongoal("67:22",pratto,andrada,True, False,assist=nacho)

	restart("68:05","KICKOFF",pavon)

	foul("69:26","WARNING","VIOLENTKICK",pity,victim=buffarini)

	restart("69:52","FREEKICK",andrada)

	restart("70:26","THROWIN",casco)

	restart("71:08","THROWIN",olaza)

	restart("71:40","GOALKICK",armani)

	foul("72:29","WARNING","VIOLENTKICK",nacho,victim=barrios)

	substitution("72:44",montiel,mayada)

	restart("73:15","FREEKICK",izquierdoz)

	foul("74:07","WARNING","VIOLENTKICK",pratto,victim=barrios)

	restart("74:35","FREEKICK",magallan)

	restart("75:16","THROWIN",casco)

	foul("76:04","WARNING","HAND",pity)

	restart("76:16","FREEKICK",izquierdoz)

	restart("76:44","CORNER",buffarini)

	foul("77:15","WARNING","OTHERVIOLENCE",pinola,victim=nandez)

	restart("79:57","FREEKICK",olaza)

	foul("80:16","YELLOW","VIOLENTKICK",nacho,victim=nandez)

	restart("81:27","FREEKICK",villa)

	foul("82:29","YELLOW","VIOLENTKICK",maidana,victim=wanchope)

	restart("83:04","THROWIN",olaza)

	restart("83:29","THROWIN",mayada)

	restart("84:15","THROWIN",casco)

	restart("85:30","GOALKICK",armani)

	foul("86:13","WARNING","CHARGEPLAYER",barrios, victim=pity)

	injury("86:40",nacho,"MED")

	foul("87:41","WARNING","CHARGEPLAYER",pity, victim=nandez)

	restart("88:17","FREEKICK",izquierdoz)

	substitution("88:37",perez,gago)

	restart("89:20","THROWIN",buffarini)

	restart("89:44","THROWIN",casco)

	foul("90+0:40","WARNING","VIOLENTKICK",palacios,victim=buffarini)

	restart("90+1:11","FREEKICK",izquierdoz)

	injury("90+2:10",nandez,"HIG")

	matchmoment("90+5:16","SECONTIMEEND")

	matchmoment("90:00","FIRSTEXTRASTART")

	restart("90:00","KICKOFF",wanchope)

	foul("91:42","YELLOW","VIOLENTKICK",barrios,victim=palacios)

	restart("93:24","FREEKICK",pinola)

	substitution("95:04",villa,jara)

	restart("95:51","THROWIN",buffarini)

	substitution("96:47",palacios,alvarez)

	restart("97:12","GOALKICK",andrada)

	restart("98:09","CORNER",pity)

	injury("98:20",andrada,"LOW")

	injury("98:21",buffarini,"LOW")

	restart("99:45","GOALKICK",andrada)

	restart("101:14","GOALKICK",andrada)

	ongoal("101:56",alvarez,andrada,False,False,assist=pity)

	restart("102:30","GOALKICK",andrada)

	ongoal("103:01",pratto,andrada,False,False,assist=mayada)

	restart("103:20","CORNER",quintero)

	restart("103:55","GOALKICK",andrada)

	restart("104:12","THROWIN",pinola)

	foul("104:58","WARNING","CHARGEPLAYER",quintero,gago)

	restart("105+0:27","GOALKICK",andrada)

	injury("105+0:45",enzo,"LOW")

	restart("105+0:48","THROWIN",olaza)

	matchmoment("105+1:05","SECONEXTRASTART")

	matchmoment("105:00","FIRSTEXTRAEND")

	restart("105:00","KICKOFF",nacho)

	restart("105:37","THROWIN",casco)

	restart("106:25","THROWIN",casco)

	injury("106:58",wanchope,"LOW")

	restart("107:24","THROWIN",mayada)

	ongoal("108:06",quintero,andrada,True,False,assist=mayada)

	restart("109:20","KICKOFF",wanchope)

	ongoal("109:38",wanchope,armani,False,False,assist=buffarini)

	substitution("110:14",nacho,zuculini)

	substitution("110:14",buffarini,tevez)

	restart("110:57","THROWIN",olaza)

	injury("111:42",armani,"LOW")

	restart("112:54","GOALKICK",armani)

	restart("113:42","THROWIN",olaza)

	restart("114:15","CORNER",izquierdoz)

	restart("114:35","CORNER",pavon)

	ongoal("114:54",wanchope,armani,False,False,assist=jara)

	ongoal("115:01",gago,armani,False,False,assist=pavon)

	ongoal("115:37",alvarez,andrada,False,False,assist=pity)

	restart("115:55","THROWIN",casco)

	injury("116:24",gago,"HIG")

	ongoal("116:27",alvarez,andrada,False,False)

	restart("117:02","THROWIN",olaza)

	injury("118:00",pratto,"LOW")

	injury("118:00",pity,"LOW")

	restart("118:04","THROWIN",olaza)

	restart("118:35","GOALKICK",andrada)

	restart("119:24","THROWIN", mayada)

	ongoal("119:46",jara,armani,False,False,assist=tevez)

	foul("120+0:38","YELLOW","OTHERVIOLENCE",tevez,victim=casco)
	
	foul("120+0:38","YELLOW","OTHERVIOLENCE",casco,victim=tevez)

	restart("120+1:05","CORNER", pavon)

	highlight("120+1:11","El taco no..., hace la personal y ahí se va, se va.", [quintero, pity])

	ongoal("120+1:20",pity,andrada,True,False,assist=quintero)

	matchmoment("120+2:10","SECONEXTRAEND")

end = datetime.now()
diff = end-start
print("Complete match upload in {},{} seconds".format(diff.seconds,diff.microseconds//1000))