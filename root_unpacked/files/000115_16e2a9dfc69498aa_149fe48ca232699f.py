# -*- coding: utf-8 -*-
"""
Grid System Module

This module provides a grid-based inventory system for managing items with different sizes.
Supports multi-page grids and provides iteration capabilities.
"""

import item


class IItem(object):
    """Interface for items that can be placed in a grid"""
    
    def __init__(self):
        pass
    
    def GetSize(self):
        """
        Get the size of the item (how many grid slots it occupies vertically)
        
        Returns:
            int: Size of the item
            
        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("GetSize method must be implemented by subclasses")


class SizeItem(IItem):
    """Item implementation with a fixed size"""
    
    def __init__(self, size):
        """
        Initialize a size item.
        
        Args:
            size (int): Size of the item in grid slots
        """
        super(SizeItem, self).__init__()
        self.__size = size
    
    def GetSize(self):
        """
        Get the size of this item.
        
        Returns:
            int: Size of the item
        """
        return self.__size


class Grid(object):
    """
    A grid-based storage system for items.
    
    Supports multiple pages and items of different sizes.
    Items are placed vertically and can occupy multiple consecutive slots.
    """
    
    class Iterator(object):
        """Iterator for grid items"""
        
        def __init__(self, grid):
            """
            Initialize grid iterator.
            
            Args:
                grid (Grid): Grid instance to iterate over
            """
            self.__grid = grid
            self.__pos = 0
        
        def __next__(self):
            """
            Get next item in iteration.
            
            Returns:
                object: Next item in grid
                
            Raises:
                StopIteration: When iteration is complete
            """
            if self.__pos >= self.__grid.GetSize():
                raise StopIteration
            else:
                self.__pos += 1
                return self.__grid.GetGlobal(self.__pos - 1)
        
        def next(self):
            """Python 2 compatibility method for iteration"""
            return self.__next__()
    
    def __init__(self, width, height, pages=1):
        """
        Initialize a new grid.
        
        Args:
            width (int): Width of the grid (columns)
            height (int): Height of the grid (rows)
            pages (int): Number of pages in the grid (default: 1)
        """
        self.__width = width
        self.__height = height
        self.__pages = pages
        
        self.Initialize()
    
    def Initialize(self):
        """Initialize the grid data structure"""
        self.__size = self.GetWidth() * self.GetHeight() * self.GetPages()
        self.__items = [None for _ in range(self.GetSize())]
    
    def ToGlobalPosition(self, x, y, z):
        """
        Convert local coordinates to global position.
        
        Args:
            x (int): Column position
            y (int): Row position
            z (int): Page number
            
        Returns:
            int: Global position index
        """
        return (self.GetWidth() * self.GetHeight() * z + 
                self.GetWidth() * y + 
                x)
    
    def ToLocalPosition(self, position):
        """
        Convert global position to local coordinates.
        
        Args:
            position (int): Global position index
            
        Returns:
            tuple: (x, y, z) coordinates
        """
        page = position // (self.GetWidth() * self.GetHeight())
        position = position % (self.GetWidth() * self.GetHeight())
        row = position // self.GetWidth()
        col = position % self.GetWidth()
        
        return (col, row, page)
    
    def Put(self, item, x, y, z):
        """
        Put an item at specific coordinates.
        
        Args:
            item (IItem): Item to place
            x (int): Column position
            y (int): Row position
            z (int): Page number
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.PutGlobal(item, self.ToGlobalPosition(x, y, z))
    
    def PutGlobal(self, item, position):
        """
        Put an item at a global position.
        
        Args:
            item (IItem): Item to place
            position (int): Global position index
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.IsBlankGlobal(item, position):
            return False
        
        self.__items[position] = item
        return True
    
    def Get(self, x, y, z):
        """
        Get item at specific coordinates.
        
        Args:
            x (int): Column position
            y (int): Row position
            z (int): Page number
            
        Returns:
            object: Item at position or None if empty
        """
        return self.GetGlobal(self.ToGlobalPosition(x, y, z))
    
    def GetGlobal(self, position):
        """
        Get item at global position.
        
        Args:
            position (int): Global position index
            
        Returns:
            object: Item at position or None if empty
        """
        if 0 <= position < len(self.__items):
            return self.__items[position]
        return None
    
    def Clear(self, x, y, z):
        """
        Clear item at specific coordinates.
        
        Args:
            x (int): Column position
            y (int): Row position
            z (int): Page number
            
        Returns:
            object: Removed item or None if empty
        """
        return self.ClearGlobal(self.ToGlobalPosition(x, y, z))
    
    def ClearGlobal(self, position):
        """
        Clear item at global position.
        
        Args:
            position (int): Global position index
            
        Returns:
            object: Removed item or None if empty
        """
        if 0 <= position < len(self.__items):
            item = self.__items[position]
            self.__items[position] = None
            return item
        return None
    
    def IsBlank(self, item, x, y, z):
        """
        Check if an item can be placed at specific coordinates.
        
        Args:
            item (IItem): Item to check placement for
            x (int): Column position
            y (int): Row position
            z (int): Page number
            
        Returns:
            bool: True if item can be placed, False otherwise
        """
        # Check if item would exceed grid height
        if (y + item.GetSize()) > self.GetHeight():
            return False
        
        # Check if any slot the item would occupy is already taken
        for size_offset in range(item.GetSize()):
            if self.Get(x, y + size_offset, z):
                return False
        
        # Check if any item above would overlap with this item
        if y > 0:
            for row in range(y - 1, -1, -1):
                item_above = self.Get(x, row, z)
                if item_above:
                    # If item above extends into our placement area
                    if (row + item_above.GetSize()) > y:
                        return False
                    # Found an item that doesn't overlap, stop checking
                    break
        
        return True
    
    def IsBlankGlobal(self, item, position):
        """
        Check if an item can be placed at a global position.
        
        Args:
            item (IItem): Item to check placement for
            position (int): Global position index
            
        Returns:
            bool: True if item can be placed, False otherwise
        """
        x, y, z = self.ToLocalPosition(position)
        return self.IsBlank(item, x, y, z)
    
    def FindBlank(self, item):
        """
        Find the first available position for an item.
        
        Args:
            item (IItem): Item to find space for
            
        Returns:
            int: Global position index or -1 if no space available
        """
        extra_space = item.GetSize() - 1
        
        for page in range(self.GetPages()):
            for row in range(self.GetHeight() - extra_space):
                for col in range(self.GetWidth()):
                    if self.IsBlank(item, col, row, page):
                        return self.ToGlobalPosition(col, row, page)
        
        return -1
    
    def GetWidth(self):
        """Get grid width"""
        return self.__width
    
    def GetHeight(self):
        """Get grid height"""
        return self.__height
    
    def GetPages(self):
        """Get number of pages"""
        return self.__pages
    
    def GetSize(self):
        """Get total number of slots in grid"""
        return self.__size
    
    def GetItemCount(self):
        """
        Get number of items currently in the grid.
        
        Returns:
            int: Number of non-None items
        """
        return sum(1 for item in self.__items if item is not None)
    
    def IsEmpty(self):
        """
        Check if grid is completely empty.
        
        Returns:
            bool: True if no items in grid
        """
        return self.GetItemCount() == 0
    
    def IsFull(self):
        """
        Check if grid is completely full.
        
        Returns:
            bool: True if all slots are occupied
        """
        return self.GetItemCount() == self.GetSize()
    
    def GetItems(self):
        """
        Get all non-None items in the grid.
        
        Returns:
            list: List of items in the grid
        """
        return [item for item in self.__items if item is not None]
    
    def ClearAll(self):
        """Clear all items from the grid"""
        self.__items = [None for _ in range(self.GetSize())]
    
    def __iter__(self):
        """Make grid iterable"""
        return self.Iterator(self)
    
    def __len__(self):
        """Get total grid size"""
        return self.GetSize()
    
    def __str__(self):
        """String representation of grid"""
        return "Grid({}x{}x{}, {} items)".format(
            self.GetWidth(), 
            self.GetHeight(), 
            self.GetPages(),
            self.GetItemCount()
        )