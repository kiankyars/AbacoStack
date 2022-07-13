import random as r

class AbacoStack:
    '''
    Class which represents the AbacoStack structure
    '''

    def __init__(self, colours, stackDepth, card = None) -> None:
        '''
        Does: initializes and AbacoStack object
        Input: self (AbacoStack), colours (int), stackDepth (int)
        Output: None
        '''
        self.AbacoStack = [BStack(stackDepth) for i in range(colours)]
        #this is an optional parameter that I set (card), which just allows
        #the player to have a shuffled deck to start with instead of a sorted deck
        if card:
            configurationCard = r.shuffle(card).splitList()
            for i in range(colours):
                self.AbacoStack[i].setStack(configurationCard[i])
        else:
            for i in range(colours):
                self.AbacoStack[i].fill(chr(65 + i))
        self.topRow = [None for i in range(colours + 2)]
        self.moves = 0
        self.columns = colours
        self.rows = stackDepth

    def moveBead(self, move):
        '''
        Does: gets input to move the bead from a stack or the top row
        Input: self (AbacoStack), move (str)
        Output: bool
        '''
        try:
            column = int(move[:-1])
            direction = move[-1]
            if direction == 'l':
                self.moveLeft(column)
            elif direction == 'r':
                self.moveRight(column)
            elif direction == 'u':
                self.moveUp(column)
            elif direction == 'd':
                self.moveDown(column)
            else:
                raise Exception('Error: invalid move')
        except Exception as e:
            [print(e.args[0])]
            return False
        else:
            self.moves+=1
            return True

    def moveLeft(self, column):
        '''
        Does: helper function that moves a bead left
        Input: self (AbacoStack), column (int)
        Output: None
        '''
        assert 1 <= column <= self.columns + 1, 'Error: invalid move'
        assert self.topRow[column], 'Error: invalid move'
        assert not self.topRow[column - 1], 'Error: invalid move'
        self.topRow[column], self.topRow[column - 1] = (
            self.topRow[column - 1],
            self.topRow[column],
        )

    def moveRight(self, column):
        '''
        Does: helper function that moves a bead right
        Input: self (AbacoStack), column (int)
        Output: None
        '''
        assert 0 <= column <= self.columns, 'Error: invalid move'
        assert self.topRow[column], 'Error: invalid move'
        assert not self.topRow[column + 1], 'Error: invalid move'
        self.topRow[column], self.topRow[column + 1] = (
            self.topRow[column + 1],
            self.topRow[column],
        )

    def moveUp(self, column):
        '''
        Does: helper function that moves a bead up
        Input: self (AbacoStack), column (int)
        Output: None
        '''
        assert 1 <= column <= self.columns, 'Error: invalid move'
        assert not self.AbacoStack[column - 1].isEmpty(), 'Error: invalid move'
        assert not self.topRow[column], 'Error: invalid move'
        self.topRow[column] = self.AbacoStack[column - 1].pop()

    def moveDown(self, column):
        '''
        Does: helper function that moves a bead down
        Input: self (AbacoStack), column (int)
        Output: None
        '''
        assert 1 <= column <= self.columns, 'Error: invalid move'
        assert not self.AbacoStack[column - 1].isFull(), 'Error: invalid move'
        assert self.topRow[column], 'Error: invalid move'
        self.AbacoStack[column - 1].push(self.topRow[column])
        self.topRow[column] = None

    def isSolved(self, card):
        '''
        Does: checks if the current game state matches the configuration card
        Input: self (AbacoStack), card (Card)
        Output: bool
        '''
        instanceState = []
        card = card.splitList()
        for i in range(self.columns):
            instanceState.append(self.AbacoStack[i].getStack()[::-1])
        return instanceState == card

    def reset(self):
        '''
        Does: resets the game deck
        Input: self (AbacoStack)
        Output: None
        '''
        self.__init__(self.columns, self.rows)

    def show(self, card=None):
        '''
        Does: shows the game state in between turns
        Input: self (AbacoStack), card (Card)
        Output: None
        '''
        if card:
            #get a card to print
            configurationCard = card.configurationCard()
            #print all of the column indeces
            print(*range(self.columns + 2))
            #print top row
            print(*['.' if not x else x for x in self.topRow], '\tcard')
            for i in range(self.rows):
                temp = []
                for j in range(self.columns):
                    #check if the position with row i column j should be empty or filled
                    if i + self.AbacoStack[j].size() >= self.rows:
                        #add the appropriate element
                        temp.append(self.AbacoStack[j].getStack()[::-1][i-self.rows])
                    else:
                        #add a period
                        temp.append('.')
                #use the string join method to print
                join = ' '.join(temp)
                print(f'| {join} | \t{configurationCard[i]}')
            dash = '-' + '--' * self.columns
            print(f'+{dash}+ \t\t{self.moves} moves')
        else:
            print(*range(self.columns + 2))
            print(*['.' if not x else x for x in self.topRow])
            for i in range(self.rows):
                temp = []
                for j in range(self.columns):
                    if i + self.AbacoStack[j].size() >= self.rows:
                        temp.append(self.AbacoStack[j].getStack()[::-1][i-self.rows])
                    else:
                        temp.append('.')
                join = ' '.join(temp)
                print(f'| {join} |')
            dash = '-' + '--' * self.columns
            print(f'+{dash}+')


class BStack:
    def __init__(self, capacity):
        self.items = []
        self.capacity = capacity

    def fill(self, item):
        if not self.items:
            self.items = [item for i in range(self.capacity)]

    def push(self, item):
        try:
            assert self.size() <= self.capacity, 'the bounded stack is full'
        except AssertionError:
            print('the bounded stack is full, cannot push')
        else:
            self.items.append(item)

    def pop(self):
        try:
            return self.items.pop()
        except IndexError as e:
            print(e.args[0])

    def peek(self):
        try:
            return self.items[len(self.items) - 1]
        except IndexError as e:
            print(e.args[0])

    def isEmpty(self):
        return self.items == []

    def size(self):
        return len(self.items)

    def show(self):
        print(self.items)

    def __str__(self):
        stackAsString = ''
        for item in self.items:
            stackAsString += item + ' '
        return stackAsString

    def clear(self):
        if not self.items:
            self.items = []

    def isFull(self):
        return self.size() == self.capacity

    def getStack(self):
        return self.items

    def setStack(self, stack):
        self.items = stack

class Card:
    '''
    Class which represents a configuration card
    '''

    def __init__(self, colours, stackDepth) -> None:
        '''
        Does: constructs a Card object
        Input: self (Card), colours i.e. columns (int), stackDepth i.e. rows (int)
        Output: None
        '''
        self.__beads = []
        self.columns = int(colours)
        self.rows = int(stackDepth)
        for i in range(self.rows * self.columns):
            self.__beads.append(chr(65 + i // self.rows))

    def reset(self):
        '''
        Does: shuffles the bead list
        Input: self (Card)
        Output: None
        '''
        r.shuffle(self.__beads)

    def show(self):
        '''
        Does: prints the bead row-wisev
        Input: self (Card)
        Output: None
        '''
        list = self.splitList()
        for i in range(self.rows):
            temp = []
            for j in range(self.columns):
                temp.append(list[j][i])
            join = ' '.join(temp)
            print(f'|{join}|')

    def stack(self, number):
        '''
        Does: returns the n-th stack
        Input: self (Card), number (int)
        Output: None
        '''
        return self.splitList()[number - 1]

    def splitList(self):
        '''
        Does: splits the bead list into its respective stacks
        Input: self (Card)
        Output: None
        '''
        partitionedList = [
            self.__beads[i : i + self.rows]
            for i in range(0, len(self.__beads), self.rows)
        ]
        return partitionedList

    def replace(self, filename, n):
        '''
        Does: replaces the current self.__beads list with a file input
        Input: self (Card)
        Output: None
        '''
        with open(filename) as f:
            lines = f.readlines()
        line = list(lines[n].replace(' ', ''))
        self.__beads = line

    def configurationCard(self) -> str:
        '''
        Does: returns a print friendly version of the configuration card to be printed by the AbacoStack show method
        Input: self (Card)
        Output: rows (list)
        '''
        list = self.splitList()
        rows = []
        for i in range(self.rows):
            temp = []
            for j in range(self.columns):
                temp.append(list[j][i])
            join = ' '.join(temp)
            rows.append(f'|{join}|')
        return rows

    def __str__(self) -> str:
        '''
        Does: deafult string method for a card object
        Input: self (Card)
        Output: string (str)
        '''
        string = ''
        for i in range(1, self.columns + 1):
            add = ''.join(self.stack(i))
            string+=(f'|{add}|')
        return string

    def __repr__(self) -> str:
        '''
        Does: formal representation of a ScrabbleDict object
        Input: self (ScrabbleDict)
        Output: string representation (str)
        '''
        return f'Card object of depth {self.rows} with {self.columns} colours and appearance {self}'


def main():
    '''
    Does: executes other methods
    '''
    card = Card(4, 3)
    card.show()
    print(card.stack(1))
    print(str(card))
    print(repr(card))
    stack = BStack(5)
    stack.pop()
    stack.peek()
    stack.fill('A')
    stack.fill('B')
    print(stack)
    abacoStack = AbacoStack(5, 4)
    abacoStack.isSolved(card)
    abacoStack.show()
    abacoStack.moveBead('1u')
    abacoStack.show()
    card.replace('replace.txt', 0)


if __name__ == '__main__':

    main()
