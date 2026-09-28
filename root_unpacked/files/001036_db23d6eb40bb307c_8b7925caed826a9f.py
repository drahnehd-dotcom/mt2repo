import app, net, chrmgr, player, app, item, _weakref
from _weakref import proxy, ref

from math import floor
from ui import ExpandedImageBox
from ui import Window, ImageBox, AutoGrowingVerticalContainer, TextLine

class CallbackSavedArgs(object):
	def __init__(self, cls, obj, func, args):
		object.__init__(self)
		self.cls = cls
		self.objRef = ref(obj)
		self.func = proxy(func)
		self.args = args
	
	def __call__(self, *args):
		if self.objRef:
			return self.func(self.objRef(), *self.args)
	
	def __bool__(self):
		return bool(self.objRef)

class CallbackNoArgs(object):
	def __init__(self, cls, obj, func):
		object.__init__(self)
		self.cls = cls
		self.objRef = ref(obj)
		self.func = proxy(func)
	
	def __call__(self, *args):
		if self.objRef:
			return self.func(self.objRef())
	
	def __bool__(self):
		return bool(self.objRef)

class Callback(object):
	def __init__(self, cls, obj, func):
		object.__init__(self)
		self.cls = cls
		self.objRef = ref(obj)
		self.func = proxy(func)
	
	def __call__(self, *args):
		if self.objRef:
			return self.func(self.objRef(), *args)
	
	def __bool__(self):
		return bool(self.objRef)

class AutoGrowingVerticalContainerEx(AutoGrowingVerticalContainer):
	def __init__(self):
		AutoGrowingVerticalContainer.__init__(self)
		self.elementsPerRow = 1
		self.elementHorizontalPadding = (0, 0)

		self.elementStartOffSetY = 0

		self.elementCurrentOffSetY = 0

		self.elementOffSetX = 0

		self.oldItems = []

		self.__lockedItems = {}

	def SetElementsPerRow(self, count):
		self.elementsPerRow = count

	def SetStartOffSetWindowPadding(self, lPadding = (0, 0)):
		self.elementHorizontalPadding = lPadding

	def SetStartOffSetY(self, offset):
		self.elementStartOffSetY = offset
		self.height = offset

	def AppendItem(self, item, index = -1):
		if self.height == 0:
			self.height += item.GetHeight() + self.elementCurrentOffSetY

		xPos, bAddHeight = self.Calculate(item)
		if (bAddHeight):
			addHeight = item.GetHeight() + self.elementOffSetY
			self.height += addHeight

		if index == -1:
			self.containerItems.append(item)

		self.containerItems[index].SetPosition(xPos + self.elementHorizontalPadding[0], self.height - self.containerItems[index].GetHeight())
		self.Update()
	
	def RemoveItem(self, item):
		if not item in self.containerItems: return
		self.containerItems.remove(item)

		self.RecalculateHeight()

	def RemoveAllItems(self):
		self.containerItems = []
		self.RecalculateHeight()

	def Calculate(self, item):
		return (len(self.containerItems) % self.elementsPerRow * (item.GetWidth() + self.elementHorizontalPadding[1]),
		bool(floor(
			(len(self.containerItems) / self.elementsPerRow)
			) * (item.GetHeight())
		))

	def ShowItems(self):
		if self.GetLockState():
			return

		for item in self.containerItems:
			item.Show()

	def HideItems(self):
		if self.GetLockState():
			return

		for item in self.containerItems:
			item.Hide()

	def GetItems(self):
		return self.containerItems

	def SetLockedItem(self, id = 0, state = True):
		if (state == False):
			for lockedItem in self.__lockedItems.keys():
				self.containerItems[lockedItem].SetApplyColor(0xFFffffff)

			self.__lockedItems.clear()

			self.RecalculateHeight()
			return

		if not self.GetLockState():
			self.SetStartOffSetY(0)

		self.HideItems()
		self.__lockedItems[id] = state

		self.containerItems[id].Show()
		self.containerItems[id].SetApplyColor(0xFF0E3D06)
		self.AppendItem(self.containerItems[id], id)

	def GetLockedItem(self, id):
		return self.__lockedItems.get(id, False)

	def GetLockState(self):
		return len(self.__lockedItems)

	def RecalculateHeight(self):
		self.oldItems = self.containerItems
		self.height = self.elementStartOffSetY
		self.containerItems = []

		for item in self.oldItems:
			self.AppendItem(item)

class ToggleAbleTitledWindow(Window):
	def __init__(self, imageFileName=None, icon=None, iconHide = None, scale = (1.0, 1.0)):
		Window.__init__(self)

		self.baseSize = [200, 20]
		self.eventsOpenCloseActive = True

		self.Elements = { "ICONS" : dict() }

		self.backgroundImage = ExpandedImageBox()
		self.backgroundImage.SAFE_SetStringEvent("MOUSE_LEFT_BUTTON_UP", self.OnMouseLeftButtonDoubleClick)
		self.backgroundImage.SetParent(self)
		self.backgroundImage.LoadImage(imageFileName)
		self.backgroundImage.Show()

		self.backgroundImage.SetScale(*scale)

		self.toggleIndicator = ImageBox()
		self.toggleIndicator.SetParent(self.backgroundImage)
		self.toggleIndicator.SAFE_SetStringEvent("MOUSE_LEFT_BUTTON_UP", self.OnToggle)
		self.toggleIndicator.SetWindowVerticalAlignCenter()
		self.toggleIndicator.SetWindowHorizontalAlignRight()
		self.toggleIndicator.SetPosition(10, 0)
		self.toggleIndicator.Show()

		self.titleText = TextLine()
		self.titleText.SetFontName("Verdana:12")
		self.titleText.SetParent(self.backgroundImage)
		self.titleText.SetPosition(30, -2)
		self.titleText.SetWindowHorizontalAlignLeft()
		self.titleText.SetWindowVerticalAlignCenter()
		self.titleText.Show()

		if icon:
			self.icon = ImageBox()
			self.icon.SAFE_SetStringEvent("MOUSE_LEFT_BUTTON_UP", self.OnMouseLeftButtonDoubleClick)
			self.icon.SetParent(self.backgroundImage)
			self.icon.LoadImage(icon)
			self.icon.SetWindowVerticalAlignCenter()
			self.icon.SetPosition(8, 0)
			self.icon.Show()
			self.Elements["ICONS"].update({
				'active' : icon
			})

		if iconHide:
			self.Elements["ICONS"].update({
				'deactive' : iconHide
			})


		self.toggleAbleContent = AutoGrowingVerticalContainerEx()
		self.toggleAbleContent.SetParent(self)
		self.toggleAbleContent.SetStartOffSetY(0)
		self.toggleAbleContent.SetPosition(0, self.backgroundImage.GetHeight())
		self.toggleAbleContent.Show()

		self.eventOnToggle = None
		self.eventOnGrow = None
		self.eventOpen = None
		self.eventClose = None
		self.toggleContentIsShown = False
		self.toggleShowFilename = ""
		self.toggleHideFilename = ""

		self.baseSize[1] = self.backgroundImage.GetHeight()
		self.width = 0

	def getContainer(self):
		return self.toggleAbleContent

	def getToggleState(self):
		return self.toggleContentIsShown

	def OnMouseLeftButtonDoubleClick(self):
		self.OnToggle()
		return True

	def SetOpenCloseEventStatus(self, status):
		self.eventsOpenCloseActive = status

	def SetWidth(self, width):
		self.toggleAbleContent.SetWidth(width)
		self.width = width
		self.SetSize(width, self.GetHeight())

	def SetTitle(self, title):
		self.titleText.SetText(title)

	def SetFontColor(self, tColors):
		self.titleText.SetFontColor(*tColors)

	def SetBackgroundImage(self, filename):
		self.backgroundImage = ExpandedImageBox()
		self.backgroundImage.SetParent(self)
		self.backgroundImage.LoadImage(filename)
		self.backgroundImage.Show()

	def SetToggleShowFilename(self, filename):
		self.toggleShowFilename = filename
		if not self.toggleContentIsShown:
			self.toggleIndicator.LoadImage(self.toggleShowFilename)

	def SetToggleHideFilename(self, filename):
		self.toggleHideFilename = filename
		if self.toggleContentIsShown:
			self.toggleIndicator.LoadImage(self.toggleHideFilename)

	def SetOnToggleEvent(self, event):
		self.eventOnToggle = MakeEvent(event)

	def SetOnGrowEvent(self, event):
		self.eventOnGrow = MakeEvent(event)

	def SetOpenEvent(self, event):
		self.eventOpen = MakeEvent(event)

	def SetCloseEvent(self, event):
		self.eventClose = MakeEvent(event)

	def AppendToToggleContent(self, item):
		self.toggleAbleContent.AppendItem(item)
		item.SetParent(self.toggleAbleContent)
		if self.eventOnGrow:
			self.eventOnGrow()
		self.Update()

	def Update(self):
		if self.toggleContentIsShown:
			self.SetSize(self.baseSize[0], self.baseSize[1] + self.toggleAbleContent.GetHeight())
		else:
			self.SetSize(*self.baseSize)
		self.UpdateRect()

	def Close(self):
		self.toggleAbleContent.Hide()
		self.toggleAbleContent.HideItems()

		self.toggleContentIsShown = False

		if self.icon:
			self.icon.LoadImage(self.Elements["ICONS"].get("active", ""))



	def Open(self):
		self.toggleAbleContent.Show()
		self.toggleAbleContent.ShowItems()
		self.toggleContentIsShown = True

		if self.icon:
			self.icon.LoadImage(self.Elements["ICONS"].get("deactive", ""))



	def OnToggle(self, bEditlineRequest = False, bKeepOpen = False):

		if (not bEditlineRequest and self.getContainer().GetLockState()):
			self.getContainer().SetLockedItem(state = False)

		self.eventsOpenCloseActive = False
		if self.toggleContentIsShown and not bKeepOpen:
			self.Close()
		else:
			self.Open()

		self.eventsOpenCloseActive = True

		if self.eventOnToggle:
			self.eventOnToggle()

def MakeCallback(func):
	try:
		if func.__func__.__code__.co_argcount > 1:
			return Callback(func.__self__.__class__, func.__self__, func.__func__)
		else:
			return CallbackNoArgs(func.__self__.__class__, func.__self__, func.__func__)
	except AttributeError:
		return func

class Event(object):
	def __init__(self, func, *args):
		object.__init__(self)
		self.callback = MakeCallback(func)
		self.args = args
	
	def __call__(self, *args):
		if args:
			args = self.args + args
			return self.callback(*args)
		else:
			return self.callback(*self.args)
	
	def __bool__(self):
		return bool(self.callback)

def MakeEvent(event):
	if not event:
		return None

	if isinstance(event, Event):
		return event
	else:
		return MakeCallback(event)


def NOOP(*args, **kwargs):
	"""No-operation function."""
	pass
