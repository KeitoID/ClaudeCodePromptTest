"""
Binary Search Tree implementation with comprehensive functionality.

This module provides a complete Binary Search Tree (BST) implementation
with insertion, deletion, searching, traversal, and utility methods.
"""

from typing import Optional, List, Any


class BSTNode:
    """
    Node class for Binary Search Tree.
    
    Attributes:
        value: The value stored in the node
        left: Reference to the left child node
        right: Reference to the right child node
    """
    
    def __init__(self, value: Any) -> None:
        """
        Initialize a BST node with the given value.
        
        Args:
            value: The value to store in the node
        """
        self.value = value
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None


class BinarySearchTree:
    """
    Binary Search Tree implementation with full functionality.
    
    A BST is a binary tree where for each node:
    - All values in the left subtree are less than the node's value
    - All values in the right subtree are greater than the node's value
    """
    
    def __init__(self) -> None:
        """Initialize an empty Binary Search Tree."""
        self.root: Optional[BSTNode] = None
    
    def insert(self, value: Any) -> None:
        """
        Insert a value into the Binary Search Tree.
        
        Args:
            value: The value to insert into the tree
            
        Raises:
            TypeError: If the value type is not comparable
        """
        try:
            if self.root is None:
                self.root = BSTNode(value)
            else:
                self._insert_recursive(self.root, value)
        except TypeError as e:
            raise TypeError(f"Cannot insert non-comparable value: {e}")
    
    def _insert_recursive(self, node: BSTNode, value: Any) -> None:
        """
        Recursively insert a value into the tree.
        
        Args:
            node: The current node in the recursion
            value: The value to insert
        """
        if value < node.value:
            if node.left is None:
                node.left = BSTNode(value)
            else:
                self._insert_recursive(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = BSTNode(value)
            else:
                self._insert_recursive(node.right, value)
    
    def search(self, value: Any) -> bool:
        """
        Search for a value in the Binary Search Tree.
        
        Args:
            value: The value to search for
            
        Returns:
            True if the value is found, False otherwise
            
        Raises:
            TypeError: If the value type is not comparable with tree values
        """
        if self.root is None:
            return False
        
        try:
            return self._search_recursive(self.root, value)
        except TypeError as e:
            raise TypeError(f"Cannot search for non-comparable value: {e}")
    
    def _search_recursive(self, node: Optional[BSTNode], value: Any) -> bool:
        """
        Recursively search for a value in the tree.
        
        Args:
            node: The current node in the recursion
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
            TypeError: If the value type is not comparable with tree values
        """
        if self.root is None:
            return False
        
        try:
            self.root, deleted = self._delete_recursive(self.root, value)
            return deleted
        except TypeError as e:
            raise TypeError(f"Cannot delete non-comparable value: {e}")
    
    def _delete_recursive(self, node: Optional[BSTNode], value: Any) -> tuple[Optional[BSTNode], bool]:
        """
        Recursively delete a value from the tree.
        
        Args:
            node: The current node in the recursion
            value: The value to delete
            
        Returns:
            A tuple of (updated_node, deletion_success)
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
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True
            else:
                successor = self._find_min_node(node.right)
                node.value = successor.value
                node.right, _ = self._delete_recursive(node.right, successor.value)
                return node, True
    
    def find_min(self) -> Any:
        """
        Find the minimum value in the Binary Search Tree.
        
        Returns:
            The minimum value in the tree
            
        Raises:
            ValueError: If the tree is empty
        """
        if self.root is None:
            raise ValueError("Cannot find minimum value in empty tree")
        
        return self._find_min_node(self.root).value
    
    def _find_min_node(self, node: BSTNode) -> BSTNode:
        """
        Find the node with the minimum value in a subtree.
        
        Args:
            node: The root of the subtree
            
        Returns:
            The node with the minimum value
        """
        while node.left is not None:
            node = node.left
        return node
    
    def find_max(self) -> Any:
        """
        Find the maximum value in the Binary Search Tree.
        
        Returns:
            The maximum value in the tree
            
        Raises:
            ValueError: If the tree is empty
        """
        if self.root is None:
            raise ValueError("Cannot find maximum value in empty tree")
        
        return self._find_max_node(self.root).value
    
    def _find_max_node(self, node: BSTNode) -> BSTNode:
        """
        Find the node with the maximum value in a subtree.
        
        Args:
            node: The root of the subtree
            
        Returns:
            The node with the maximum value
        """
        while node.right is not None:
            node = node.right
        return node
    
    def inorder_traversal(self) -> List[Any]:
        """
        Perform in-order traversal of the Binary Search Tree.
        
        In-order traversal visits nodes in ascending order for a BST.
        
        Returns:
            A list containing all values in the tree in ascending order
        """
        result: List[Any] = []
        if self.root is not None:
            self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[BSTNode], result: List[Any]) -> None:
        """
        Recursively perform in-order traversal.
        
        Args:
            node: The current node in the recursion
            result: The list to store the traversal result
        """
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    def is_empty(self) -> bool:
        """
        Check if the tree is empty.
        
        Returns:
            True if the tree is empty, False otherwise
        """
        return self.root is None
    
    def size(self) -> int:
        """
        Get the number of nodes in the tree.
        
        Returns:
            The number of nodes in the tree
        """
        return self._size_recursive(self.root)
    
    def _size_recursive(self, node: Optional[BSTNode]) -> int:
        """
        Recursively count the number of nodes in a subtree.
        
        Args:
            node: The root of the subtree
            
        Returns:
            The number of nodes in the subtree
        """
        if node is None:
            return 0
        return 1 + self._size_recursive(node.left) + self._size_recursive(node.right)


if __name__ == "__main__":
    bst = BinarySearchTree()
    
    values = [50, 30, 70, 20, 40, 60, 80]
    for value in values:
        bst.insert(value)
    
    print("In-order traversal:", bst.inorder_traversal())
    print("Minimum value:", bst.find_min())
    print("Maximum value:", bst.find_max())
    print("Search for 40:", bst.search(40))
    print("Search for 90:", bst.search(90))
    
    print("Deleting 20...")
    bst.delete(20)
    print("In-order traversal after deletion:", bst.inorder_traversal())