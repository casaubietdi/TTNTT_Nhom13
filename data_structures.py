from __future__ import annotations
from typing import TypeVar, Generic, List, Deque, Optional

T = TypeVar('T') 


class Stack(Generic[T]): # Lớp ngăn xếp-Last In First Out (LIFO)
    def __init__(self) -> None: 
        self.container: List[T] = [] # Khởi tạo ngăn xếp và tạo một danh sách rỗng

    @property
    def empty(self) -> bool:    
        return not self.container  # Kiểm tra ngăn xếp, trả về True nếu ngăn xếp rỗng

    def push(self, item: T) -> None:
        self.container.append(item) # Thêm phần tử vào danh sách

    def pop(self) -> T:
        return self.container.pop()  # Thực hiện thao tác LIFO

    def __repr__(self) -> str:
        return repr(self.container) # Trả về chuỗi biểu diễn của ngăn xếp


class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node], cost: float = 0.0, heuristic: float = 0.0) -> None:
        self.state: T = state #Trạng thái, kiểu tổng quát
        self.parent: Optional[Node] = parent # Nút cha, có thể là None nếu không có
        self.cost: float = cost # Chi phí từ nút gốc đến nút hiện tại (gọi là g(n) trong A*)
        self.heuristic: float = heuristic # Ước lượng chi phí đến mục tiêu (gọi là h(n) trong A*)

    def __lt__(self, other: Node) -> bool: # __lt__ là viết tắt của “less than”, dùng cho toán tử <
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)
    # Cho phép Node được so sánh dựa trên tổng chi phí + heuristic

def node_to_path(node: Node[T]) -> List[T]: # Chuyển đổi Node thành đường đi
    path: List[T] = [node.state]
    # Bắt đầu từ nút hiện tại và đi ngược về nút gốc
    while node.parent is not None: 
        node = node.parent # Duyệt ngược từ nút hiện tại về nút cha của nó, lặp lại đến nút gốc
        path.append(node.state) # Mỗi lần lùi về cha, ta thêm node.state vào danh sách path
    path.reverse()
    return path


class Queue(Generic[T]): # Lớp hàng đợi-First In First Out (FIFO)
    def __init__(self) -> None:
        self.container: Deque[T] = Deque() # Khởi tạo hàng đợi và tạo một Deque rỗng

    @property
    def empty(self) -> bool:
        return not self.container  # Kiểm tra hàng đợi, trả về True nếu hàng đợi rỗng

    def push(self, item: T) -> None:
        self.container.append(item) # Thêm phần tử vào hàng đợi

    def pop(self) -> T:
        return self.container.popleft()  # Thực hiện thao tác FIFO

    def __repr__(self) -> str:
        return repr(self.container) # Trả về chuỗi biểu diễn của hàng đợi