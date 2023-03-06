import random

team_states = {
    "blue": 0,
    "red": 0,
    "green": 0,
    "yellow": 0
}


class pawn(object):
    start_pos = {
        "blue": 2,
        "red": 15,
        "green": 28,
        "yellow": 41
    }

    finishing_pos_pos = {
        "blue": 0,
        "red": 13,
        "green": 26,
        "yellow": 39
    }

    def __init__(self, id, team):

        self.pos = -1
        self.team = team
        self.id = id
        self.is_finishing = False
        self.finished = False
        self.needed = 6

    def move(self, dice_roll):

        if (self.finished):
            return "error"
        if (self.is_finishing):
            if (dice_roll > self.needed):
                return "error"
            self.needed -= dice_roll
            if (not (self.needed)):
                self.finish()
                return "success"
        if (self.pos == -1 and not (dice_roll == 6)):
            return "error"
        if (self.pos == -1):
            self.pos = self.start_pos[self.team]
            return "success"
        potential = (self.pos + dice_roll) % 52
        if (potential > self.finishing_pos[self.team]):  # finishing
            self.is_finishing = True
            potential -= self.finishing_pos[self.team]
            self.needed = 6 - potential
            return "success"

    def finish(self):
        self.finished = True
        team_states[self.team] += 1
        if (team_states[self.team]) == 2:
            print(self.team, "wins!")
            exit(0)


class game(object):
    pawns = {
        "blue": [],
        "red": [],
        "green": [],
        "yellow": []
    }
    teams = ["blue", "red", "green", "yellow"]

    def roll(self):
        return random.randint(1, 7)

    def print_state(self):
        for team in self.teams:
            print(team, "state -")
            for pawn in self.pawns[team]:
                print(pawn.id, "is at", pawn.pos, "and is_finishing is", pawn.is_finishing, " and finished is ",
                      pawn.finished)

    def main(self):
        for team in self.teams:
            pawn1 = pawn(0, team)
            pawn2 = pawn(1, team)
            self.pawns[team] = [pawn1, pawn2]

        turn_number = 0
        while (True):
            current_team = self.teams[turn_number % 4]
            print("its ", current_team, "'s turn")
            d_roll = self.roll()
            current_team.move(d_roll)
            print("")