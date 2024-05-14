class Mancala_Board:
    def __init__(self, mancala):
        if mancala != None:
            self.mancala = mancala[:]
        else:
            self.mancala = [0 for i in range(14)]
            for i in range(0,6):
                self.mancala[i] = 4
            for i in range(7,13):
                self.mancala[i] = 4

    def player_move(self, i):
        j = i
        repeat_turn = False
        add = self.mancala[j]
        self.mancala[j] = 0
        if i > 6:
            stones = add
            while stones > 0:
                i += 1
                i = i % 14
                if i == 6:
                    continue
                else:
                    self.mancala[i % 14] += 1
                stones -= 1
            if i > 6 and self.mancala[i] == 1 and i != 13 and self.mancala[5-(i-7)] != 0:
                self.mancala[13] += 1 + self.mancala[5-(i-7)]
                self.mancala[i] = 0
                self.mancala[5-(i-7)] = 0
            if i == 13:
                repeat_turn = True
        else:
            stones = add
            while (stones > 0):
                i += 1
                i = i % 14
                if i == 13:
                    continue
                else:
                    self.mancala[i%14] += 1
                stones -= 1
            if i < 6 and self.mancala[i] == 1 and i !=6 and self.mancala[-i + 12]!=0:
                self.mancala[6] += 1 + self.mancala[-i + 12]
                self.mancala[i] = 0
                self.mancala[-i + 12] = 0
            if i == 6:
                repeat_turn = True
        return repeat_turn

    def isEnd(self):
        if sum(self.mancala[0:6])==0 :
            self.mancala[13]+=sum(self.mancala[7:13])
            for i in range(14):
                if  (i != 13 and i != 6):
                    self.mancala[i] = 0

            return True
        elif sum(self.mancala[7:13])==0:
            self.mancala[6] += sum(self.mancala[0:6])
            for i in range(14):
                if  (i != 13 and i != 6):
                    self.mancala[i] = 0
            return True

        return False

    def print_mancala(self):
        for i in range(12,6,-1):
            print('  ', self.mancala[i], '   ', end = '')
        print('  ')
        print(self.mancala[13],'                                           ',self.mancala[6])

        for i in range(0,6,1):
            print('  ', self.mancala[i], '   ', end='')
        print('  ')
    def husVal(self):
        if self.isEnd():
            if self.mancala[13]>self.mancala[6]:
                return 100
            elif self.mancala[13]==self.mancala[6]:
                return 0
            else :
                 return -100
        else:
            return self.mancala[13]- self.mancala[6]