class card:
    def __init__(self,image,value,suit,totalvalue):
        self.image = image
        self.value = self.cardassign(value)
        self.suit = self.suitassign(suit)
        self.totalvalue = float(f'{self.value}.{self.suit}')
    
    def cardassign(self,card):
        cardvalue = 0
        if card == "JACK":
            cardvalue = 11
        elif card == "QUEEN":
            cardvalue = 12
        elif card == "KING":
            cardvalue = 13
        elif card == "ACE":
            cardvalue = 1
        else:
            cardvalue = int(card)
        return cardvalue

    def suitassign(self,suit):
        cardsuit = 0
        if suit == "DIAMONDS":
            cardsuit = 0
        elif suit == "CLUBS":
            cardsuit = 1
        elif suit == "HEARTS":
            cardsuit = 2
        elif suit == "SPADES":
            cardsuit = 3
        return cardsuit
    
def cardmaker(carddata,int):
    cardimage = carddata["cards"][int]["image"]
    cardvalue = carddata["cards"][int]["value"]
    cardsuit = carddata["cards"][int]["suit"]
    totalvalue = 0
    createdcard = card(cardimage,cardvalue,cardsuit,totalvalue)
    return createdcard

   