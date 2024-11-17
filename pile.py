from collections import namedtuple


class Pile:
    def __init__(self, cards, Xcoordinate, Ycoordinate, dimensions, type="TABLEAU"):
        self.cards = cards
        self.y = Ycoordinate
        self.x = Xcoordinate
        self.CardW, self.CardH = dimensions
        self.type = type
        self.PileOrder = namedtuple(
            'PileOrder', ['suit', 'rank', 'base'])

# self.spread means to distrubute the cards in vertical line as in tableau
        # stock pile cards order
        if self.type == 'STOCK':
            self.tableauSpread = False
            self.placementOrder = self.PileOrder(
                suit=None, rank=None, base=None)
            self.PileHeight = self.CardH
            self.faceUp = 'none'

        # waste pile cards order
        elif self.type == 'WASTE':
            self.tableauSpread = False
            self.placementOrder = self.PileOrder(
                suit=None, rank=None, base=None)
            self.PileHeight = self.CardH
            self.faceUp = 'ALL'

        # foundation pile cards order
        elif self.type == 'FOUNDATION':
            self.tableauSpread = False
            self.placementOrder = self.PileOrder(
                suit='same', rank=1, base='ace')
            self.PileHeight = self.CardH
            self.faceUp = 'ALL'

        # tableau pile cards order
        elif self.type == 'TABLEAU':
            # only distribute tableau cards in vertical lines
            self.tableauSpread = True
            self.placementOrder = self.PileOrder(
                suit='alternate',  rank=-1, base='king')
            self.PileHeight = 450
            self.faceUp = 'TOP'

        # cards sizes
        self.footerMargin = 15
        self.CardMinPadding = 15
        self.CardMaxPadding = 50
        self.CardsPadding = self.CardMaxPadding
        self.RefreshPileLayout()

    # check mouse click
    def isClicked(self, mouseCoordinate):
        Xmouse, Ymouse = mouseCoordinate
        # check if mouse click is within pile boundary
        return self.x < Xmouse < self.x + self.CardW and self.y < Ymouse < self.y + self.PileHeight

    # check card selection so that onward piles can be moved
    def selectionCheck(self, mouseCoordinate, piles):
        PilesReset = False
        isSelected = False
        CardsSelected = []

        # Check if a card in the pile was clicked
        for index, card in enumerate(self.cards):
            if card.checkClick(mouseCoordinate) and card.faceUp:
                isSelected = True
                CardsSelected = self.cards[index:]

        #  stock pile behavior
        if self.type == 'STOCK':
            PilesReset = True
            wastePile = next(
                (pile for pile in piles if pile.type == 'WASTE'), None)

            if len(self.cards) != 0:
                # moving top card from stock to waste
                wastePile.cards.append(self.cards[-1])
                del self.cards[-1]
            else:
                # when stock is empty, refill the stock from waste
                self.cards = wastePile.cards[::-1]
                wastePile.cards = []

        return isSelected, CardsSelected, PilesReset

    # determine card select area
    def cardSelectionArea(self, card):
        # selected card highlight thickness
        selectedCardHighlight = 5
        # x and y coordinates for selection area
        xAXIS = card.getX() - selectedCardHighlight
        yAXIS = card.getY() - selectedCardHighlight
        # width and height of selected area
        selectionWidth = self.CardW + (selectedCardHighlight * 2)
        selectionHeight = self.CardH + (selectedCardHighlight * 2)
        return [xAXIS, yAXIS, selectionWidth, selectionHeight]

    # determine which card to turn face up
    def FaceUpChange(self):
        if len(self.cards) != 0:
            for index, card in enumerate(self.cards):
                if self.faceUp == 'none':
                    card.faceUp = False
                    # only turn last card of pile
                elif self.faceUp == 'TOP' and index == len(self.cards) - 1:
                    card.faceUp = True
                    # turn all cards
                elif self.faceUp == 'ALL':
                    card.faceUp = True

    # determine whether to stack cards or place with padding
    def CardCoordinateChange(self):
        if len(self.cards) > 0:
            for index, card in enumerate(self.cards):
                # if tableau spread is enabled, position cards with proper padding
                if self.tableauSpread:
                    card.coordinate = (self.x, self.y +
                                       (index * self.CardsPadding))
                # else just place cards on each other
                else:
                    card.coordinate = (self.x, self.y)

    # adjust vertical length of tablue piles
    def adjustTableauPilesLength(self, heightOFscreen):
        # calculating bottom boundary of the screen
        screenLimit = heightOFscreen - self.footerMargin
        # if pile has cards
        if len(self.cards) > 0:

            #  decrease card spacing if the last card is beyond  screen limit
            if self.lastCard() > screenLimit:
                while self.CardsPadding > self.CardMinPadding:
                    # break if the last card is yet within screen bounds
                    if self.lastCard() < screenLimit:
                        break
                    else:
                        # else reduce card spacing by decrementing and update card coordinates
                        self.CardsPadding -= 1 / len(self.cards)
                        self.CardCoordinateChange()

            # if last card is above the screen limit, increase card spacing
            elif self.lastCard() < screenLimit:
                while self.CardsPadding < self.CardMaxPadding:
                    # break if the last card exceeds screen bounds
                    if self.lastCard() > screenLimit:
                        break
                    else:
                        # else increase card spacing by incrementing and update card coordinates
                        self.CardsPadding += 1 / len(self.cards)
                        self.CardCoordinateChange()

            # clean up final output
            self.CardsPadding = round(self.CardsPadding)

    # retrieve position of last card if it exists in self.cards[]
    def lastCard(self):
        return self.cards[-1].coordinate[1] + self.CardH if self.cards else self.y

    def validMove(self, PileDestination, CardsSelected, sequenceOfRanks):
        valid = True
        # determine bottom card in destination pile
        if len(PileDestination.cards) != 0:
            PileLastCard = PileDestination.cards[-1]
        else:
            PileLastCard = None

        # top card of the selected cards
        firstCard = CardsSelected[0]

        # ---rules---#

        # Rules for an empty destination pile
        if PileLastCard is None:
            # compare base rank
            if PileDestination.placementOrder.base is not None:
                # check if first card rank match required base rank in destination pile
                if firstCard.rank != PileDestination.placementOrder.base:
                    # if rank doesnot match, its invalid move
                    valid = False

        # Rules for a non-empty destination pile
        else:
            # pile has suit or color requirment
            if PileDestination.placementOrder.suit is not None:
                # alternating colors or same suit based on destination pile requirements
                if PileDestination.placementOrder.suit == 'alternate':
                    # means that color of first and last card must be different
                    if firstCard.color == PileLastCard.color:
                        valid = False
                elif PileDestination.placementOrder.suit == 'same':
                    # means that suits of first and last card must be different
                    if firstCard.suit != PileLastCard.suit:
                        valid = False
            # check that first and piles last card rank is correct
            if PileDestination.placementOrder.rank is not None:
                lastCardRankPosition = sequenceOfRanks.index(PileLastCard.rank)
                # check if the selected card's rank follows the required rank sequence
                if firstCard.rank != sequenceOfRanks[lastCardRankPosition + PileDestination.placementOrder.rank]:
                    valid = False

        # Rule, cannot move cards to stock or waste piles
        if PileDestination.type in ['WASTE', 'STOCK']:
            valid = False

        return valid

    # move cards a target pile if transfer is valid
    def moveSelectedCardsToPile(self, CardsSelected, PileDestination, sequenceOfRanks):
        # check valid moves
        if self.validMove(PileDestination, CardsSelected, sequenceOfRanks):
            # if yes, transfer each card selected to desired pile
            for card in CardsSelected:
                PileDestination.cards.append(card)
                # keep removing card from current pile
                self.cards.remove(card)
            return True
        return False

    # update pile
    def RefreshPileLayout(self):
        self.CardCoordinateChange()
        self.FaceUpChange()
