from collections import defaultdict
import heapq

# Pattern 1: HashMap + Linked List (LRU Cache)
class HashMapLinkedList:
    """HashMap stores references to linked list nodes"""
    def __init__(self):
        self.map = {}  # key -> Node
        self.head = self.tail = None
    
    def example(self):
        # self.map[key] = node_reference
        pass

# Pattern 2: HashMap + Array/List (Index Mapping)
class HashMapArray:
    """HashMap stores indices into an array"""
    def __init__(self):
        self.map = {}  # key -> index in array
        self.arr = []  # actual data
    
    def add(self, key, value):
        if key not in self.map:
            self.arr.append(value)
            self.map[key] = len(self.arr) - 1  # Store index
    
    def get(self, key):
        if key in self.map:
            index = self.map[key]
            return self.arr[index]
        return None

# Pattern 3: HashMap + Heap (Priority Queue with Updates)
class HashMapHeap:
    """HashMap tracks elements in heap for O(1) existence checks"""
    def __init__(self):
        self.heap = []
        self.in_heap = set()  # Track what's currently in heap
        self.map = {}  # key -> priority or other metadata
    
    def push(self, item, priority):
        heapq.heappush(self.heap, (priority, item))
        self.in_heap.add(item)
        self.map[item] = priority
    
    def contains(self, item):
        return item in self.in_heap  # O(1) check instead of O(n) heap search

# Pattern 4: HashMap + Tree/Graph (Node References)
class GraphNode:
    def __init__(self, val):
        self.val = val
        self.neighbors = []

class HashMapGraph:
    """HashMap stores references to graph nodes"""
    def __init__(self):
        self.nodes = {}  # key -> GraphNode reference
    
    def add_node(self, key, val):
        self.nodes[key] = GraphNode(val)
    
    def add_edge(self, key1, key2):
        if key1 in self.nodes and key2 in self.nodes:
            self.nodes[key1].neighbors.append(self.nodes[key2])
            self.nodes[key2].neighbors.append(self.nodes[key1])

# Pattern 5: HashMap + Stack/Queue (Position Tracking)
class HashMapStack:
    """HashMap tracks positions of elements in stack"""
    def __init__(self):
        self.stack = []
        self.positions = {}  # element -> index in stack
    
    def push(self, item):
        self.stack.append(item)
        self.positions[item] = len(self.stack) - 1
    
    def remove_by_value(self, item):
        if item in self.positions:
            # This is simplified - real implementation needs to handle
            # position updates after removal
            index = self.positions[item]
            # Remove and update positions...

# Pattern 6: Two HashMaps (Bidirectional Mapping)
class BiDirectionalMap:
    """Two hashmaps for O(1) lookup in both directions"""
    def __init__(self):
        self.key_to_val = {}
        self.val_to_key = {}
    
    def put(self, key, val):
        # Remove old mappings if they exist
        if key in self.key_to_val:
            old_val = self.key_to_val[key]
            del self.val_to_key[old_val]
        if val in self.val_to_key:
            old_key = self.val_to_key[val]
            del self.key_to_val[old_key]
        
        # Add new bidirectional mapping
        self.key_to_val[key] = val
        self.val_to_key[val] = key
    
    def get_by_key(self, key):
        return self.key_to_val.get(key)
    
    def get_by_val(self, val):
        return self.val_to_key.get(val)

# Real-world example: Design Browser History
class BrowserHistory:
    """Uses HashMap + Array for O(1) navigation"""
    def __init__(self, homepage):
        self.history = [homepage]
        self.current = 0
        self.url_to_index = {homepage: 0}  # Optional: for quick checks
    
    def visit(self, url):
        # Clear forward history
        self.history = self.history[:self.current + 1]
        self.history.append(url)
        self.current += 1
    
    def back(self, steps):
        self.current = max(0, self.current - steps)
        return self.history[self.current]
    
    def forward(self, steps):
        self.current = min(len(self.history) - 1, self.current + steps)
        return self.history[self.current]

# Test the patterns
if __name__ == "__main__":
    print("=== HashMap + Array Pattern ===")
    hash_arr = HashMapArray()
    hash_arr.add("user1", "Alice")
    hash_arr.add("user2", "Bob")
    print(f"Get user1: {hash_arr.get('user1')}")
    print(f"Array: {hash_arr.arr}")
    print(f"Map: {hash_arr.map}")
    
    print("\n=== Bidirectional Map Pattern ===")
    bimap = BiDirectionalMap()
    bimap.put("name", "Alice")
    bimap.put("id", 123)
    print(f"Get by key 'name': {bimap.get_by_key('name')}")
    print(f"Get by val 'Alice': {bimap.get_by_val('Alice')}")
    
    print("\n=== Browser History Pattern ===")
    browser = BrowserHistory("google.com")
    browser.visit("facebook.com")
    browser.visit("youtube.com")
    print(f"Back 1: {browser.back(1)}")
    print(f"Forward 1: {browser.forward(1)}")
    print(f"Current history: {browser.history}")
    print(f"Current position: {browser.current}")