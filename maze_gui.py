from enum import Enum
from logging import root
from tkinter import messagebox
from typing import List, NamedTuple, TypeVar, Set
import random
from data_structures import Stack, Queue, node_to_path, Node
from tkinter import *
from tkinter.ttk import *

T = TypeVar('T')


class Cell(str, Enum):
    EMPTY = " "        # Ô trống
    BLOCKED = "X"      # Ô bị chặn
    START = "S"        # Ô bắt đầu
    GOAL = "G"         # Ô đích
    EXPLORED = "E"     # Ô đã được duyệt
    CURRENT = "C"      # Ô đang xét tại bước hiện tại
    FRONTIER = "F"     # Các ô biên đang nằm trong frontier
    PATH = "*"         # Đường đi cuối cùng từ start -> goal
r:int = 0
c:int = 0
goal_r:int = 0
goal_c:int = 0
class main():
    def __init__(self, root):
        self.root = root
        self.root.title("Chuẩn bị mê cung")
        self.root.geometry("550x350")      
        # Tạo Label và Entry widget cho số nguyên đầu tiên
        Label(self.root, text="Số hàng của mê cung:").pack(pady=5)
        self.entry1 = Entry(self.root)
        self.entry1.pack(pady=5)
        # Tạo Label và Entry widget cho số nguyên thứ hai
        Label(self.root, text="Số cột của mê cung:").pack(pady=5)
        self.entry2 = Entry(self.root)
        self.entry2.pack(pady=5)
        
        Label(self.root, text="Vị trí đích ở hàng ?").pack(pady=5)
        self.entry3 = Entry(self.root)
        self.entry3.pack(pady=5)
        
        Label(self.root, text="Vị trí đích ở cột ?").pack(pady=5)
        self.entry4 = Entry(self.root)
        self.entry4.pack(pady=5)
        # Tạo nút để lấy giá trị và xử lý
        Button(self.root, text="Done", command=self.get_integers).pack(pady=10)

    def get_integers(self):
        try:
            # Lấy giá trị từ Entry và chuyển đổi thành số nguyên
            global r
            global c
            global goal_c
            global goal_r
            r = int(self.entry1.get()) 
            c = int(self.entry2.get())
            goal_r = int(self.entry3.get())
            goal_c = int(self.entry4.get())
        except ValueError:
            # Xử lý lỗi nếu giá trị nhập không phải là số nguyên
            messagebox.showerror("Lỗi", "Vui lòng nhập các số nguyên hợp lệ.")
        self.root.destroy()

class MazeLocation(NamedTuple):
    row: int
    column: int

    def __str__(self):
        return f"({self.row}, {self.column})" #In ra vị trí theo định dạng (row, column)
    
class MazeGUI:
    root = Tk()
    app = main(root)
    root.mainloop()
    # Các hàm getter để lấy các biến toàn cục (sử dụng cho constructor)
    def get_r()-> int:
        global r
        return r
    def get_c()-> int:
        global c
        return c
    def get_p_c()-> int:
        global goal_c
        return goal_c
    def get_p_r()-> int:
        global goal_r
        return goal_r
        
    def __init__(self, rows: int = get_r(), columns: int = get_c(), sparseness: float = 0.2, # xác suất mỗi ô là ô bị chặn
                 start: MazeLocation = MazeLocation(0, 0), goal: MazeLocation = MazeLocation(get_p_r(), get_p_c())) -> None:
        # Khởi tạo các biến thể hiện cơ bản
        self._rows: int = rows
        self._columns: int = columns
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal
        # Lấp đầy lưới bằng các ô trống
        self._grid: List[List[Cell]] = [[Cell.EMPTY for c in range(columns)] for r in range(rows)]
        # Lấp đầy lưới bằng các ô bị chặn
        self._randomly_fill(rows, columns, sparseness)
        # Điền vào vị trí bắt đầu và vị trí đích
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL
        
        self._setup_GUI()

    def _setup_GUI(self):
        # start the GUI
        self.root: Tk = Tk()
        self.root.title("Đại chiến mê cung")
        # Đảm bảo frame con có thể co giãn theo cửa sổ
        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)
        # Tạo một khung để chứa toàn bộ widget chính
        frame: Frame = Frame(self.root)
        frame.grid(row=0, column=0, sticky=N + S + E + W)
        # style for widgets
        style: Style = Style() # Tạo một đối tượng Style từ module ttk
        style.theme_use('classic')
        style.configure("BG.TLabel", foreground="black", font=('Helvetica', 26))
        style.configure("BG.TButton", foreground="black", font=('Helvetica', 26))
        style.configure("BG.TListbox", foreground="black", font=('Helvetica', 26))
        style.configure("BG.TCombobox", foreground="black", font=('Helvetica', 26))
        style.configure(" ", foreground="black", background="white")
        style.configure(Cell.EMPTY.value + ".TLabel", foreground="black", background="white", font=('Helvetica', 26))
        style.configure(Cell.BLOCKED.value + ".TLabel", foreground="white", background="black", font=('Helvetica', 26))
        style.configure(Cell.START.value + ".TLabel", foreground="black", background="green", font=('Helvetica', 26))
        style.configure(Cell.GOAL.value + ".TLabel", foreground="black", background="red", font=('Helvetica', 26))
        style.configure(Cell.PATH.value + ".TLabel", foreground="black", background="cyan", font=('Helvetica', 26))
        style.configure(Cell.EXPLORED.value + ".TLabel", foreground="black", background="yellow", font=('Helvetica', 26))
        style.configure(Cell.CURRENT.value + ".TLabel", foreground="black", background="blue", font=('Helvetica', 26))
        style.configure(Cell.FRONTIER.value + ".TLabel", foreground="black", background="orange", font=('Helvetica', 26))
        # Hiển thị chỉ số hàng
        for row in range(self._rows):
            Grid.rowconfigure(frame, row, weight=1)
            row_label: Label = Label(frame, text=str(row), style="BG.TLabel", anchor="center")
            row_label.grid(row=row, column=0, sticky=N + S + E + W)
            Grid.rowconfigure(frame, row, weight=1)
            Grid.grid_columnconfigure(frame, 0, weight=1)
        # Hiển thị chỉ số cột
        for column in range(self._columns):
            Grid.columnconfigure(frame, column, weight=1)
            column_label: Label = Label(frame, text=str(column), style="BG.TLabel", anchor="center")
            column_label.grid(row=self._rows, column=column + 1, sticky=N + S + E + W)
            Grid.rowconfigure(frame, self._rows, weight=1)
            Grid.columnconfigure(frame, column + 1, weight=1)
        # Khởi tạo lưới
        self._cell_labels: List[List[Label]] = [[Label(frame, anchor="center") for c in range(self._columns)] for r in range(self._rows)]
        for row in range(self._rows):
            for column in range(self._columns):
                cell_label: Label = self._cell_labels[row][column]
                Grid.columnconfigure(frame, column + 1, weight=1)
                Grid.rowconfigure(frame, row, weight=1)
                cell_label.grid(row=row, column=column + 1, sticky=N + S + E + W)
        self._display_grid()
        # setup các nút
        dfs_button: Button = Button(frame, style="BG.TButton", text="Run DFS", command=self.dfs)
        dfs_button.grid(row=self._rows + 2, column=0, columnspan=6, sticky=N + S +E+W)
        bfs_button: Button = Button(frame, style="BG.TButton", text="Run BFS", command=self.bfs)
        bfs_button.grid(row=self._rows + 2, column=6, columnspan=6, sticky=N + S + E + W)
        Grid.rowconfigure(frame, self._rows + 2, weight=1)
        # setup data structure displays
        frontier_label: Label = Label(frame, text="Frontier", style="BG.TLabel", anchor="center")
        frontier_label.grid(row=0, column=self._columns + 2, columnspan=3, sticky=N + S + E + W)
        explored_label: Label = Label(frame, text="Explored", style="BG.TLabel", anchor="center")
        explored_label.grid(row=self._rows // 2, column=self._columns + 2, columnspan=3, sticky=N + S + E + W)
        Grid.columnconfigure(frame, self._columns + 2, weight=1)
        Grid.columnconfigure(frame, self._columns + 3, weight=1)
        Grid.columnconfigure(frame, self._columns + 4, weight=1)
        self._frontier_listbox: Listbox = Listbox(frame, font=("Helvetica", 14))
        self._frontier_listbox.grid(row=1, column=self._columns + 2, columnspan=3, rowspan=self._rows // 2 - 1, sticky=N + S + E + W)
        self._explored_listbox: Listbox = Listbox(frame, font=("Helvetica", 14))
        self._explored_listbox.grid(row=self._rows // 2 + 1, column=self._columns + 2, columnspan=3, rowspan=self._rows // 2 - 1, sticky=N + S + E + W)
        interval_label: Label = Label(frame, text="Interval", style="BG.TLabel", anchor="center")
        interval_label.grid(row=self._rows + 1, column=self._columns + 2, columnspan=3, sticky=N + S + E + W)
        self._interval_box: Combobox = Combobox(frame, state="readonly", values=[1, 2, 3, 4, 5], justify="center", style="BG.TCombobox")
        self._interval_box.set(2)
        self._interval_box.grid(row=self._rows + 2, column=self._columns + 2, columnspan=3, sticky=N + S + E + W)
        # pack and go
        frame.pack(fill="both", expand=True)
        self.root.mainloop()
    # Tạo mê cung ngẫu nhiên với xác suất ô bị chặn
    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED
    # Hiển thị lưới mê cung trong GUI
    def _display_grid(self):
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL
        for row in range(self._rows):
            for column in range(self._columns):
                cell: Cell = self._grid[row][column]
                cell_label: Label = self._cell_labels[row][column]
                cell_label.configure(style=cell.value + ".TLabel")

    # Hàm step trong thuật toán tìm kiếm, xử lý từng bước một
    def step(self, frontier, explored, last_node):
        if not frontier.empty:
            # Nếu frontier không rỗng, lấy node đầu/đỉnh ra (Stack hoặc Queue)
            current_node: Node[T] = frontier.pop()
            current_state: T = current_node.state
            # Xóa phần tử khỏi frontier_listbox
            if isinstance(frontier, Stack):
                self._frontier_listbox.delete(END, END)
            elif isinstance(frontier, Queue):
                self._frontier_listbox.delete(0, 0)
            # Đánh dấu ô hiện tại là ô đang xét    
            self._grid[current_state.row][current_state.column] = Cell.CURRENT
            # Đánh dấu ô trước đó là đã duyệt, đổi màu ô đó
            if last_node is not None:
                self._grid[last_node.state.row][last_node.state.column] = Cell.EXPLORED
            # Nếu tìm thấy đích thì truy vết đường đi từ node đích về start
            if self.goal_test(current_state):
                path = node_to_path(current_node)
                self.mark(path) # Đánh dấu đường đi trên lưới
                self._display_grid()
                return
            # Kiểm tra xem có thể đi đến những đâu tiếp theo và là nơi chưa từng đi qua
            for child in self.successors(current_state):
                if child in explored:  # Bỏ qua các nút con đã đi qua
                    continue
                explored.add(child)
                frontier.push(Node(child, current_node))
                # Đánh dấu ô mới thêm vào frontier là FRONTIER, thêm thông tin tọa độ vào 2 listbox
                self._grid[child.row][child.column] = Cell.FRONTIER
                self._explored_listbox.insert(END, str(child))
                self._frontier_listbox.insert(END, str(child))
                self._explored_listbox.select_set(END)
                self._explored_listbox.yview(END)
                self._frontier_listbox.select_set(END)
                self._frontier_listbox.yview(END)
            self._display_grid()
            # Thời gian trễ giữa các bước
            num_delay = int(self._interval_box.get()) * 1000
            self.root.after(num_delay, self.step, frontier, explored, current_node)

    def dfs(self):
        self.clear()
        self._display_grid()
        # Khởi tạo Frontier (ngăn xếp)
        frontier: Stack[Node[T]] = Stack()
        frontier.push(Node(self.start, None))
        # Tập explored lưu các trạng thái đã đi qua để tránh lặp lại
        explored: Set[T] = {self.start}
        # Gọi hàm step() để bắt đầu quá trình tìm kiếm
        self.step(frontier, explored, None)

    def bfs(self):
        self.clear()
        self._display_grid()
        # Khởi tạo Frontier (hàng đợi)
        frontier: Queue[Node[T]] = Queue()
        frontier.push(Node(self.start, None))
        # Tập explored lưu các trạng thái đã đi qua để tránh lặp lại
        explored: Set[T] = {self.start}
        # Gọi hàm step() để bắt đầu quá trình tìm kiếm
        self.step(frontier, explored, None)

    # Trả về một phiên bản mê cung đã hoàn thành
    def __str__(self) -> str:
        output: str = ""
        for row in self._grid:
            output += "".join([c.value for c in row]) + "\n"
        return output
    # Kiểm tra xem ô hiện tại có phải là ô đích không
    def goal_test(self, ml: MazeLocation) -> bool:
        return ml == self.goal
    # Trả về các ô kế tiếp có thể đi đến từ ô hiện tại
    def successors(self, ml: MazeLocation) -> List[MazeLocation]:
        locations: List[MazeLocation] = []
        if ml.row + 1 < self._rows and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.column))
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))
        if ml.column + 1 < self._columns and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column + 1))
        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))
        return locations

    def mark(self, path: List[MazeLocation]):
        for maze_location in path:
            # Đánh dấu các ô trong đường đi là PATH
            self._grid[maze_location.row][maze_location.column] = Cell.PATH
        # Đánh dấu ô bắt đầu và ô đích
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def clear(self):
        # Xóa hiển thị trong 2 Listbox
        self._frontier_listbox.delete(0, END)
        self._explored_listbox.delete(0, END)
        for row in range(self._rows):
            # Đặt lại các ô trong lưới về trạng thái ban đầu
            for column in range(self._columns):
                if self._grid[row][column] != Cell.BLOCKED:
                    self._grid[row][column] = Cell.EMPTY
        # Đặt lại các ô bắt đầu và đích
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

if __name__ == "__main__":

    m: MazeGUI = MazeGUI()