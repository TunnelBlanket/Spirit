worldHandlers = {
	"j#js": "handleJoinWorld",
	"j#jr": "handleJoinRoom"
}

def handleJoinWorld(self, data):
	from time import time

	self.logger.debug("Received joinWorld request")

	playerId = data[4]
	loginKey = data[5]

	if self.user.Id != int(playerId):
		self.logger.warn("User sent an invalid player id!")
		self.transport.loseConnection()

	if self.user.LoginKey != loginKey:
		self.logger.warn("User sent invalid login key in joinWorld request!")

	self.user.LoginKey = None
	self.session.commit()

	self.sendLine("%xt%js%-1%1%0%{0}%1%".format("1" if self.user.Moderator else "0"))

	playerString = self.getPlayerString()
	loginTime = time()

	# TODO - update?
	loadPlayer = "{0}|%{1}%0%1440%{2}%{3}%0%7521%%7%1%0%211843".format(playerString, self.user.Coins, str(loginTime),
	                                                                   self.age)
	self.sendLine("%xt%lp%-1%{0}%".format(loadPlayer))

def handleJoinRoom(self, data):
	self.logger.debug("Received joinRoom request")