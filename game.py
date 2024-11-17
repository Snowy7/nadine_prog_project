import pygame
from deck import Deck

screenSize = (1600, 910)
greenBG = (15, 85, 8)

pygame.init()
screen = pygame.display.set_mode(screenSize)


def main():
    deck = Deck()
    deck.initDeck()
    deck.deckShuffle()
    deck.initPile(screenSize)

    gameLoop = True
    while gameLoop:
        # win condition check
        if deck.winCheck():
            print("You won!")
            gameLoop = False  # exit the game

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameLoop = False  # exit the game
            # leftclick / button 1 for moves
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # get current cursor postion
                mousePointer = pygame.mouse.get_pos()
                # process move at current pointer and store updated piles reference
                changedPiles, _ = deck.mouseClick(mousePointer)
                # keep updating card deck to show updates
                deck.Deckupdate(changedPiles, screenSize[1])

        # draw screen objects
        screen.fill(greenBG)
        deck.deckPrint(screen)
        pygame.display.update()

    # end game
    pygame.quit()
    quit()

