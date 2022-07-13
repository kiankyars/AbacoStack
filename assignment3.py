from AbacoStack import *
import time as t

class Game:
    '''
    Class which represents an AbacoStack game
    '''

    def __init__(self) -> None:
        '''
        Does: initializes the Game class
        Input: self (Game)
        Output: None
        '''
        self.continueGame = True
        self.abacoStack = None
        self.card = None

    def play(self):
        '''
        Does: plays the game
        Input: self (Game)
        Output: None
        '''
        #gets initial input
        correct = False
        while not correct:
            try:
                columns, rows = self.getInput()
            except ValueError as e:
                print(e.args[0])
            except AssertionError as e:
                print(e.args[0])
            else:
                correct = True
        #creates Card and AbacoStack object and starts timer
        self.card = Card(columns, rows)
        self.card.reset()
        self.abacoStack = AbacoStack(columns, rows)
        start = t.time()
        #main game loop
        while self.continueGame:
            self.abacoStack.show(self.card)
            correct = False
            while not correct:
                Input = input('Enter your move(s) [Q for quit and R to reset]: ')
                if Input.upper() == 'Q':
                    print('Quit game, goodbye…')
                    quit()
                elif Input.upper() == 'R':
                    self.abacoStack.reset()
                    correct = True
                elif len(Input) < 2:
                    print('Error: invalid move')
                else:
                    correct = True
                    Input = Input.replace(' ', '')
                    move = Input[:10]
                    #integer division so that there cannot be an odd length of a string
                    moves = len(move)//2
                    successful = True
                    #breaks up input into its respective amount of moves up to 5
                    for i in range(0,2*moves,2):
                        if successful:
                            successful = self.abacoStack.moveBead(move[i:i+2])
            if self.abacoStack.isSolved(self.card):
                stop = t.time()
                self.continueGame = False
        timeTaken = stop - start
        self.abacoStack.show(self.card)
        print(f'Congratulations, you solved the AbacoStack in {round(timeTaken, 1)} s!')
        correct = False
        while not correct:
            Input = input('Would you like to get another configuration card to attempt? (Y or N): ')
            if Input.upper() == 'Y':
                correct = True
                main()
            elif Input.upper() == 'N':
                quit()
            else:
                print(f'Invalid input: {Input}')
            

    def getInput(self):
        '''
        Does: gets user input for column and row size
        Input: self (Card)
        Output: columns (int), rows (int)
        '''
        columns = int(input('Choose the number of colours in range [2,5]: '))
        rows = int(input('Select the depth of the stacks in range [2,4]: '))
        assert 2<=columns<=5 and 2<=rows<=4, 'Numbers outside of range'
        return columns, rows
    
    def __repr__(self) -> str:
        '''
        Does: formal representation of a Game object
        Input: self (Game)
        Output: string representation (str)
        '''

        return f'Game class for AbacoStack using {self.abacoStack.show()} and card {self.card}'

def main():
    '''
    Does: executes other methods
    '''
    game = Game()
    game.play()
    
if __name__ == '__main__':

    main()