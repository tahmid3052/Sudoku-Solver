def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    def isSudokuValid():
        for i in range(9):
            #gets all the numbers in the row
            row = sudoku[i, :]
            #gets all the numbers in the column
            column = sudoku[:, i]
            #gets all the numbers in the 3x3 grid
            grid = sudoku[i // 3 * 3:(i // 3 + 1) * 3, i % 3 * 3:(i % 3 + 1) * 3].flat
            #checks if any number appears more than once in either row, grid, or column
            if any(
                np.count_nonzero(row == num) > 1 or
                np.count_nonzero(column == num) > 1 or
                np.count_nonzero(grid == num) > 1
                for num in range(1, 10)
            ):
                return False
        #returns true if this is a valid sudoku grid for solving
        return True
    
    #function to get a list of all the valid options for the current empty cell
    def getValidOptions(row, column):
        #gets all the numbers that are being used in the current row
        rowUsed = set(sudoku[row, :])
        #gets all the numbers that are being used in the current column
        columnUsed = set(sudoku[:, column])
        #gets all the number that are being used in the current 3x3 grid
        gridUsed = set(sudoku[row // 3 * 3:(row // 3 + 1) * 3, column // 3 * 3:(column // 3 + 1) * 3].flat)
        #combines all the used numbers
        used = rowUsed | columnUsed | gridUsed
        #returns the numbers that are not in the used numbers
        return [num for num in range(1, 10) if num not in used]

    #a function that is based on the MRV (minimum remaining values) heuristic
    def mrvCell():
        #initialising the minimum number of options to more than 9
        minCellOptions = 10
        #for when no empty cells are found, this initalisation of mrvCell is returned to show that
        mrvCell = (-1, -1)
        #looping through the rows
        for row in range(9):
            #looping through the columns
            for column in range(9):
                #a check to see if the current cell is empty or not
                if sudoku[row, column] == 0:
                    #gets all the valid options for the cell
                    cellOptions = getValidOptions(row, column)
                    #a check that replaces the minCellOptions with the current cellOptions if its lower than it
                    if len(cellOptions) < minCellOptions:
                        #replacing happens here
                        minCellOptions = len(cellOptions)
                        mrvCell = (row, column)
                        #a check to see if theres only 1 option, if so, return it
                        if minCellOptions == 1:
                            return mrvCell
        #returns the MRV cell
        return mrvCell

    #a function that is called recursively to solve each cell of the sudoku puzzle by backtracking
    def solve():
        #mrvCell function is used to find the next best empty cell and stores the row and column of it
        row, column = mrvCell()
        #if (-1,-1) is returned, then the sudoku has now been solved
        if row == -1 or column == -1:
            return True
        #gets all the valid options for the cell
        cellOptions = getValidOptions(row, column)
        #goes through each valid number in the list
        for i in cellOptions:
            sudoku[row, column] = i
            #keep doing the solve function until the sudoku is solved
            if solve():
                return True
            #if it doesnt work, then makes the cell empty again for backtracking
            sudoku[row, column] = 0
        #returns false if there is not solution
        return False
    #a check to see if the isSudokuValid function returns false 
    if not isSudokuValid():
        #if it does return false, it means theres no solution, so it replaces all cells with -1
        sudoku[:, :] = -1
        return sudoku
    #a check to see if the solve function returns false 
    if not solve():
        #if it does return false, it means theres no solution, so it replaces all cells with -1
        sudoku[:, :] = -1
    #returns the sudoku
    return sudoku
