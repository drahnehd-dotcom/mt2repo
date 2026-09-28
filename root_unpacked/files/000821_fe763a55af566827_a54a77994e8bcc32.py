# -*- coding: iso-8859-1 -*-
import app
import ui
import grp
import net
import guild
import messenger
import localeInfo
import uiToolTip
import uiGameOption
import uiCommon
from _weakref import proxy

GROUP_FRIEND = 0
GROUP_GUILD = 1
if app.TEAM_MEMBER_STATUS:
    GROUP_BOARD = 2

START_POSITION = 40
MIN_WINDOW_HEIGHT = 200
MIN_WINDOW_WIDTH = 280
DEFAULT_WINDOW_WIDTH = 320
DEFAULT_WINDOW_HEIGHT = 400
ITEM_HEIGHT = 20
ITEM_SPACING = 20
FLAG_WIDTH = 16

STATE_OFFLINE = 0
STATE_ONLINE = 1

IMAGE_PATHS = {
    "ONLINE": "d:/ymir work/ui/game/windows/messenger_list_online.sub",
    "OFFLINE": "d:/ymir work/ui/game/windows/messenger_list_offline.sub",
    "OPEN": "d:/ymir work/ui/game/windows/messenger_list_open.sub",
    "CLOSE": "d:/ymir work/ui/game/windows/messenger_list_close.sub",
}

FLAG_FORMULA = "_language/flagi_male/{}.jpg"

SELECTION_COLOR = grp.GenerateColor(0.0, 0.0, 0.7, 0.7)


class MessengerItemBase(ui.Window):
    """Base class for all messenger items."""

    def __init__(self, parent_getter):
        super(MessengerItemBase, self).__init__()
        
        self._parent_getter = parent_getter
        self._name = ""
        self._is_selected = False
        self._love_point = -1
        self._love_point_tooltip = None
        
        self._setup_ui()
        self._setup_events()

    def _setup_ui(self):
        """Setup basic UI components."""
        self.SetParent(self._parent_getter())
        self.AddFlag("float")

        self._image = ui.ImageBox()
        self._image.AddFlag("not_pick")
        self._image.SetParent(self)
        self._image.Show()

        self._text = ui.TextLine()
        self._text.SetParent(self)
        self._text.SetPosition(20, 2)
        self._text.Show()

    def _setup_events(self):
        """Setup event handlers."""
        # Events will be overridden in derived classes
        pass

    def SetName(self, name):
        """Set the display name."""
        self._name = name
        if name:
            self._text.SetText(name)
            self.SetSize(20 + 6 * len(name) + 4, 16)

    def SetLovePoint(self, love_point):
        """Set love point for family members."""
        self._love_point = love_point

    def GetName(self):
        """Get the display name."""
        return self._name

    def Select(self):
        """Select this item."""
        self._is_selected = True

    def UnSelect(self):
        """Unselect this item."""
        self._is_selected = False

    def GetStepWidth(self):
        """Get indentation width."""
        return 0

    # Interface methods to be implemented by derived classes
    def CanWhisper(self):
        """Check if whisper is available."""
        return False

    def IsOnline(self):
        """Check if member is online."""
        return False

    def IsMobile(self):
        """Check if member has mobile access."""
        return False

    def OnWhisper(self):
        """Handle whisper action."""
        pass

    def OnMobileMessage(self):
        """Handle mobile message action."""
        pass

    def CanRemove(self):
        """Check if item can be removed."""
        return False

    def OnRemove(self):
        """Handle remove action."""
        return False

    def CanWarp(self):
        """Check if warp is available."""
        return False

    def OnWarp(self):
        """Handle warp action."""
        pass

    def OnMouseOverIn(self):
        """Handle mouse over event."""
        if self._love_point != -1:
            self._show_love_point_tooltip()

    def OnMouseOverOut(self):
        """Handle mouse out event."""
        if self._love_point_tooltip:
            self._love_point_tooltip.HideToolTip()

    def _show_love_point_tooltip(self):
        """Show love point tooltip."""
        if not self._love_point_tooltip:
            self._love_point_tooltip = uiToolTip.ToolTip(100)
            self._love_point_tooltip.SetTitle(self._name)
            self._love_point_tooltip.AppendTextLine(
                localeInfo.AFF_LOVE_POINT % self._love_point
            )
            self._love_point_tooltip.ResizeToolTip()
        self._love_point_tooltip.ShowToolTip()

    def OnMouseLeftButtonDown(self):
        """Handle left mouse button down."""
        self._parent_getter().OnSelectItem(self)

    def OnMouseLeftButtonDoubleClick(self):
        """Handle double click."""
        self._parent_getter().OnDoubleClickItem(self)

    def OnRender(self):
        """Render selection highlight."""
        if self._is_selected:
            x, y = self.GetGlobalPosition()
            grp.SetColor(SELECTION_COLOR)
            grp.RenderBar(x + 16, y, self.GetWidth() - 16, self.GetHeight())


class MessengerMemberItem(MessengerItemBase):
    """Base class for member items (friends, guild members, etc.)."""

    def __init__(self, parent_getter):
        super(MessengerMemberItem, self).__init__(parent_getter)
        
        self._key = None
        self._state = STATE_OFFLINE
        
        self._set_offline_state()

    def GetStepWidth(self):
        """Get indentation for member items."""
        return 15

    def SetKey(self, key):
        """Set unique identifier key."""
        self._key = key

    def IsSameKey(self, key):
        """Check if key matches."""
        return self._key == key

    def IsOnline(self):
        """Check if member is online."""
        return self._state == STATE_ONLINE

    def SetOnline(self):
        """Set member as online."""
        self._image.LoadImage(IMAGE_PATHS["ONLINE"])
        self._state = STATE_ONLINE

    def SetOffline(self):
        """Set member as offline."""
        self._image.LoadImage(IMAGE_PATHS["OFFLINE"])
        self._state = STATE_OFFLINE

    def _set_offline_state(self):
        """Initialize with offline state."""
        self.SetOffline()

    def CanWhisper(self):
        """Check if whisper is available."""
        return self.IsOnline()

    def OnWhisper(self):
        """Handle whisper action."""
        if self.IsOnline():
            self._parent_getter().whisperButtonEvent(self.GetName())


class MessengerGroupItem(MessengerItemBase):
    """Base class for group items that can contain members."""

    def __init__(self, parent_getter):
        super(MessengerGroupItem, self).__init__(parent_getter)
        
        self._is_open = False
        self._member_list = []
        
        self._set_closed_state()

    def _set_closed_state(self):
        """Initialize with closed state."""
        self.Close()

    def AppendMember(self, member, key, name):
        """Add a member to this group."""
        member.SetKey(key)
        member.SetName(name)
        self._member_list.append(member)
        return member

    def RemoveMember(self, item):
        """Remove a member from this group."""
        try:
            self._member_list.remove(item)
        except ValueError:
            pass

    def ClearMember(self):
        """Clear all members."""
        self._member_list = []

    def FindMember(self, key):
        """Find member by key."""
        for member in self._member_list:
            if member.IsSameKey(key):
                return member
        return None

    def GetLoginMemberList(self):
        """Get list of online members."""
        return [member for member in self._member_list if member.IsOnline()]

    def GetLogoutMemberList(self):
        """Get list of offline members."""
        return [member for member in self._member_list if not member.IsOnline()]

    def IsOpen(self):
        """Check if group is expanded."""
        return self._is_open

    def Open(self):
        """Expand the group."""
        self._image.LoadImage(IMAGE_PATHS["OPEN"])
        self._is_open = True

    def Close(self):
        """Collapse the group."""
        self._image.LoadImage(IMAGE_PATHS["CLOSE"])
        self._is_open = False
        
        # Hide all members
        for member in self._member_list:
            member.Hide()

    def Select(self):
        """Toggle group open/closed state."""
        if self.IsOpen():
            self.Close()
        else:
            self.Open()
        
        super(MessengerGroupItem, self).Select()
        self._parent_getter().OnRefreshList()


class MessengerFriendItem(MessengerMemberItem):
    """Friend list item."""

    def __init__(self, parent_getter):
        super(MessengerFriendItem, self).__init__(parent_getter)

    def CanRemove(self):
        """Friends can be removed."""
        return True

    def OnRemove(self):
        """Remove friend."""
        messenger.RemoveFriend(self._key)
        net.SendMessengerRemovePacket(self._key, self._name)
        return True


class MessengerGuildItem(MessengerMemberItem):
    """Guild member item."""

    def __init__(self, parent_getter):
        super(MessengerGuildItem, self).__init__(parent_getter)

    def CanWarp(self):
        """Check if warp to guild member is available."""
        return self.IsOnline()

    def OnWarp(self):
        """Warp to guild member."""
        net.SendGuildUseSkillPacket(155, self._key)

    def CanRemove(self):
        """Check if guild member can be removed."""
        # Cannot remove during guild wars
        for i in range(guild.ENEMY_GUILD_SLOT_MAX_COUNT):
            if guild.GetEnemyGuildName(i) != "":
                return False

        # Check authority and membership
        if guild.MainPlayerHasAuthority(guild.AUTH_REMOVE_MEMBER):
            if guild.IsMemberByName(self._name):
                return True

        return False

    def OnRemove(self):
        """Remove guild member."""
        net.SendGuildRemoveMemberPacket(self._key)
        return True


if app.ENABLE_MESSENGER_TEAM:
    class MessengerTeamItem(MessengerMemberItem):
        """Team member item."""

        def __init__(self, parent_getter):
            super(MessengerTeamItem, self).__init__(parent_getter)

        def CanRemove(self):
            """Team members cannot be removed."""
            return False

        def OnRemove(self):
            """Team members cannot be removed."""
            return False


if app.TEAM_MEMBER_STATUS:
    class MessengerBoardItem(MessengerMemberItem):
        """Board member item with flag support."""

        def __init__(self, parent_getter):
            super(MessengerBoardItem, self).__init__(parent_getter)
            self._flags = []

        def CanRemove(self):
            """Board members cannot be removed."""
            return False

        def OnRemove(self):
            """Board members cannot be removed."""
            return False

        def GetName(self):
            """Use key as name for board items."""
            return self._key

        def AppendCharFlag(self, flags_string):
            """Add character flags."""
            self._text.SetPosition(0, 2)
            self._image.SetPosition(-14, 2)

            for flag in flags_string.split(","):
                flag_image = ui.ImageBox()
                flag_image.SetParent(self)

                text_size_x, text_size_y = self._text.GetTextSize()
                text_x, text_y = self._text.GetLocalPosition()
                x_pos = (text_size_x + text_x + 5) + len(self._flags) * FLAG_WIDTH
                flag_image.SetPosition(x_pos, 0)
                flag_image.SetWindowVerticalAlignCenter()
                
                try:
                    flag_image.LoadImage(FLAG_FORMULA.format(flag))
                    flag_image.Show()
                    self._flags.append(flag_image)
                except:
                    flag_image.Hide()
                    break

        def SetName(self, name):
            """Override to adjust position for flags."""
            super(MessengerBoardItem, self).SetName(name)
            self._text.SetPosition(0, 2)


class MessengerFriendGroup(MessengerGroupItem):
    """Friend group container."""

    def __init__(self, parent_getter):
        super(MessengerFriendGroup, self).__init__(parent_getter)
        self.SetName(localeInfo.MESSENGER_FRIEND)

    def AppendMember(self, key, name):
        """Add friend member."""
        item = MessengerFriendItem(self._parent_getter)
        return super(MessengerFriendGroup, self).AppendMember(item, key, name)


class MessengerGuildGroup(MessengerGroupItem):
    """Guild group container."""

    def __init__(self, parent_getter):
        super(MessengerGuildGroup, self).__init__(parent_getter)
        self.SetName(localeInfo.MESSENGER_GUILD)
        self.AddFlag("float")

    def AppendMember(self, key, name):
        """Add guild member."""
        item = MessengerGuildItem(self._parent_getter)
        return super(MessengerGuildGroup, self).AppendMember(item, key, name)


if app.ENABLE_MESSENGER_TEAM:
    class MessengerTeamGroup(MessengerGroupItem):
        """Team group container."""

        def __init__(self, parent_getter):
            super(MessengerTeamGroup, self).__init__(parent_getter)
            self.SetName(localeInfo.MESSENGER_TEAM)

        def AppendMember(self, key, name):
            """Add team member."""
            item = MessengerTeamItem(self._parent_getter)
            return super(MessengerTeamGroup, self).AppendMember(item, key, name)


if app.TEAM_MEMBER_STATUS:
    class MessengerBoardGroup(MessengerGroupItem):
        """Board group container."""

        def __init__(self, parent_getter):
            super(MessengerBoardGroup, self).__init__(parent_getter)
            self.SetName("TeamList")
            self.AddFlag("float")

        def AppendMember(self, key, name):
            """Add board member."""
            item = MessengerBoardItem(self._parent_getter)
            return super(MessengerBoardGroup, self).AppendMember(item, key, name)


class MessengerFamilyGroup(MessengerGroupItem):
    """Family group container."""

    def __init__(self, parent_getter):
        super(MessengerFamilyGroup, self).__init__(parent_getter)
        self.SetName(localeInfo.MESSENGER_FAMILY)
        self.AddFlag("float")
        self._lover = None

    def AppendMember(self, key, name):
        """Add family member (lover)."""
        item = MessengerGuildItem(self._parent_getter)
        self._lover = item
        return super(MessengerFamilyGroup, self).AppendMember(item, key, name)

    def GetLover(self):
        """Get lover reference."""
        return self._lover


class ResizeButton(ui.DragButton):
    """Custom resize button for messenger window with enhanced resize functionality."""

    def __init__(self):
        super(ResizeButton, self).__init__()
        self._is_resizing = False

    def OnMouseOverIn(self):
        """Show resize cursor."""
        app.SetCursor(app.VSIZE)

    def OnMouseOverOut(self):
        """Restore normal cursor."""
        app.SetCursor(app.NORMAL)

    def OnMouseLeftButtonDown(self):
        """Handle resize start."""
        self._is_resizing = True
        super(ResizeButton, self).OnMouseLeftButtonDown()

    def OnMouseLeftButtonUp(self):
        """Handle resize end."""
        self._is_resizing = False
        super(ResizeButton, self).OnMouseLeftButtonUp()

    def IsResizing(self):
        """Check if currently resizing."""
        return self._is_resizing


class MessengerWindow(ui.ScriptWindow):
    """Main messenger window with friends, guild, and family management."""

    def __init__(self):
        super(MessengerWindow, self).__init__()
        
        # Set messenger handler
        messenger.SetMessengerHandler(self)
        
        # Initialize state
        self._is_loaded = False
        self._showing_page_size = 0
        self._start_line = 0
        
        # Initialize collections
        self._group_list = []
        self._showing_item_list = []
        self._selected_item = None
        self._family_group = None
        
        # Initialize UI components
        self._ui_components = {}
        self._dialogs = {}
        
        # Initialize callbacks
        self.whisperButtonEvent = lambda *args: None
        self.guildButtonEvent = None
        
        # Setup groups and refresh
        self._setup_groups()
        messenger.RefreshGuildMember()

    def __del__(self):
        messenger.SetMessengerHandler(None)
        super(MessengerWindow, self).__del__()

    def Show(self):
        """Show messenger window and load if needed."""
        if not self._is_loaded:
            self._is_loaded = True
            self._load_window()
            self._set_default_size()
            self.OnRefreshList()
            self.OnResizeDialog()
        
        super(MessengerWindow, self).Show()

    def _load_window(self):
        """Load UI script and setup components."""
        try:
            py_scr_loader = ui.PythonScriptLoader()
            py_scr_loader.LoadScriptFile(self, "UIScript/MessengerWindow.py")
            
            self._bind_ui_components()
            self._setup_events()
            self._setup_resize_button()
            self._setup_ui_layout()
            
        except Exception as e:
            import exception
            exception.Abort("MessengerWindow._load_window")

    def _bind_ui_components(self):
        """Bind UI components from script."""
        component_names = [
            "board", "ScrollBar", "WhisperButton",
            "RemoveButton", "AddFriendButton", "GuildButton"
        ]
        
        for name in component_names:
            try:
                key = name.lower().replace("button", "_button").replace("bar", "_bar")
                self._ui_components[key] = self.GetChild(name)
            except KeyError:
                import exception
                exception.Abort("MessengerWindow._bind_ui_components: " + name)

    def _setup_events(self):
        """Setup event handlers for UI components."""
        # Window events
        self._ui_components['board'].SetCloseEvent(ui.__mem_func__(self.Close))
        self._ui_components['scroll_bar'].SetScrollEvent(ui.__mem_func__(self.OnScroll))
        
        # Button events
        button_events = {
            'whisper_button': self.OnPressWhisperButton,
            'remove_button': self.OnPressRemoveButton,
            'addfriend_button': self.OnPressAddFriendButton,
            'guild_button': self.OnPressGuildButton,
        }
        
        for button_key, event_handler in button_events.items():
            if button_key in self._ui_components:
                self._ui_components[button_key].SetEvent(ui.__mem_func__(event_handler))

        # Disable buttons initially
        self._ui_components['whisper_button'].Disable()
        self._ui_components['remove_button'].Disable()

    def _setup_resize_button(self):
        """Setup window resize functionality with larger default size."""
        resize_button = ResizeButton()
        resize_button.AddFlag("restrict_x")
        resize_button.SetParent(self)
        resize_button.SetSize(self.GetWidth(), 10)
        resize_button.SetWindowVerticalAlignBottom()
        resize_button.SetPosition(0, DEFAULT_WINDOW_HEIGHT - 100)
        resize_button.SetMoveEvent(ui.__mem_func__(self.OnResizeDialog))
        resize_button.Show()
        
        self._ui_components['resize_button'] = resize_button

    def _set_default_size(self):
        """Set larger default window size."""
        # Set initial window size to be larger
        self.SetSize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        
        # Update board size to match
        if self._ui_components.get('board'):
            self._ui_components['board'].SetSize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        
        # Position resize button for the larger window
        if self._ui_components.get('resize_button'):
            self._ui_components['resize_button'].SetPosition(0, DEFAULT_WINDOW_HEIGHT - 100)

    def _setup_ui_layout(self):
        """Setup UI layout with better positioning for larger window."""
        button_positions = [
            ('addfriend_button', -60, 35),
            ('whisper_button', -20, 35),
            ('remove_button', 20, 35),
            ('guild_button', 60, 35),
        ]
        
        for button_key, x, y in button_positions:
            if button_key in self._ui_components:
                self._ui_components[button_key].SetPosition(x, y)

        for group in self._group_list:
            group.SetTop()
        self.SetTop()

    def _setup_groups(self):
        """Initialize messenger groups."""
        # Friend group
        friend_group = MessengerFriendGroup(ui.__mem_func__(self.GetSelf))
        friend_group.Open()
        friend_group.Show()
        self._group_list.append(friend_group)

        # Guild group
        guild_group = MessengerGuildGroup(ui.__mem_func__(self.GetSelf))
        guild_group.Open()
        guild_group.Show()
        self._group_list.append(guild_group)

        # Team board group (if enabled)
        if app.TEAM_MEMBER_STATUS:
            board_group = MessengerBoardGroup(ui.__mem_func__(self.GetSelf))
            board_group.Open()
            board_group.Show()
            self._group_list.append(board_group)

        # Team group (if enabled)
        if app.ENABLE_MESSENGER_TEAM:
            team_group = MessengerTeamGroup(ui.__mem_func__(self.GetSelf))
            team_group.Open()
            team_group.Show()
            self._group_list.append(team_group)

    def _add_family_group(self):
        """Add family group when needed."""
        family_group = MessengerFamilyGroup(ui.__mem_func__(self.GetSelf))
        family_group.Open()
        family_group.Show()
        self._family_group = family_group

    def SetSize(self, width, height):
        """Override size setting to update board with minimum size constraints."""
        # Enforce minimum size constraints
        width = max(width, MIN_WINDOW_WIDTH)
        height = max(height, MIN_WINDOW_HEIGHT)
        
        super(MessengerWindow, self).SetSize(width, height)
        if self._ui_components.get('board'):
            self._ui_components['board'].SetSize(width, height)

    def OnResizeDialog(self):
        """Handle window resize with improved size constraints."""
        if 'resize_button' not in self._ui_components:
            return
            
        x, y = self._ui_components['resize_button'].GetLocalPosition()
        
        if y < MIN_WINDOW_HEIGHT:
            self._ui_components['resize_button'].SetPosition(x, MIN_WINDOW_HEIGHT)
            return
        
        new_height = y + self._ui_components['resize_button'].GetHeight()
        
        self.SetSize(self.GetWidth(), new_height)
        
        self._showing_page_size = y - (START_POSITION + 26)
        
        self._showing_page_size = max(self._showing_page_size, ITEM_HEIGHT * 3)
        
        self._ui_components['scroll_bar'].SetScrollBarSize(self._showing_page_size)
        
        self._locate_members()
        
        self._ui_components['resize_button'].TurnOffCallBack()
        self.UpdateRect()
        self._ui_components['resize_button'].TurnOnCallBack()

    def _locate_members(self):
        """Position member items in the window with improved spacing for larger window."""
        if not self._is_loaded:
            return

        # Handle scrollbar visibility
        visible_items = self._showing_page_size // ITEM_HEIGHT
        if visible_items >= len(self._showing_item_list):
            self._ui_components['scroll_bar'].Hide()
            self._start_line = 0
        else:
            if self._showing_item_list:
                ratio = float(visible_items) / float(len(self._showing_item_list))
                self._ui_components['scroll_bar'].SetMiddleBarSize(ratio)
            self._ui_components['scroll_bar'].Show()

        # Position items with better spacing for larger window
        y_pos = START_POSITION
        height_limit = self.GetHeight() - (START_POSITION + 20)  # More bottom margin

        # Hide all items first
        for item in self._showing_item_list:
            item.Hide()

        # Show visible items with improved positioning
        items_shown = 0
        for item in self._showing_item_list[self._start_line:]:
            # Better horizontal positioning for larger window
            x_pos = 25 + item.GetStepWidth()  # Slightly more left margin
            item.SetPosition(x_pos, y_pos)
            item.SetTop()
            item.Show()
            
            items_shown += 1
            y_pos += ITEM_HEIGHT
            
            # Add extra spacing every 5 items for better visual grouping
            if items_shown % 5 == 0:
                y_pos += 2
            
            if y_pos > height_limit:
                break

    def OnRefreshList(self):
        """Refresh the display list."""
        self._showing_item_list = []

        if self._family_group:
            self._showing_item_list.append(self._family_group)
            if self._family_group.GetLover():
                self._showing_item_list.append(self._family_group.GetLover())

        for group in self._group_list:
            self._showing_item_list.append(group)

            if group.IsOpen():
                login_members = group.GetLoginMemberList()
                logout_members = group.GetLogoutMemberList()

                if login_members or logout_members:
                    self._showing_item_list.extend(login_members)
                    self._showing_item_list.extend(logout_members)
                else:
                    empty_item = MessengerItemBase(ui.__mem_func__(self.GetSelf))
                    empty_item.SetName(localeInfo.MESSENGER_EMPTY_LIST)
                    self._showing_item_list.append(empty_item)

        self._locate_members()

    def OnSelectItem(self, item):
        """Handle item selection."""
        if self._selected_item and item != self._selected_item:
            self._selected_item.UnSelect()

        self._selected_item = item

        if self._selected_item:
            self._selected_item.Select()
            self._update_button_states()

    def _update_button_states(self):
        """Update button enabled/disabled states based on selection."""
        if not self._selected_item:
            return

        if self._selected_item.CanWhisper():
            self._ui_components['whisper_button'].Enable()
        else:
            self._ui_components['whisper_button'].Disable()

        if self._selected_item.CanRemove():
            self._ui_components['remove_button'].Enable()
        else:
            self._ui_components['remove_button'].Disable()

    def OnDoubleClickItem(self, item):
        """Handle double click on item."""
        if not self._selected_item:
            return

        if self._selected_item.IsOnline():
            self.OnPressWhisperButton()

    # Button event handlers
    def OnPressWhisperButton(self):
        """Handle whisper button press."""
        if self._selected_item:
            self._selected_item.OnWhisper()

    def OnPressRemoveButton(self):
        """Handle remove button press."""
        if self._selected_item and self._selected_item.CanRemove():
            question_dialog = uiCommon.QuestionDialog()
            question_dialog.SetText(localeInfo.MESSENGER_DO_YOU_DELETE)
            question_dialog.SetAcceptEvent(ui.__mem_func__(self.OnRemove))
            question_dialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
            question_dialog.Open()
            self._dialogs['question'] = question_dialog

    def OnPressAddFriendButton(self):
        """Handle add friend button press."""
        input_dialog = uiCommon.InputDialog()
        input_dialog.SetTitle(localeInfo.MESSENGER_ADD_FRIEND)
        input_dialog.SetAcceptEvent(ui.__mem_func__(self.OnAddFriend))
        input_dialog.SetCancelEvent(ui.__mem_func__(self.OnCancelAddFriend))
        input_dialog.Open()
        self._dialogs['friend_input'] = input_dialog

    def OnPressGuildButton(self):
        """Handle guild button press."""
        if self.guildButtonEvent:
            self.guildButtonEvent()

    # Dialog event handlers
    def OnRemove(self):
        """Handle remove confirmation."""
        if self._selected_item and self._selected_item.CanRemove():
            for group in self._group_list:
                group.RemoveMember(self._selected_item)
            
            self._selected_item.OnRemove()
            self._selected_item.UnSelect()
            self._selected_item = None
            self.OnRefreshList()

        self.OnCloseQuestionDialog()

    def OnAddFriend(self):
        """Handle add friend confirmation."""
        if 'friend_input' in self._dialogs:
            text = self._dialogs['friend_input'].GetText()
            if text:
                net.SendMessengerAddByNamePacket(text)
        self.OnCancelAddFriend()
        return True

    def OnCancelAddFriend(self):
        """Handle add friend cancellation."""
        if 'friend_input' in self._dialogs:
            self._dialogs['friend_input'].Close()
            del self._dialogs['friend_input']
        return True

    def OnCloseQuestionDialog(self):
        """Handle question dialog close."""
        if 'question' in self._dialogs:
            self._dialogs['question'].Close()
            del self._dialogs['question']
        return True

    def OnScroll(self):
        """Handle scroll bar movement."""
        scroll_line_count = len(self._showing_item_list) - (self._showing_page_size // ITEM_HEIGHT)
        start_line = int(scroll_line_count * self._ui_components['scroll_bar'].GetPos())

        if start_line != self._start_line:
            self._start_line = start_line
            self._locate_members()

    def Close(self):
        """Close messenger window."""
        for dialog in self._dialogs.values():
            if dialog:
                dialog.Close()
        self._dialogs.clear()
        self.Hide()

    def OnPressEscapeKey(self):
        """Handle escape key press."""
        self.Close()
        return True

    def GetSelf(self):
        """Get self reference for callbacks."""
        return self

    # Messenger interface methods
    def ClearGuildMember(self):
        """Clear guild member list."""
        self._group_list[GROUP_GUILD].ClearMember()

    def SetWhisperButtonEvent(self, event):
        """Set whisper button event handler."""
        self.whisperButtonEvent = event

    def SetGuildButtonEvent(self, event):
        """Set guild button event handler."""
        self.guildButtonEvent = event

    def RefreshMessenger(self):
        """Refresh messenger display."""
        self.OnRefreshList()

    # Member management methods
    def _add_to_group(self, group_index, key, name):
        """Add member to specified group."""
        group = self._group_list[group_index]
        member = group.FindMember(key)
        if not member:
            member = group.AppendMember(key, name)
            self.OnSelectItem(None)
        return member

    def OnLogin(self, group_index, key, name=None):
        """Handle member login."""
        if not name:
            name = key
        member = self._add_to_group(group_index, key, name)
        member.SetName(name)
        member.SetOnline()
        self.OnRefreshList()

    def OnLogout(self, group_index, key, name=None):
        """Handle member logout."""
        if not name:
            name = key
        member = self._add_to_group(group_index, key, name)
        member.SetName(name)
        member.SetOffline()
        self.OnRefreshList()

    def OnAddLover(self, name, love_point):
        """Add lover to family group."""
        if not self._family_group:
            self._add_family_group()

        member = self._family_group.AppendMember(0, name)
        member.SetName(name)
        member.SetLovePoint(love_point)
        member.SetOffline()
        self.OnRefreshList()

    def OnUpdateLovePoint(self, love_point):
        """Update love point value."""
        if self._family_group:
            lover = self._family_group.GetLover()
            if lover:
                lover.SetLovePoint(love_point)

    def OnLoginLover(self):
        """Handle lover login."""
        if self._family_group:
            lover = self._family_group.GetLover()
            if lover:
                lover.SetOnline()

    def OnLogoutLover(self):
        """Handle lover logout."""
        if self._family_group:
            lover = self._family_group.GetLover()
            if lover:
                lover.SetOffline()

    def ClearLoverInfo(self):
        """Clear lover information."""
        if self._family_group:
            self._family_group.ClearMember()
            self._family_group = None
            self.OnRefreshList()

    # Team member status (if enabled)
    if app.TEAM_MEMBER_STATUS:
        def CheckoutTeamMemberStatus(self, name, lang, status):
            """Handle team member status update."""
            group = self._group_list[GROUP_BOARD]
            member = group.FindMember(name)

            if not member:
                member = group.AppendMember(name, name)
                member.AppendCharFlag(lang)
                self.OnSelectItem(None)

            if status:
                member.SetOnline()
            else:
                member.SetOffline()

            self.OnRefreshList()

        def ClearTeamMemberList(self):
            """Clear team member list."""
            group = self._group_list[GROUP_BOARD]
            group.ClearMember()
            self.OnRefreshList()

    def Destroy(self):
        """Clean up resources."""
        self._ui_components.clear()
        self._dialogs.clear()
        self._group_list = []
        self._showing_item_list = []
        self._selected_item = None
        self._family_group = None