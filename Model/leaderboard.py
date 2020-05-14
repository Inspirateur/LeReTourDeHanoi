import json


def dif(isHard):
	return "Insane" if isHard else "Normal"


def readFile():
	try:
		with open(f"leaderboard.txt", "r") as flead:
			return json.load(flead)
	except json.decoder.JSONDecodeError:
		return {dif(False): {}, dif(True): {}}


def writeFile(tabScores):
	print("writing to leaderboar")
	print(tabScores)
	with open(f"leaderboard.txt", "w") as flead:
		json.dump(tabScores, flead)
