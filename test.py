from __future__ import annotations
from enum import Enum
from platform import node
import random
from typing import Callable, Deque, Generic, NamedTuple, Optional, TypeVar,List
import tkinter as tk
from tkinter import *
T = TypeVar("T")


list  = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]

goal  = 9 
class Stack(Generic[T]):
    def __init__(self) -> None:
          self.container:List [T] = []
    @property
    def empty(self) -> bool:
        return not self.container
    
    def push(self,item: T) -> None:
        self.container.append(item)
        
    def pop(self) ->T:
        return self.container.pop #LIFO
    def __repr__(self) -> str:
         return self.container
class Queue(Generic[T]):
    def __init__(self) -> None:
        self.container: Deque[T] = Deque()

    @property
    def empty(self) -> bool:
        return not self.container  # not is true for empty container

    def push(self, item: T) -> None:
        self.container.append(item)

    def pop(self) -> T:
        return self.container.popleft()  # FIFO

    def __repr__(self) -> str:
        return repr(self.container)
class Cell(str, Enum):
    EMPTY =" "
    BLOCKED = "X"
    START ="S"
    GOAL = "G"
    PATH = "-"
class MazeLocation(NamedTuple):
    row :int
    column:int
class setup:
    r = tk.Tk()
    r.title('Counting Seconds')
    button = tk.Button(r, text='Stop', width=25, command=r.destroy)
    button.pack()
    r.mainloop()
class Maze:
    def __init__(self, row:int =10 ,column:int = 10, sparseness:float = 0.2, start:MazeLocation = MazeLocation(0,0), goal:MazeLocation = MazeLocation(9,9) 
                 ) -> None:
        self._row:int = row
        self._column:int  = column
        self.start:MazeLocation = start
        self.goal:MazeLocation = goal
        # empty Cell
        self._grid: List[List[Cell]] =[[Cell.EMPTY for c in range(column)] for r in range(row)] 
        self._randomly_fill(row,column,sparseness)
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] =Cell.GOAL
    def _randomly_fill(self,row:int ,column:int,sparseness:float):
        for r in range(row):
            for c in range(column):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[r][c] = Cell.BLOCKED
    def __str__(self) -> str:
        output: str = ""
        for row in self._grid:
            output += "".join([c.value for c in row]) + "\n"
        return output
    #Check if there is a cell empty at right, left, above or below
    def successor(self, ml: MazeLocation) -> List[MazeLocation]:
        locations: List[MazeLocation] =[]
        if ml.row + 1 < self._rows and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.column))
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))
        if ml.column + 1 < self._columns and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column + 1))
        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))
        return locations


class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node]) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
    def dfs(initial:T, goal_test : Callable[[T], bool] , successor: Callable[[T],List[T]]) ->Optional[Node]:
        #tap mo
        frontier: Stack[Node[T]] = Stack()
        frontier.push(Node(initial, None))
        #tap dong
        explored: set[T] = initial
#test:
maze: setup = setup()


    

            
        
        
        
    



