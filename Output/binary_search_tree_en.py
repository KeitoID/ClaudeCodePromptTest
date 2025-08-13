"""
Binary Search Tree implementation with comprehensive functionality.

This module provides a complete Binary Search Tree (BST) implementation
with insert, search, delete, traversal, and utility methods.
"""

from typing import Optional, List, Any, Union


class TreeNode:
    """
    A node in the Binary Search Tree.
    
    Attributes:
        value: The value stored in the node
        left: Reference to the left child node
        right: Reference to the right child node
    """
    
    def __init__(self, value: Any) -> None:
        """
        Initialize a tree node with a value.
        
        Args:
            value: The value to store in the node
        """
        self.value: Any = value
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None


class BinarySearchTree:
    """
    A Binary Search Tree implementation with comprehensive functionality.
    
    This class provides methods for inserting, searching, deleting nodes,
    finding minimum/maximum values, and performing tree traversals.
    """
    
    def __init__(self) -> None:
        """Initialize an empty Binary Search Tree."""
        self.root: Optional[TreeNode] = None
        self._size: int = 0
    
    @property
    def size(self) -> int:
        """Return the number of nodes in the tree."""
        return self._size
    
    @property
    def is_empty(self) -> bool:
        """Return True if the tree is empty, False otherwise."""
        return self.root is None
    
    def insert(self, value: Any) -> None:
        """
        Insert a value into the Binary Search Tree.
        
        Args:
            value: The value to insert into the tree
            
        Raises:
            TypeError: If the value type is incompatible with existing values
        """
        if value is None:
            raise ValueError("Cannot insert None value into the tree")
        
        try:
            if self.root is None:
                self.root = TreeNode(value)
                self._size += 1
            else:
                self._insert_recursive(self.root, value)
        except TypeError as e:
            raise TypeError(f"Cannot compare value types: {e}")
    
    def _insert_recursive(self, node: TreeNode, value: Any) -> None:
        """
        Recursively insert a value into the tree.
        
        Args:
            node: The current node being examined
            value: The value to insert
        """
        try:
            if value < node.value:
                if node.left is None:
                    node.left = TreeNode(value)
                    self._size += 1
                else:
                    self._insert_recursive(node.left, value)
            elif value > node.value:
                if node.right is None:
                    node.right = TreeNode(value)
                    self._size += 1
                else:
                    self._insert_recursive(node.right, value)
            # If value == node.value, do nothing (no duplicates allowed)
        except TypeError:
            raise TypeError("Cannot compare values of different incompatible types")
    
    def search(self, value: Any) -> bool:
        """
        Search for a value in the Binary Search Tree.
        
        Args:
            value: The value to search for
            
        Returns:
            True if the value is found, False otherwise
            
        Raises:
            ValueError: If searching for None value
            TypeError: If the value type is incompatible with tree values
        """
        if value is None:
            raise ValueError("Cannot search for None value")
        
        if self.root is None:
            return False
        
        try:
            return self._search_recursive(self.root, value)
        except TypeError as e:
            raise TypeError(f"Cannot compare value types during search: {e}")
    
    def _search_recursive(self, node: Optional[TreeNode], value: Any) -> bool:
        """
        Recursively search for a value in the tree.
        
        Args:
            node: The current node being examined
            value: The value to search for
            
        Returns:
            True if the value is found, False otherwise
        """
        if node is None:
            return False
        
        if value == node.value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
    
    def delete(self, value: Any) -> bool:
        """
        Delete a value from the Binary Search Tree.
        
        Args:
            value: The value to delete
            
        Returns:
            True if the value was found and deleted, False otherwise
            
        Raises:
            ValueError: If trying to delete None value
            TypeError: If the value type is incompatible with tree values
        """
        if value is None:
            raise ValueError("Cannot delete None value")
        
        if self.root is None:
            return False
        
        try:
            self.root, deleted = self._delete_recursive(self.root, value)
            if deleted:
                self._size -= 1
            return deleted
        except TypeError as e:
            raise TypeError(f"Cannot compare value types during deletion: {e}")
    
    def _delete_recursive(self, node: Optional[TreeNode], value: Any) -> tuple[Optional[TreeNode], bool]:
        """
        Recursively delete a value from the tree.
        
        Args:
            node: The current node being examined
            value: The value to delete
            
        Returns:
            A tuple containing the updated node and a boolean indicating if deletion occurred
        """
        if node is None:
            return None, False
        
        if value < node.value:
            node.left, deleted = self._delete_recursive(node.left, value)
            return node, deleted
        elif value > node.value:
            node.right, deleted = self._delete_recursive(node.right, value)
            return node, deleted
        else:
            # Node to be deleted found
            # Case 1: Node has no children (leaf node)
            if node.left is None and node.right is None:
                return None, True
            
            # Case 2: Node has one child
            elif node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True
            
            # Case 3: Node has two children
            else:
                # Find the inorder successor (smallest value in right subtree)
                successor_value = self._find_min_value(node.right)
                node.value = successor_value
                node.right, _ = self._delete_recursive(node.right, successor_value)
                return node, True
    
    def _find_min_value(self, node: TreeNode) -> Any:
        """
        Find the minimum value in a subtree.
        
        Args:
            node: The root of the subtree
            
        Returns:
            The minimum value in the subtree
        """
        while node.left is not None:
            node = node.left
        return node.value
    
    def find_minimum(self) -> Any:
        """
        Find the minimum value in the Binary Search Tree.
        
        Returns:
            The minimum value in the tree
            
        Raises:
            ValueError: If the tree is empty
        """
        if self.root is None:
            raise ValueError("Cannot find minimum in empty tree")
        
        return self._find_min_value(self.root)
    
    def find_maximum(self) -> Any:
        """
        Find the maximum value in the Binary Search Tree.
        
        Returns:
            The maximum value in the tree
            
        Raises:
            ValueError: If the tree is empty
        """
        if self.root is None:
            raise ValueError("Cannot find maximum in empty tree")
        
        node = self.root
        while node.right is not None:
            node = node.right
        return node.value
    
    def inorder_traversal(self) -> List[Any]:
        """
        Perform an in-order traversal of the Binary Search Tree.
        
        In-order traversal visits nodes in ascending order for a BST:
        left subtree -> root -> right subtree
        
        Returns:
            A list containing all values in the tree in ascending order
        """
        result: List[Any] = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[TreeNode], result: List[Any]) -> None:
        """
        Recursively perform in-order traversal.
        
        Args:
            node: The current node being visited
            result: The list to append values to
        """
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    def __str__(self) -> str:
        """
        Return a string representation of the tree.
        
        Returns:
            String representation showing the in-order traversal
        """
        if self.is_empty:
            return "Empty BST"
        return f"BST({self.inorder_traversal()})"
    
    def __repr__(self) -> str:
        """
        Return a detailed string representation of the tree.
        
        Returns:
            Detailed string representation of the BST
        """
        return f"BinarySearchTree(size={self.size}, values={self.inorder_traversal()})"


if __name__ == "__main__":
    # Example usage and basic testing
    bst = BinarySearchTree()
    
    # Test insertions
    values = [50, 30, 70, 20, 40, 60, 80]
    for value in values:
        bst.insert(value)
    
    print(f"Tree size: {bst.size}")
    print(f"In-order traversal: {bst.inorder_traversal()}")
    print(f"Minimum value: {bst.find_minimum()}")
    print(f"Maximum value: {bst.find_maximum()}")
    
    # Test search
    print(f"Search 40: {bst.search(40)}")
    print(f"Search 90: {bst.search(90)}")
    
    # Test deletion
    print(f"Delete 30: {bst.delete(30)}")
    print(f"After deletion: {bst.inorder_traversal()}")
    
    print(bst)