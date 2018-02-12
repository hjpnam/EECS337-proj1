class AwardCounter:

    def __init__(self):
        self.awards = {}

    def add_award(self, award):
        if award in self.awards:
            return False;
        else:
            self.awards[award] = {}
            return True

    def increment(self, award, actor):
        if award not in self.awards:
            self.awards[award] = {}
        if actor not in self.awards[award]:
            self.awards[award][actor] = 0
        self.awards[award][actor] += 1
        return True

	# def increment(self, award, actor):
	# 	if award not in self.awards:
	# 		self.awards[award] = {}
	# 	if actor not in self.awards[award]:
	# 		self.awards[award][actor] = 0
	# 	self.awards[award][actor] += 1
	# 	return True
    #
    # def increment_award_actor(self, award, actor):
    #     if award not in self.awards or actor not in self.awards[award]:
    #         return False
    #     self.awards[award][actor] += 1
    #     return True

    def get_actors_for_award(self, award):
        if award not in self.awards:
            return False
        return self.awards[award]

    def get_max_actor(self, award):
        if award not in self.awards:
            return False
        max_value = max(self.awards[award].values())
        return [k for k,v in self.awards[award].items() if v == max_value]

    def get_all(self):
        return self.awards

tester = AwardCounter()
tester.add_award("Best Actor")
tester.increment("Best Actor", "Gary Oldman")
tester.increment("Best Actor", "Gary Oldman")
tester.increment("Best Actor", "Timothee Chalamet")
print tester.get_all()
