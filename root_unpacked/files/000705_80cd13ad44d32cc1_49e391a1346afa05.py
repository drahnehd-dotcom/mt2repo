# -*- coding: utf-8 -*-
"""
Mouse Module
Handles mouse cursor and drag-drop operations
"""

import app
import grpImage
import item
import wndMgr
import player
import skill
import dbg
import ui
import systemSetting


def SlotTypeToWindowType(slotType):
    """Convert slot type to window type"""
    return ({
        player.SLOT_TYPE_INVENTORY: player.INVENTORY,
        player.SLOT_TYPE_SAFEBOX: player.SAFEBOX,
        player.SLOT_TYPE_MALL: player.MALL,
        player.SLOT_TYPE_DRAGON_SOUL_INVENTORY: player.DRAGON_SOUL_INVENTORY,
    }).get(slotType, None)


class CursorImage:
    """Cursor image handler"""
    
    def __init__(self, imageName=None):
        self.handle = 0
        if imageName:
            self.LoadImage(imageName)

    def __del__(self):
        if self.handle:
            grpImage.Delete(self.handle)

    def LoadImage(self, imageName):
        """Load cursor image"""
        try:
            self.handle = grpImage.Generate(imageName)
        except Exception:
            import sys
            dbg.TraceError("{} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
            self.handle = 0

    def DeleteImage(self):
        """Delete cursor image"""
        if self.handle:
            grpImage.Delete(self.handle)
            self.handle = 0

    def IsImage(self):
        """Check if image is loaded"""
        return bool(self.handle)

    def SetPosition(self, x, y):
        """Set cursor position"""
        if self.handle:
            grpImage.SetPosition(self.handle, x, y)

    def Render(self):
        """Render cursor"""
        if self.handle:
            grpImage.Render(self.handle)


class CMouseController:
    """Main mouse controller class"""

    def __init__(self):
        self.x = 0
        self.y = 0

        self.IsSoftwareCursor = False
        self.curCursorName = ""
        self.curCursorImage = 0
        self.cursorPosX = 0
        self.cursorPosY = 0

        self.AttachedIconHandle = 0
        self.AttachedOwner = 0
        self.AttachedFlag = False
        self.AttachedType = 0
        self.AttachedSlotNumber = 0
        self.AttachedCount = 1
        self.AttachedIconHalfWidth = 0
        self.AttachedIconHalfHeight = 0
        self.LastAttachedSlotNumber = 0

        self.countNumberLine = None
        self.callbackDict = {}

        self.DeattachObject()

    def __del__(self):
        self.Destroy()

    def Destroy(self):
        """Cleanup resources"""
        self.callbackDict = {}
        self.countNumberLine = None

    def Create(self):
        """Initialize mouse controller"""
        self.IsSoftwareCursor = systemSetting.IsSoftwareCursor()

        self.cursorDict = {
            app.NORMAL          : CursorImage("D:/Ymir Work/UI/Cursor/cursor.sub"),
            app.ATTACK          : CursorImage("D:/Ymir Work/UI/Cursor/cursor_attack.sub"),
            app.TARGET          : CursorImage("D:/Ymir Work/UI/Cursor/cursor_attack.sub"),
            app.TALK            : CursorImage("D:/Ymir Work/UI/Cursor/cursor_talk.sub"),
            app.CANT_GO         : CursorImage("D:/Ymir Work/UI/Cursor/cursor_no.sub"),
            app.PICK            : CursorImage("D:/Ymir Work/UI/Cursor/cursor_pick.sub"),
            app.DOOR            : CursorImage("D:/Ymir Work/UI/Cursor/cursor_door.sub"),
            app.CHAIR           : CursorImage("D:/Ymir Work/UI/Cursor/cursor_chair.sub"),
            app.MAGIC           : CursorImage("D:/Ymir Work/UI/Cursor/cursor_chair.sub"),
            app.BUY             : CursorImage("D:/Ymir Work/UI/Cursor/cursor_buy.sub"),
            app.SELL            : CursorImage("D:/Ymir Work/UI/Cursor/cursor_sell.sub"),
            app.CAMERA_ROTATE   : CursorImage("D:/Ymir Work/UI/Cursor/cursor_camera_rotate.sub"),
            app.HSIZE           : CursorImage("D:/Ymir Work/UI/Cursor/cursor_hsize.sub"),
            app.VSIZE           : CursorImage("D:/Ymir Work/UI/Cursor/cursor_vsize.sub"),
            app.HVSIZE          : CursorImage("D:/Ymir Work/UI/Cursor/cursor_hvsize.sub"),
        }
        self.cursorPosDict = {
            app.NORMAL          : (0, 0),
            app.TARGET          : (0, 0),
            app.ATTACK          : (0, 0),
            app.TALK            : (0, 0),
            app.CANT_GO         : (0, 0),
            app.PICK            : (0, 0),
            app.DOOR            : (0, 0),
            app.CHAIR           : (0, 0),
            app.MAGIC           : (0, 0),
            app.BUY             : (0, 0),
            app.SELL            : (0, 0),
            app.CAMERA_ROTATE   : (0, 0),
            app.HSIZE           : (-16, -16),
            app.VSIZE           : (-16, -16),
            app.HVSIZE          : (-16, -16),
        }

        app.SetCursor(app.NORMAL)

        self.countNumberLine = ui.NumberLine("CURTAIN")
        self.countNumberLine.SetHorizontalAlignCenter()
        self.countNumberLine.Hide()

        return True

    def ChangeCursor(self, cursorNum):
        """Change active cursor"""
        try:
            self.curCursorNum = cursorNum
            self.curCursorImage = self.cursorDict[cursorNum]
            (self.cursorPosX, self.cursorPosY) = self.cursorPosDict[cursorNum]

            if not self.curCursorImage.IsImage():
                self.curCursorNum = app.NORMAL
                self.curCursorImage = self.cursorDict[app.NORMAL]

        except KeyError:
            dbg.TraceError("mouseModule.MouseController.SetCursor [{}]".format(cursorNum))
            self.curCursorName = app.NORMAL
            self.curCursorImage = self.cursorDict[app.NORMAL]

    def AttachObject(self, Owner, Type, SlotNumber, ItemIndex, count=0):
        """Attach object to cursor for drag-drop"""
        self.LastAttachedSlotNumber = self.AttachedSlotNumber

        self.AttachedFlag = True
        self.AttachedOwner = Owner
        self.AttachedType = Type
        self.AttachedSlotNumber = SlotNumber
        self.AttachedItemIndex = ItemIndex
        self.AttachedCount = count
        self.countNumberLine.SetNumber("")
        self.countNumberLine.Hide()

        if count > 1:
            self.countNumberLine.SetNumber(str(count))
            self.countNumberLine.Show()

        try:
            width = 1
            height = 1

            if Type in (player.SLOT_TYPE_INVENTORY,
                        player.SLOT_TYPE_PRIVATE_SHOP,
                        player.SLOT_TYPE_SHOP,
                        player.SLOT_TYPE_SAFEBOX,
                        player.SLOT_TYPE_MALL,
                        player.SLOT_TYPE_DRAGON_SOUL_INVENTORY,
                        player.SLOT_TYPE_SWITCHBOT,
                        player.SLOT_TYPE_SKILL_BOOK_INVENTORY,
                        player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY,
                        player.SLOT_TYPE_STONE_INVENTORY,
                        player.SLOT_TYPE_BOX_INVENTORY,
                        player.SLOT_TYPE_EFSUN_INVENTORY,
                        player.SLOT_TYPE_CICEK_INVENTORY):

                item.SelectItem(self.AttachedItemIndex)
                self.AttachedIconHandle = item.GetIconInstance()

                if not self.AttachedIconHandle:
                    self.AttachedIconHandle = 0
                    self.DeattachObject()
                    return

                (width, height) = item.GetItemSize()

            elif Type == player.SLOT_TYPE_SKILL:
                skillGrade = player.GetSkillGrade(SlotNumber)
                self.AttachedIconHandle = skill.GetIconInstanceNew(self.AttachedItemIndex, skillGrade)

            elif Type == player.SLOT_TYPE_EMOTION:
                image = player.GetEmotionIconImage(ItemIndex)
                self.AttachedIconHandle = grpImage.GenerateFromHandle(image)

            elif Type == player.SLOT_TYPE_QUICK_SLOT:
                (quickSlotType, position) = player.GetGlobalQuickSlot(SlotNumber)

                if quickSlotType == player.SLOT_TYPE_INVENTORY:
                    itemIndex = player.GetItemIndex(position)
                    item.SelectItem(itemIndex)
                    self.AttachedIconHandle = item.GetIconInstance()
                    (width, height) = item.GetItemSize()

                elif quickSlotType == player.SLOT_TYPE_SKILL:
                    skillIndex = player.GetSkillIndex(position)
                    skillGrade = player.GetSkillGrade(position)
                    self.AttachedIconHandle = skill.GetIconInstanceNew(skillIndex, skillGrade)

                elif quickSlotType == player.SLOT_TYPE_EMOTION:
                    image = player.GetEmotionIconImage(position)
                    self.AttachedIconHandle = grpImage.GenerateFromHandle(image)

            if not self.AttachedIconHandle:
                self.DeattachObject()
                return

            self.AttachedIconHalfWidth = grpImage.GetWidth(self.AttachedIconHandle) // 2
            self.AttachedIconHalfHeight = grpImage.GetHeight(self.AttachedIconHandle) // 2
            wndMgr.AttachIcon(self.AttachedType, self.AttachedItemIndex, self.AttachedSlotNumber, width, height)

        except Exception as e:
            dbg.TraceError("mouseModule.py: AttachObject : {}".format(str(e)))
            self.AttachedIconHandle = 0

    def IsAttachedMoney(self):
        """Check if money is attached"""
        if self.isAttached():
            if player.ITEM_MONEY == self.GetAttachedItemIndex():
                return True
        return False

    def GetAttachedMoneyAmount(self):
        """Get attached money amount"""
        if self.isAttached():
            if player.ITEM_MONEY == self.GetAttachedItemIndex():
                return self.GetAttachedItemCount()
        return 0

    def AttachMoney(self, owner, type, count):
        """Attach money to cursor"""
        self.LastAttachedSlotNumber = self.AttachedSlotNumber

        self.AttachedFlag = True
        self.AttachedOwner = owner
        self.AttachedType = type
        self.AttachedSlotNumber = -1
        self.AttachedItemIndex = player.ITEM_MONEY
        self.AttachedCount = count
        self.AttachedIconHandle = grpImage.Generate("icon/item/money.tga")
        self.AttachedIconHalfWidth = grpImage.GetWidth(self.AttachedIconHandle) // 2
        self.AttachedIconHalfHeight = grpImage.GetHeight(self.AttachedIconHandle) // 2
        wndMgr.AttachIcon(self.AttachedType, self.AttachedItemIndex, self.AttachedSlotNumber, 1, 1)

        if count > 1:
            self.countNumberLine.SetNumber(str(count))
            self.countNumberLine.Show()

    if app.ENABLE_CHEQUE_SYSTEM:
        def AttacCheque(self, owner, type, count):
            """Attach cheque to cursor"""
            self.LastAttachedSlotNumber = self.AttachedSlotNumber
            self.AttachedFlag = True
            self.AttachedOwner = owner
            self.AttachedType = type
            self.AttachedSlotNumber = -2
            self.AttachedItemIndex = player.CHEQUE
            self.AttachedCount = count
            self.AttachedIconHandle = grpImage.Generate("icon/item/80020.tga")
            self.AttachedIconHalfWidth = grpImage.GetWidth(self.AttachedIconHandle) // 2
            self.AttachedIconHalfHeight = grpImage.GetHeight(self.AttachedIconHandle) // 2
            wndMgr.AttachIcon(self.AttachedType, self.AttachedItemIndex, self.AttachedSlotNumber, 1, 1)
            if count > 1:
                self.countNumberLine.SetNumber(str(count))
                self.countNumberLine.Show()

    def DeattachObject(self):
        """Detach object from cursor"""
        self.ClearCallBack()
        self.LastAttachedSlotNumber = self.AttachedSlotNumber

        if self.AttachedIconHandle != 0:
            if self.AttachedType in (player.SLOT_TYPE_INVENTORY,
                                      player.SLOT_TYPE_PRIVATE_SHOP,
                                      player.SLOT_TYPE_SHOP,
                                      player.SLOT_TYPE_SAFEBOX,
                                      player.SLOT_TYPE_MALL,
                                      player.SLOT_TYPE_SWITCHBOT,
                                      player.SLOT_TYPE_SKILL_BOOK_INVENTORY,
                                      player.SLOT_TYPE_UPGRADE_ITEMS_INVENTORY,
                                      player.SLOT_TYPE_STONE_INVENTORY,
                                      player.SLOT_TYPE_BOX_INVENTORY,
                                      player.SLOT_TYPE_EFSUN_INVENTORY,
                                      player.SLOT_TYPE_CICEK_INVENTORY):
                item.DeleteIconInstance(self.AttachedIconHandle)

            elif self.AttachedType == player.SLOT_TYPE_SKILL:
                skill.DeleteIconInstance(self.AttachedIconHandle)

            elif self.AttachedType == player.SLOT_TYPE_EMOTION:
                grpImage.Delete(self.AttachedIconHandle)

        self.AttachedFlag = False
        self.AttachedType = -1
        self.AttachedItemIndex = -1
        self.AttachedSlotNumber = -1
        self.AttachedIconHandle = 0
        wndMgr.SetAttachingFlag(False)

        if self.countNumberLine:
            self.countNumberLine.Hide()

    def isAttached(self):
        """Check if object is attached"""
        return self.AttachedFlag

    def GetAttachedOwner(self):
        """Get attached object owner"""
        if not self.isAttached():
            return 0
        return self.AttachedOwner

    def GetAttachedType(self):
        """Get attached object type"""
        if not self.isAttached():
            return player.SLOT_TYPE_NONE
        return self.AttachedType

    def GetAttachedSlotNumber(self):
        """Get attached slot number"""
        if not self.isAttached():
            return 0
        return self.AttachedSlotNumber

    def GetLastAttachedSlotNumber(self):
        """Get last attached slot number"""
        return self.LastAttachedSlotNumber

    def GetAttachedItemIndex(self):
        """Get attached item index"""
        if not self.isAttached():
            return 0
        return self.AttachedItemIndex

    def GetAttachedItemCount(self):
        """Get attached item count"""
        if not self.isAttached():
            return 0
        return self.AttachedCount

    def Update(self, x, y):
        """Update mouse position"""
        self.x = x
        self.y = y

        if self.isAttached():
            if self.AttachedIconHandle != 0:
                grpImage.SetDiffuseColor(self.AttachedIconHandle, 1.0, 1.0, 1.0, 0.5)
                grpImage.SetPosition(self.AttachedIconHandle, self.x - self.AttachedIconHalfWidth, self.y - self.AttachedIconHalfHeight)
                self.countNumberLine.SetPosition(self.x, self.y - self.AttachedIconHalfHeight - 3)

        if self.IsSoftwareCursor:
            if self.curCursorImage != 0:
                self.curCursorImage.SetPosition(self.x + self.cursorPosX, self.y + self.cursorPosY)

    def Render(self):
        """Render attached icon and cursor"""
        if self.isAttached():
            if self.AttachedIconHandle != 0:
                grpImage.Render(self.AttachedIconHandle)

        if self.IsSoftwareCursor:
            if app.IsShowCursor():
                if self.curCursorImage != 0:
                    self.curCursorImage.Render()
        else:
            if not app.IsShowCursor():
                if app.IsLiarCursorOn():
                    if self.curCursorImage != 0:
                        self.curCursorImage.SetPosition(self.x + self.cursorPosX, self.y + self.cursorPosY)
                        self.curCursorImage.Render()

    def SetCallBack(self, type, event=lambda *arg: None):
        """Set callback for drop event"""
        self.callbackDict[type] = event

    def RunCallBack(self, type, *arg):
        """Run callback for drop event"""
        if type not in self.callbackDict:
            self.DeattachObject()
            return

        self.callbackDict[type]()

    def ClearCallBack(self):
        """Clear all callbacks"""
        self.callbackDict = {}


# Global instance
mouseController = None
