def makeBoard(length, height, defaulttile):
    board = [] # Will contain the full board as a 2D array
    tempRow = [] # Creates rows for the board
    
    for i in range(height):
        for j in range(length):
            tempRow.append(defaulttile) # Making a row of squares
        board.append(tempRow) # Adding row to the board
        tempRow = [] # Clearing the row
        
    return board

#==================================================================

def printBoard(board):
    print '\n' * 40 # "Only one board will be seen on-screen at once

    for i in range(1, len(board[0]) + 1): # Numbering the top of the board 1 - n
        print str(i) + ' ',
    print

    for i in range(len(board)): # Height of board
        for j in range(len(board[0])): # Length of board
            print board[i][j], "", # Print each item in a row next to each other
        print # Print the row and move on to the next row
 
#==================================================================

def dropChip(token, board, defaulttile):
    validMove = False
    
    while not validMove:
        print "\n", u"{0}".format(token), "Where do you want to drop your chip? (1 - {0})".format(len(board[0]))
                
        columnPlaced = raw_input("> ")
        
        # If the column is not filled, the input is between 1 - n, and the input is a number
        if columnPlaced.isdigit() and int(columnPlaced) <= len(board[0]) and \
        int(columnPlaced) > 0 and board[0][int(columnPlaced) - 1] == defaulttile:
            validMove = True
            columnPlaced = (int(columnPlaced) - 1) # The column in which the chip will fall

        else:
            print '\n' * 40 # Refresh the board
            printBoard(board)

    # This goes from the bottom row to the top row. Once a empty space is
    # detected, the chip gets placed there
    rowPlaced = (len(board) - 1) # The bottom row
    spaceIsOpen = True

    while spaceIsOpen:
        if board[rowPlaced][columnPlaced] == defaulttile: # If an empty square is
            board[rowPlaced][columnPlaced] = token        # found, place the chip
            spaceIsOpen = False
        
        else:
            rowPlaced -= 1 # Move the chip up one row

    return board

#==================================================================

def checkForWinner(board, currentPlayer): 
    consecutiveTokensNeededForWin = 4
    currentConsecutiveTokens = 0

    cursorX = 0
    cursorY = 0

    winner = False
 


    # Horizontal check
    for i in range(len(board)): # Iterate through all the rows

        # Check if there is n-in-a-row
        while cursorX < len(board[0]):
            if board[i][cursorX] == currentPlayer:
                currentConsecutiveTokens += 1
                
                # If there is n-in-a-row, there is a winner
                if currentConsecutiveTokens == consecutiveTokensNeededForWin:
                    winner = True

            else:
                currentConsecutiveTokens = 0

            cursorX += 1

        cursorX = 0
        currentConsecutiveTokens = 0



    # Vertical check
    for i in range(len(board[0])): # Iterate through all the columns

        # Check if there is n-in-a-row
        while cursorY < len(board):
            if board[cursorY][i] == currentPlayer:
                currentConsecutiveTokens += 1

                # If there is n-in-a-row, there is a winner
                if currentConsecutiveTokens == consecutiveTokensNeededForWin:
                    winner = True

            else:
                currentConsecutiveTokens = 0

            cursorY += 1

        cursorY = 0
        currentConsecutiveTokens = 0



    # Diagonal up-right check
    iteratorY = 0
    iteratorX = 0

    cursorY = 0
    cursorX = 0

    # This block scans the board in an "L" pattern.
    while iteratorY < len(board) and iteratorX < len(board[0]):
        while (iteratorY - cursorY) >= 0 and (iteratorX + cursorX) < len(board[0]):

            if board[iteratorY - cursorY][iteratorX + cursorX] == currentPlayer:
                currentConsecutiveTokens += 1

                # If there is n-in-a-row, there is a winner
                if currentConsecutiveTokens == consecutiveTokensNeededForWin:
                    winner = True

            else:
                currentConsecutiveTokens = 0

            cursorX += 1
            cursorY += 1

        if iteratorY != (len(board) - 1): # If iteratorY is not on bottom row,
            iteratorY += 1                # move down
        else:
            iteratorX += 1                # When last row is reached, 
                                          # move horizontally with iteratorX
        cursorY = 0
        cursorX = 0

        currentConsecutiveTokens = 0


    
    # Diagonal down-right check
    iteratorX = len(board[0]) - 1
    iteratorY = 0
    
    # This block scans in a backwards "L" pattern
    while iteratorY < len(board) and (iteratorX >= 0):
        while (iteratorY - cursorY) >= 0 and (iteratorX + cursorX) >= 0:

            if board[iteratorY - cursorY][iteratorX + cursorX] == currentPlayer:
                currentConsecutiveTokens += 1

                # If there is n-in-a-row, there is a winner
                if currentConsecutiveTokens == consecutiveTokensNeededForWin:
                    winner = True

            else:
                currentConsecutiveTokens = 0

            cursorX -= 1
            cursorY += 1


        if iteratorY != (len(board) - 1): # If iteratorY is not on bottom row.
            iteratorY += 1                # move down
        else:
            iteratorX -= 1                # When last row is reached,
                                          # move horizontally with iteratorX

        cursorY = 0
        cursorX = 0

        currentConsecutiveTokens = 0

    return winner

#==================================================================

boardLength = 7 # I don't suggest making this greater than 9
boardHeight = 6


standardTile = u"\u001b[34m\u25A2\u001b[0m" # Blue rounded-corner box

            #  Yellow filled square,         Red filled square (ANSI)
playerChips = [u'\u001b[33m\u25A0\u001b[0m', u'\u001b[31m\u25A0\u001b[0m']


currentBoard = makeBoard(boardLength, boardHeight, standardTile)
printBoard(currentBoard)

gameOver = False
draw = False

iterator = 1
movesPlayed = 0

while not gameOver and not draw:
    playerMove = dropChip(playerChips[iterator], currentBoard, standardTile) # Take a turn
    gameOver = checkForWinner(playerMove, playerChips[iterator]) # Check for winner
    printBoard(playerMove) # Print the board
    
    # Changes the player each turn
    iterator += 1 
    iterator %= 2

    movesPlayed += 1

    # If the board is completely filled, and no winner has been found
    if not gameOver and movesPlayed == (boardLength * boardHeight):
        draw = True


if draw and not gameOver:
    print "\nSorry! It's a draw. You're both losers\n"
else:
    print "\nCongratulations player " + playerChips[(iterator + 1) % 2] + ", you won!\n"
