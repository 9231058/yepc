class Temp():
    def __init__(self):
        self.seq = 0

    def new_temp(self):
        self.seq += 1
        return 'jj' + self.seq
