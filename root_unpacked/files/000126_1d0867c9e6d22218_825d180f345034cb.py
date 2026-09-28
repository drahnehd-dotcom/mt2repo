#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Item Wrapper Module
Rewritten for Python 3 with better maintainability and cleaner code structure
"""

from __future__ import annotations

import dbg
import interfaceModule
import item
import player
import safebox
import uiToolTip
import exchange


__all__ = [
    "ItemWrapper",
    "ItemToolTipWrapper",
    "ItemToolTipDummy",
    "ItemToolTipOnlyTitleDummy",
    "ItemGridWrapper",
    "ItemContainer",
]


class ItemWrapper:
    """Wrapper class for items in various windows (inventory, safebox, mall)."""
    
    def __init__(self, window: int, position: int) -> None:
        self.__isActivated: bool = False
        
        self.__window: int = window
        self.__position: int = position
    
    def __del__(self) -> None:
        if self.IsActivated():
            self.Deactivate()
    
    def GetVnum(self):
        """Get the item vnum (virtual number)."""
        if self.GetWindow() in (player.INVENTORY, player.DRAGON_SOUL_INVENTORY):
            return player.GetItemIndex(self.GetWindow(), self.GetPosition())
        elif self.GetWindow() == player.SAFEBOX:
            return safebox.GetItemID(self.GetPosition())
        elif self.GetWindow() == player.MALL:
            return safebox.GetMallItemID(self.GetPosition())
        return None
    
    def GetCount(self):
        """Get the item count."""
        if self.GetWindow() in (player.INVENTORY, player.DRAGON_SOUL_INVENTORY):
            return player.GetItemCount(self.GetWindow(), self.GetPosition())
        elif self.GetWindow() == player.SAFEBOX:
            return safebox.GetItemCount(self.GetPosition())
        elif self.GetWindow() == player.MALL:
            return safebox.GetMallItemCount(self.GetPosition())
        return None
    
    def GetWindow(self) -> int:
        """Get the window type."""
        return self.__window
    
    def SetWindow(self, window: int) -> None:
        """Set the window type."""
        self.__window = window
    
    def GetPosition(self) -> int:
        """Get the position in the window."""
        return self.__position
    
    def SetPosition(self, position: int) -> None:
        """Set the position in the window."""
        self.__position = position
    
    def IsActivated(self) -> bool:
        """Check if the slot is activated."""
        return self.__isActivated
    
    def Activate(self, r: float = 1.0, g: float = 1.0, b: float = 1.0, a: float = 1.0) -> None:
        """Activate the slot with given color."""
        window = interfaceModule.GetInstance().GetWindowByType(self.GetWindow())
        if not window:
            return
        
        try:
            window.ActivateSlot(self.GetPosition(), r, g, b, a)
            self.__isActivated = True
        except Exception:
            dbg.TraceError(f"Not implemented method ActivateSlot for window {self.GetWindow()}.")
    
    def Deactivate(self) -> None:
        """Deactivate the slot."""
        window = interfaceModule.GetInstance().GetWindowByType(self.GetWindow())
        if not window:
            return
        
        try:
            window.DeactivateSlot(self.GetPosition())
            self.__isActivated = False
        except Exception:
            dbg.TraceError(f"Not implemented method DeactivateSlot for window {self.GetWindow()}.")


class ItemToolTipWrapper(ItemWrapper):
    """Item wrapper with tooltip functionality."""
    
    def __init__(self, window: int, position: int) -> None:
        super().__init__(window, position)
        
        self.__toolTip = uiToolTip.GetItemToolTipInstance()
    
    def GetToolTip(self):
        """Get the tooltip instance."""
        return self.__toolTip
    
    def ShowToolTip(self) -> None:
        """Show the tooltip for this item."""
        if not self.GetToolTip():
            return
        
        if self.GetWindow() in (player.INVENTORY, player.DRAGON_SOUL_INVENTORY):
            self.GetToolTip().SetInventoryItem(self.GetPosition(), self.GetWindow())
        elif self.GetWindow() == player.SAFEBOX:
            self.GetToolTip().SetSafeBoxItem(self.GetPosition())
        elif self.GetWindow() == player.MALL:
            self.GetToolTip().SetMallItem(self.GetPosition())
        else:
            raise Exception(f"Window type {self.GetWindow()} not supported.")
    
    def HideToolTip(self) -> None:
        """Hide the tooltip."""
        if not self.GetToolTip():
            return
        
        self.GetToolTip().HideToolTip()
    
    def AttachOnAddItemData(self, event: callable) -> None:
        """Attach event to be called when item data is added."""
        if not self.GetToolTip():
            return
        
        self.GetToolTip().AttachOnAddItemData(event)
    
    def DetachOnAddItemData(self, event: callable) -> None:
        """Detach event from when item data is added."""
        if not self.GetToolTip():
            return
        
        self.GetToolTip().DetachOnAddItemData(event)


class ItemToolTipDummy:
    """Dummy item tooltip for displaying item data without actual item."""
    
    def __init__(self, vnum, metinSlot = None, 
                 attrSlot = None, 
                 forceUseableColor = False) -> None:
        self.__vnum: int = vnum
        self.__metinSlot = metinSlot
        self.__attrSlot = attrSlot
        self.__forceUseableColor: bool = forceUseableColor
        
        if not self.__metinSlot:
            self.__metinSlot = [0] * player.METIN_SOCKET_MAX_NUM
        
        if not self.__attrSlot:
            self.__attrSlot = [(0, 0)] * player.ATTRIBUTE_SLOT_MAX_NUM
        
        self.__toolTip = uiToolTip.GetItemToolTipInstance()
        
        self.__shortcuts: list = []
    
    def __del__(self) -> None:
        self.__metinSlot = None
        self.__attrSlot = None
        
        self.__toolTip = None
        
        self.__shortcuts = None
    
    def GetVnum(self) -> int:
        """Get the item vnum."""
        return self.__vnum
    
    def SetVnum(self, vnum: int) -> None:
        """Set the item vnum."""
        self.__vnum = vnum
    
    def GetMetinSlot(self) -> list[int]:
        """Get the metin socket data."""
        return self.__metinSlot
    
    def SetMetinSlot(self, metinSlot: list[int]) -> None:
        """Set the metin socket data."""
        self.__metinSlot = metinSlot
    
    def GetAttrSlot(self) -> list[tuple[int, int]]:
        """Get the attribute slot data."""
        return self.__attrSlot
    
    def SetAttrSlot(self, attrSlot: list[tuple[int, int]]) -> None:
        """Set the attribute slot data."""
        self.__attrSlot = attrSlot
    
    def IsForceUseableColor(self) -> bool:
        """Check if force useable color is enabled."""
        return self.__forceUseableColor
    
    def SetForceUseableColor(self, forceUseableColor: bool) -> None:
        """Set force useable color."""
        self.__forceUseableColor = forceUseableColor
    
    def SetShortcuts(self, shortcuts: list) -> None:
        """Set keyboard shortcuts to display in tooltip."""
        self.__shortcuts = shortcuts
    
    def GetToolTip(self):
        """Get the tooltip instance."""
        return self.__toolTip
    
    def ShowToolTip(self) -> None:
        """Show the tooltip with item data."""
        if not self.GetToolTip():
            return
        
        self.GetToolTip().ClearToolTip()
        self.GetToolTip().SetCannotUseItemForceSetDisableColor(not self.IsForceUseableColor())
        self.GetToolTip().AddItemData(self.GetVnum(), self.GetMetinSlot(), self.GetAttrSlot())
        
        if len(self.__shortcuts) > 0:
            self.GetToolTip().AppendSpace(5)
            
            for shortcut in self.__shortcuts:
                self.GetToolTip().AppendShortcut(*shortcut)
        
        self.GetToolTip().ShowToolTip()
    
    def HideToolTip(self) -> None:
        """Hide the tooltip."""
        if not self.GetToolTip():
            return
        
        self.GetToolTip().HideToolTip()


class ItemToolTipOnlyTitleDummy:
    """Dummy item tooltip that only displays the item title/name."""
    
    def __init__(self, vnum: int, color: int = uiToolTip.ToolTip.TITLE_COLOR, 
                 postfix: str = "") -> None:
        self.__vnum: int = vnum
        self.__color: int = color
        self.__postfix: str = postfix
        
        self.__toolTip = uiToolTip.GetItemToolTipInstance()
    
    def GetVnum(self) -> int:
        """Get the item vnum."""
        return self.__vnum
    
    def SetVnum(self, vnum: int) -> None:
        """Set the item vnum."""
        self.__vnum = vnum
    
    def GetColor(self) -> int:
        """Get the title color."""
        return self.__color
    
    def SetColor(self, color: int) -> None:
        """Set the title color."""
        self.__color = color
    
    def GetPostfix(self) -> str:
        """Get the postfix string."""
        return self.__postfix
    
    def SetPostfix(self, postfix: str) -> None:
        """Set the postfix string."""
        self.__postfix = postfix
    
    def GetToolTip(self):
        """Get the tooltip instance."""
        return self.__toolTip
    
    def ShowToolTip(self) -> None:
        """Show the tooltip with only title."""
        if not self.GetToolTip():
            return
        
        item.SelectItem(self.GetVnum())
        
        self.GetToolTip().ClearToolTip()
        self.GetToolTip().AppendTextLine(item.GetItemName() + self.GetPostfix(), self.GetColor())
        self.GetToolTip().ShowToolTip()
    
    def HideToolTip(self) -> None:
        """Hide the tooltip."""
        if not self.GetToolTip():
            return
        
        self.GetToolTip().HideToolTip()


class ItemGridWrapper(ItemWrapper):
    """Item wrapper with grid size information."""
    
    def __init__(self, window: int, position: int) -> None:
        super().__init__(window, position)
        
        item.SelectItem(self.GetVnum())
        _, self.__size = item.GetItemSize()
    
    def GetSize(self) -> int:
        """Get the item size in grid slots."""
        return self.__size


class ItemContainer:
    """Container for managing multiple items."""
    
    def __init__(self) -> None:
        self.items: dict[int, ItemWrapper] = {}
        self.onSetItem = None
    
    def __del__(self) -> None:
        self.items = {}
        self.onSetItem = None
    
    def Clear(self) -> None:
        """Clear all items from container."""
        slotIndices = list(self.items.keys())
        
        self.items = {}
        
        for slotIndex in slotIndices:
            self.OnSetItem(slotIndex)
    
    def SetItem(self, slotIndex, i) -> None:
        """Set an item at the given slot index."""
        if not i and slotIndex in self.items:
            del self.items[slotIndex]
        else:
            self.items[slotIndex] = i
        
        self.OnSetItem(slotIndex)
    
    def GetItem(self, slotIndex):
        """Get the item at the given slot index."""
        return self.items.get(slotIndex, None)
    
    def GetItemCount(self) -> int:
        """Get the total number of items in container."""
        return len(self.items)
    
    def GetVnum(self, slotIndex: int) -> int:
        """Get the vnum of item at given slot index."""
        i = self.GetItem(slotIndex)
        if not i:
            return 0
        
        return i.GetVnum()
    
    def GetCount(self, slotIndex: int) -> int:
        """Get the count of item at given slot index."""
        i = self.GetItem(slotIndex)
        if not i:
            return 0
        
        return i.GetCount()
    
    def SetOnSetItem(self, event: callable) -> None:
        """Set callback for when an item is set."""
        self.onSetItem = event
    
    def OnSetItem(self, slotIndex: int) -> None:
        """Call the onSetItem callback if set."""
        if self.onSetItem:
            self.onSetItem(slotIndex)
    
    def __iter__(self):
        """Iterate over items in container."""
        return iter(self.items.items())
