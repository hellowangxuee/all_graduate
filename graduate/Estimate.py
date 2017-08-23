

class Estimate():
    def __init__(self):
        self.crosscommunity = set()
        t = 0
        with open("Twitter/cross_community.txt") as df:
            for d in df:
                if int(d.strip()) != 0:
                    self.crosscommunity.add(t)
                t += 1

    def calPRF(self,set1):
        P = float(len(set1 & self.crosscommunity))/float(len(set1))
        R = float(len(set1 & self.crosscommunity))/float(len(self.crosscommunity))
        if (P + R) == 0: F = 0
        else: F = float(2*P*R)/float(P+R)
        return P, R, F

if __name__ == '__main__':
    list = [76449,39916,39575,36536,84401,11606,80694,80958,83783,10840]
    set1 = set()
    for i in list:
        set1.add(i)
    e = Estimate()
    print e.crosscommunity
    p, r, f = e.calPRF(set1)
    print p, r, f