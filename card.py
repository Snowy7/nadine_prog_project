class Card:
    # initialize the card with attributes
    def __init__(self, name, size, rank, suit, faceUp=False):
        self.suit = suit
        self.rank = rank
        self.faceUp = faceUp

        self.coordinate = (0, 0)  # default position of card (x, y)
        self.color = self.checkColor()

        self.size = size  # dimension size of card
        self.name = name  # name of card imgs

    # display string card name
    def print(self):
        return self.toString()

    # return card name as string
    def toString(self):
        return "{} of {}".format(self.rank, self.suit)

    # x and y coordinates of card
    def getY(self):
        return self.coordinate[1]

    def getX(self):
        return self.coordinate[0]

    # check if mouse is clicked inside card
    def checkClick(self, mouseCoordinate):
        width, height = self.size
        Xmouse, Ymouse = mouseCoordinate

        return self.getX() < Xmouse < self.getX() + width and self.getY() < Ymouse < self.getY() + height

    # card suit color
    def checkColor(self):
        if self.suit == 'clubs' or self.suit == 'spades':
            return 'black'

        elif self.suit == 'hearts' or self.suit == 'diamonds':
            return 'red'
