class Node(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BST(object):
    def __init__(self, root):
        self.root = Node(root)

    def insert(self, new_val):
        return self.helper_insert(self.root, new_val)

    def helper_insert(self, start, new_val):
        """Helper method - use this to create a 
        recursive insertion solution."""
        if new_val > start.value:
            if start.right:
                return self.helper_insert(start.right, new_val)
            else:
                start.right = Node(new_val)
        elif new_val < start.value:
            if start.left:
                return self.helper_insert(start.left, new_val)
            else:
                start.left = Node(new_val)
        else:
            print "This value already exist in the tree"
          
            
    def search(self, find_val):
        return self.helper_search(self.root, find_val)

    def helper_search(self, start, find_val):
        """Helper method - use this to create a 
        recursive search solution."""
        if start:
            if find_val > start.value:
                return self.helper_search(start.right, find_val)
            elif find_val < start.value:
                return self.helper_search(start.left, find_val)
            else:
                return True
        else:
            return False
    
# Set up tree
tree = BST(4)

# Insert elements
tree.insert(2)
tree.insert(1)
tree.insert(3)
tree.insert(5)

# Check search
# Should be True
print tree.search(4)
# Should be False
print tree.search(6)