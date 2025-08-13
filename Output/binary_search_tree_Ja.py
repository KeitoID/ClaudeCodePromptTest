"""
Binary Search Tree implementation in Python.

This module provides a complete binary search tree implementation with
standard operations including insertion, deletion, search, and traversal.
"""

from typing import Optional, List, Any, Iterator


class TreeNode:
    """
    Represents a node in the binary search tree.

    Attributes:
        data: The value stored in the node.
        left: Reference to the left child node.
        right: Reference to the right child node.
    """

    def __init__(self, data: Any) -> None:
        """
        Initialize a tree node.

        Args:
            data: The value to store in the node.
        """
        self.data = data
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None


class BinarySearchTree:
    """
    A binary search tree implementation.

    This class provides methods for inserting, searching, and deleting nodes,
    as well as finding minimum and maximum values, and performing in-order
    traversal.
    """

    def __init__(self) -> None:
        """Initialize an empty binary search tree."""
        self.root: Optional[TreeNode] = None

    def insert(self, data: Any) -> None:
        """
        Insert a value into the binary search tree.

        Args:
            data: The value to insert into the tree.

        Raises:
            TypeError: If data is None.
        """
        if data is None:
            raise TypeError("Cannot insert None value into the tree")

        if self.root is None:
            self.root = TreeNode(data)
        else:
            self._insert_recursive(self.root, data)

    def _insert_recursive(self, node: TreeNode, data: Any) -> TreeNode:
        """
        Recursively insert a value into the tree.

        Args:
            node: The current node being examined.
            data: The value to insert.

        Returns:
            The node after insertion.
        """
        if data < node.data:
            if node.left is None:
                node.left = TreeNode(data)
            else:
                self._insert_recursive(node.left, data)
        elif data > node.data:
            if node.right is None:
                node.right = TreeNode(data)
            else:
                self._insert_recursive(node.right, data)

        return node

    def search(self, data: Any) -> bool:
        """
        Search for a value in the binary search tree.

        Args:
            data: The value to search for.

        Returns:
            True if the value is found, False otherwise.

        Raises:
            TypeError: If data is None.
        """
        if data is None:
            raise TypeError("Cannot search for None value")

        return self._search_recursive(self.root, data)

    def _search_recursive(self, node: Optional[TreeNode], data: Any) -> bool:
        """
        Recursively search for a value in the tree.

        Args:
            node: The current node being examined.
            data: The value to search for.

        Returns:
            True if the value is found, False otherwise.
        """
        if node is None:
            return False

        if data == node.data:
            return True
        elif data < node.data:
            return self._search_recursive(node.left, data)
        else:
            return self._search_recursive(node.right, data)

    def delete(self, data: Any) -> None:
        """
        Delete a value from the binary search tree.

        Args:
            data: The value to delete from the tree.

        Raises:
            TypeError: If data is None.
            ValueError: If the tree is empty or value is not found.
        """
        if data is None:
            raise TypeError("Cannot delete None value")

        if self.root is None:
            raise ValueError("Cannot delete from empty tree")

        if not self.search(data):
            raise ValueError(f"Value {data} not found in tree")

        self.root = self._delete_recursive(self.root, data)

    def _delete_recursive(self, node: Optional[TreeNode], data: Any) -> Optional[TreeNode]:
        """
        Recursively delete a value from the tree.

        Args:
            node: The current node being examined.
            data: The value to delete.

        Returns:
            The node after deletion.
        """
        if node is None:
            return None

        if data < node.data:
            node.left = self._delete_recursive(node.left, data)
        elif data > node.data:
            node.right = self._delete_recursive(node.right, data)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                successor = self._find_min_node(node.right)
                node.data = successor.data
                node.right = self._delete_recursive(node.right, successor.data)

        return node

    def find_min(self) -> Any:
        """
        Find the minimum value in the binary search tree.

        Returns:
            The minimum value in the tree.

        Raises:
            ValueError: If the tree is empty.
        """
        if self.root is None:
            raise ValueError("Cannot find minimum in empty tree")

        return self._find_min_node(self.root).data

    def _find_min_node(self, node: TreeNode) -> TreeNode:
        """
        Find the node with the minimum value starting from the given node.

        Args:
            node: The starting node.

        Returns:
            The node with the minimum value.
        """
        while node.left is not None:
            node = node.left
        return node

    def find_max(self) -> Any:
        """
        Find the maximum value in the binary search tree.

        Returns:
            The maximum value in the tree.

        Raises:
            ValueError: If the tree is empty.
        """
        if self.root is None:
            raise ValueError("Cannot find maximum in empty tree")

        return self._find_max_node(self.root).data

    def _find_max_node(self, node: TreeNode) -> TreeNode:
        """
        Find the node with the maximum value starting from the given node.

        Args:
            node: The starting node.

        Returns:
            The node with the maximum value.
        """
        while node.right is not None:
            node = node.right
        return node

    def in_order_traversal(self) -> List[Any]:
        """
        Perform in-order traversal of the binary search tree.

        Returns:
            A list containing all values in the tree in sorted order.
        """
        result: List[Any] = []
        self._in_order_recursive(self.root, result)
        return result

    def _in_order_recursive(self, node: Optional[TreeNode], result: List[Any]) -> None:
        """
        Recursively perform in-order traversal.

        Args:
            node: The current node being visited.
            result: The list to store traversal results.
        """
        if node is not None:
            self._in_order_recursive(node.left, result)
            result.append(node.data)
            self._in_order_recursive(node.right, result)

    def is_empty(self) -> bool:
        """
        Check if the binary search tree is empty.

        Returns:
            True if the tree is empty, False otherwise.
        """
        return self.root is None

    def size(self) -> int:
        """
        Get the number of nodes in the binary search tree.

        Returns:
            The number of nodes in the tree.
        """
        return self._size_recursive(self.root)

    def _size_recursive(self, node: Optional[TreeNode]) -> int:
        """
        Recursively calculate the size of the tree.

        Args:
            node: The current node being examined.

        Returns:
            The number of nodes in the subtree rooted at the given node.
        """
        if node is None:
            return 0
        return 1 + self._size_recursive(node.left) + self._size_recursive(node.right)

    def height(self) -> int:
        """
        Get the height of the binary search tree.

        Returns:
            The height of the tree (0 for empty tree, 1 for single node).
        """
        return self._height_recursive(self.root)

    def _height_recursive(self, node: Optional[TreeNode]) -> int:
        """
        Recursively calculate the height of the tree.

        Args:
            node: The current node being examined.

        Returns:
            The height of the subtree rooted at the given node.
        """
        if node is None:
            return 0
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        return 1 + max(left_height, right_height)

    def __str__(self) -> str:
        """
        String representation of the binary search tree.

        Returns:
            A string representation showing the in-order traversal.
        """
        if self.is_empty():
            return "Empty BST"
        return f"BST: {self.in_order_traversal()}"

    def __len__(self) -> int:
        """
        Get the number of nodes in the tree using len() function.

        Returns:
            The number of nodes in the tree.
        """
        return self.size()

    def __contains__(self, data: Any) -> bool:
        """
        Check if a value exists in the tree using 'in' operator.

        Args:
            data: The value to search for.

        Returns:
            True if the value exists, False otherwise.
        """
        try:
            return self.search(data)
        except TypeError:
            return False