import ui, app, net, constInfo, player
import datetime
import chat
import dbg
import wndMgr
import localeInfo
import exception
import emoji
from uiToolTip import ItemToolTip

IMG_DIR = "d:/ymir work/ui/game/event_calendar/"
IMG_ICON_DIR = "d:/ymir work/ui/game/event_calendar/icons/"
MINI_IMG_ICON_DIR = "d:/ymir work/ui/game/event_calendar/icons/mini_gui/"

EVENT_DAY_INDEX = 0
EVENT_ID = 1
EVENT_INDEX = 2
EVENT_START_TEXT = 3
EVENT_END_TEXT = 4
EVENT_EMPIRE_FLAG = 5
EVENT_CHANNEL_FLAG = 6
EVENT_VALUE0 = 7
EVENT_VALUE1 = 8
EVENT_VALUE2 = 9
EVENT_VALUE3 = 10
EVENT_START_TIME = 11
EVENT_END_TIME = 12
EVENT_IS_ACTIVE = 13

events_default_data = {
    player.BONUS_EVENT: ["bonus_event", localeInfo.BONUS_EVENT],
    player.DOUBLE_BOSS_LOOT_EVENT: ["double_boss_loot_event", localeInfo.DOUBLE_BOSS_LOOT_EVENT],
    player.DOUBLE_METIN_LOOT_EVENT: ["double_metin_loot_event", localeInfo.DOUBLE_METIN_LOOT_EVENT],
    player.DOUBLE_MISSION_BOOK_EVENT: ["double_mission_book_event", localeInfo.DOUBLE_MISSION_BOOK_EVENT],
    player.DUNGEON_COOLDOWN_EVENT: ["dungeon_cooldown_event", localeInfo.DUNGEON_COOLDOWN_EVENT],
    player.DUNGEON_CHEST_LOOT_EVENT: ["dungeon_ticket_loot_event", localeInfo.DUNGEON_CHEST_LOOT_EVENT],
    player.EMPIRE_WAR_EVENT: ["empire_war_event", ""],
    player.MOONLIGHT_EVENT: ["moonlight_event", localeInfo.MOONLIGHT_EVENT],
    player.VALENTINE_EVENT: ["valentine_event", localeInfo.VALENTINE_EVENT],
    player.TOURNAMENT_EVENT: ["tournament_event", ""],
    player.WHELL_OF_FORTUNE_EVENT: ["whell_of_fortune_event", localeInfo.WHELL_OF_FORTUNE_EVENT],
    player.HALLOWEEN_EVENT: ["halloween_event", localeInfo.HALLOWEEN_EVENT],
    player.NPC_SEARCH_EVENT: ["npc_search", ""],
    player.ITEM_DROP_EVENT: ["item_drop_event", localeInfo.ITEM_DROP_EVENT],
    player.YANG_DROP_EVENT: ["money_drop_event", localeInfo.YANG_DROP_EVENT],
    player.EXP_EVENT: ["exp_event", localeInfo.EXP_EVENT],
    player.SWITCH_RARE_EVENT: ["switch_rare_event", localeInfo.SWITCH_RARE_EVENT],
    player.SWITCH_AVERAGE_EVENT: ["switch_average_event", localeInfo.SWITCH_AVERAGE_EVENT],
    player.SWITCH_RUNE_EVENT: ["switch_rune_event", localeInfo.SWITCH_RUNE_EVENT],
    player.DOUBLE_ACHIEVEMENT_POINTS: ["double_achievement_points", localeInfo.DOUBLE_ACHIEVEMENT_POINTS],
    player.MINING_CHEST_EVENT: ["mining_chest_event", localeInfo.MINING_CHEST_EVENT],
    player.DOUBLE_ORE_EVENT: ["double_ore_event", localeInfo.DOUBLE_ORE_EVENT],
    player.BIGGER_STAR_CHANCE: ["bigger_star_chance", localeInfo.BIGGER_STAR_CHANCE],
}

server_event_data = {}


class EventDataManager(object):
    """Manages server event data with a clean API"""
    
    @staticmethod
    def calculate_day_count(month, year):
        """Calculate the number of days in a given month and year"""
        if month == 2:
            if ((year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)):
                return 29
            else:
                return 28
        elif month in (1, 3, 5, 7, 8, 10, 12):
            return 31
        else:
            return 30
    
    @staticmethod
    def set_event_status(event_id, event_status, end_time, end_time_text):
        """Update the status of an event"""
        for day_index, event_list in server_event_data.items():
            if event_id in event_list:
                event_list[event_id][EVENT_IS_ACTIVE] = event_status
                event_list[event_id][EVENT_END_TIME] = end_time
                event_list[event_id][EVENT_END_TEXT] = end_time_text
    
    @staticmethod
    def set_server_data(day_index, event_id, event_index, start_time, end_time, 
                       empire_flag, channel_flag, value0, value1, value2, value3, 
                       start_real_time, end_real_time, is_already_start):
        """Set server event data for a specific day"""
        event_data = [
            day_index, event_id, event_index, start_time, end_time, empire_flag,
            channel_flag, value0, value1, value2, value3, start_real_time,
            end_real_time, is_already_start
        ]
        
        if day_index in server_event_data:
            server_event_data[day_index][event_id] = event_data
        else:
            server_event_data[day_index] = {event_id: event_data}
    
    @staticmethod
    def is_event_id_active(event_id):
        """Check if an event ID is currently active"""
        for day_index, event_list in server_event_data.items():
            if event_id in event_list:
                return event_list[event_id][EVENT_IS_ACTIVE]
        return False
    
    @staticmethod
    def is_event_index_active(event_index):
        """Check if an event index is currently active"""
        for day_index, event_list in server_event_data.items():
            for event_id, event_data in event_list.items():
                if event_data[EVENT_IS_ACTIVE] and event_data[EVENT_INDEX] == event_index:
                    return True
        return False
    
    @staticmethod
    def get_event_index_data(event_index):
        """Get event data by event index"""
        for day_index, event_list in server_event_data.items():
            for event_id, event_data in event_list.items():
                if event_data[EVENT_INDEX] == event_index:
                    return event_data
        return None
    
    @staticmethod
    def get_event_id_data(event_id):
        """Get event data by event ID"""
        for day_index, event_list in server_event_data.items():
            if event_id in event_list:
                return event_list[event_id]
        return None


class ImageBoxSpecial(ui.ImageBox):
    """Enhanced ImageBox with event handling and animation capabilities"""
    
    def __init__(self, is_mini_icon=False):
        super(ImageBoxSpecial, self).__init__()
        self._initialize_attributes(is_mini_icon)
        self._setup_mini_icon_behavior()
    
    def __del__(self):
        super(ImageBoxSpecial, self).__del__()
    
    def _initialize_attributes(self, is_mini_icon):
        """Initialize all instance attributes"""
        self.mini_icon = None
        self.event_list = []
        self.image_index = 0
        self.is_mini_icon = is_mini_icon
        self.day_index = 0
        
        self.waiting_time = 2.0
        self.sleep_time = 0.0
        self.alpha_value = 0.3
        self.increase_value = 0.05
        self.min_alpha = 0.3
        self.max_alpha = 1.0
        self.alpha_status = False
    
    def _setup_mini_icon_behavior(self):
        """Setup behavior specific to mini icons"""
        if self.is_mini_icon:
            self.AddFlag("attach")
            self.AddFlag("movable")
            x, y = wndMgr.GetScreenWidth() - 90, 200
            self.SetPosition(x, y)
            self.SetEvent(ui.__mem_func__(self._on_click_event_icon), "mouse_click")
            self.SetMouseLeftButtonDoubleClickEvent(ui.__mem_func__(self._on_click_double))
            self.SetMouseRightButtonDownEvent(ui.__mem_func__(self._next_event_with_key))
    
    def Destroy(self):
        """Clean up resources"""
        self.mini_icon = None
        self.event_list = []
        self.image_index = 0
        self.is_mini_icon = False
        self.waiting_time = 0.0
        self.sleep_time = 0.0
        self.alpha_value = 0.0
        self.increase_value = 0.0
        self.min_alpha = 0.0
        self.max_alpha = 0.0
        self.alpha_status = False
    
    def OnMoveWindow(self, x, y):
        """Handle window movement with boundary constraints"""
        screen_width, screen_height = wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight()
        
        # Constrain x position
        if x < 0:
            x = 0
        elif x + self.GetWidth() >= screen_width - 70:
            x = screen_width - 80 - self.GetWidth()
        
        # Constrain y position
        if y < 0:
            y = 0
        elif y + self.GetHeight() >= screen_height - 100:
            y = screen_height - 100 - self.GetHeight()
        
        self.SetPosition(x, y)
    
    def _next_event_with_key(self):
        """Trigger next event animation on key press"""
        if len(self.event_list) > 1:
            self.sleep_time = 0
            self.alpha_value = self.max_alpha
            self.alpha_status = True
    
    def SetBackgroundImage(self, image):
        """Set background image and setup mouse events"""
        self.LoadImage(image)
        self.SAFE_SetStringEvent("MOUSE_OVER_IN", self.OverInItem)
        self.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.OverOutItem)
        self.SetEvent(ui.__mem_func__(self._on_click_event_icon), "mouse_click")
    
    def _on_click_event_icon(self):
        """Handle click on event icon"""
        index, event_id = self._get_next_image(self.image_index)
        event_data = EventDataManager.get_event_id_data(event_id)
        
        if event_data and event_data[EVENT_IS_ACTIVE]:
            interface = constInfo.GetInterfaceInstance()
            if interface and interface.wndEventManager:
                interface.wndEventManager.OnClick(event_data[EVENT_INDEX])
    
    def _on_click_double(self):
        """Handle double click to open event calendar"""
        interface = constInfo.GetInterfaceInstance()
        if interface:
            interface.OpenEventCalendar()
    
    def SetImage(self, folder):
        """Set the event icon image"""
        if self.mini_icon is None:
            self.mini_icon = ui.ImageBox()
            self.mini_icon.SetParent(self)
            self.mini_icon.AddFlag("not_pick")
        
        image_path = (MINI_IMG_ICON_DIR if self.is_mini_icon else IMG_ICON_DIR) + folder + ".tga"
        self.mini_icon.LoadImage(image_path)
        self.mini_icon.SetPosition(6, 6)
        self.mini_icon.Show()
        
        if self.is_mini_icon:
            self.SetSize(57, 57)
        
        self.alpha_value = self.min_alpha
        self.alpha_status = False
    
    def OverOutItem(self):
        """Handle mouse out event"""
        interface = constInfo.GetInterfaceInstance()
        if interface and interface.tooltipItem:
            interface.tooltipItem.HideToolTip()
    
    def OverInItem(self):
        """Handle mouse over event"""
        interface = constInfo.GetInterfaceInstance()
        if interface and interface.wndEventManager:
            interface.wndEventManager.OverInItem(self.day_index)
    
    def Clear(self):
        """Clear all event data and reset size"""
        self.mini_icon = None
        self.event_list = []
        if self.is_mini_icon:
            self.SetSize(0, 0)
    
    def DeleteImage(self, event_index):
        """Remove an event from the list"""
        if 0 <= event_index < len(self.event_list):
            del self.event_list[event_index]
            if self.is_mini_icon and len(self.event_list) == 0:
                self.SetSize(0, 0)
    
    def AppendImage(self, event_id):
        """Add an event to the list"""
        if event_id in self.event_list:
            return
        
        self.event_list.append(event_id)
        
        if len(self.event_list) == 1:
            self.image_index = 0
            event_data = EventDataManager.get_event_id_data(event_id)
            if event_data:
                event_index = event_data[EVENT_INDEX]
                if event_index in events_default_data:
                    self.SetImage(events_default_data[event_index][0])
        
        if self.is_mini_icon:
            self.SetSize(57, 57)
    
    def _get_next_image(self, list_index):
        """Get the next image in the rotation"""
        if list_index >= len(self.event_list):
            if len(self.event_list) > 0:
                return 0, self.event_list[0]
            return 0, 0
        return list_index, self.event_list[list_index]
    
    def OnUpdate(self):
        """Update animation state"""
        if len(self.event_list) <= 1:
            self.image_index = 0
            return
        
        if self.sleep_time > app.GetTime():
            return
        
        if self.alpha_status:
            self.alpha_value -= self.increase_value
            if self.alpha_value < self.min_alpha:
                self.alpha_value = self.min_alpha
                self.alpha_status = False
                
                image_index, event_id = self._get_next_image(self.image_index + 1)
                event_data = EventDataManager.get_event_id_data(event_id)
                if event_data:
                    event_index = event_data[EVENT_INDEX]
                    if event_index in events_default_data:
                        self.SetImage(events_default_data[event_index][0])
                self.image_index = image_index
        else:
            self.alpha_value += self.increase_value
            if self.alpha_value > self.max_alpha:
                self.alpha_status = True
                self.sleep_time = app.GetTime() + self.waiting_time
        
        if self.mini_icon:
            self.mini_icon.SetAlpha(self.alpha_value)


class EventCalendarWindow(ui.ScriptWindow):
    """Main event calendar window"""
    
    def __init__(self):
        super(EventCalendarWindow, self).__init__()
        self._initialize_attributes()
        self._load_window()
    
    def __del__(self):
        super(EventCalendarWindow, self).__del__()
    
    def _initialize_attributes(self):
        """Initialize window attributes"""
        self.children = {}
        self.current_month = 0
        self.current_year = 0
        self.board = None
        self.exit_btn = None
        self.final_date_text = None
    
    def Destroy(self):
        """Clean up window resources"""
        self.children = {}
        self.current_month = 0
        self.current_year = 0
    
    def _load_window(self):
        """Load the window UI from script"""
        try:
            py_scr_loader = ui.PythonScriptLoader()
            py_scr_loader.LoadScriptFile(self, "uiscript/eventcalendar.py")
        except:
            exception.Abort("EventCalendar.LoadDialog.LoadScript")
        
        try:
            self.board = self.GetChild("board")
            self.exit_btn = self.GetChild("ExitButton")
            self.final_date_text = self.GetChild("final_date_text")
            
            self.exit_btn.SetEvent(ui.__mem_func__(self.Close))
        except:
            exception.Abort("EventCalendar.BindObjects")
        
        self._initialize_calendar()
    
    def _initialize_calendar(self):
        """Initialize the calendar grid"""
        dt = datetime.datetime.today()
        self.current_month, self.current_year = dt.month, dt.year
        day_count = EventDataManager.calculate_day_count(self.current_month, self.current_year)
        
        for day in range(day_count):
            self._create_day_element(day, dt)
        
        self.Refresh()
    
    def _create_day_element(self, day, current_date):
        """Create UI elements for a single day"""
        y_calculate = day // 8
        x_calculate = day - (y_calculate * 8)
        
        # Create day image box
        day_images = ImageBoxSpecial(False)
        day_images.SetParent(self.board)
        
        # Set background based on whether it's today
        if current_date.day == day + 1:
            day_images.SetBackgroundImage(IMG_DIR + "today_bg.png")
        else:
            day_images.SetBackgroundImage(IMG_DIR + "black_bg.png")
        
        day_images.SetPosition(8 + (x_calculate * 66), 8 + (y_calculate * 62))
        day_images.day_index = day + 1
        day_images.Show()
        self.children["dayImages%d" % day] = day_images
        
        # Create day number
        day_index = ui.NumberLine()
        day_index.SetParent(day_images)
        day_index.SetNumber(str(day + 1))
        day_index.SetPosition(8, 8)
        day_index.Show()
        self.children["dayIndex%d" % day] = day_index
    
    def Open(self):
        """Open the calendar window"""
        self.Show()
        self.Refresh()
        self.SetTop()
    
    def Close(self):
        """Close the calendar window"""
        self.Hide()
    
    def OnPressEscapeKey(self):
        """Handle escape key press"""
        self.Close()
        return True
    
    def OnUpdate(self):
        """Update all day elements"""
        for day_index in range(31):
            day_key = "dayImages%d" % day_index
            if day_key in self.children:
                self.children[day_key].OnUpdate()
    
    def Refresh(self):
        """Refresh the calendar display"""
        dt = datetime.datetime.today()
        day_count = EventDataManager.calculate_day_count(self.current_month, self.current_year)
        
        self.final_date_text.SetText(
            "|cFFe0c18c%02d-%02d  |r-  |cFFe0c18c%02d-%02d  |r(%04d)" %
            (self.current_month, 1, self.current_month, day_count, self.current_year)
        )
        
        for day_index in range(31):
            self._refresh_day(day_index, dt)
    
    def _refresh_day(self, day_index, current_date):
        """Refresh a single day's display"""
        day_key = "dayImages%d" % day_index
        if day_key not in self.children:
            return
        
        day_event_image = self.children[day_key]
        day_event_image.Clear()
        
        if (day_index + 1) in server_event_data:
            event_dict = server_event_data[day_index + 1]
            
            # Set background color based on whether it's today and has events
            if current_date.day == day_index + 1:
                day_event_image.SetBackgroundImage(IMG_DIR + "today_bg.png")
            else:
                day_event_image.SetBackgroundImage(IMG_DIR + "blue_bg.tga")
            
            # Add all events for this day
            for event_id in event_dict:
                day_event_image.AppendImage(event_id)
        else:
            # Set background for days without events
            if current_date.day == day_index + 1:
                day_event_image.SetBackgroundImage(IMG_DIR + "today_bg.png")
            else:
                day_event_image.SetBackgroundImage(IMG_DIR + "black_bg.png")
        
        day_event_image.Show()
    
    def OnClick(self, event_index):
        """Handle event click (to be implemented by subclasses)"""
        pass
    
    def _get_bonus_name(self, affect, value):
        """Get bonus name from affect and value"""
        return ItemToolTip.AFFECT_DICT[affect](value)
    
    def _calculate_time(self, event_index, start_time_text, end_time_text, end_time):
        """Calculate and format event time display"""
        empty_times = ("1970-01-01 03:00:00", "1970-01-01 02:00:00", 
                      "1970-01-01 01:00:00", "1970-01-01 00:00:00", "")
        
        if end_time_text in empty_times:
            start_time_second = start_time_text.split(" ")[1]
            return localeInfo.PVP_EVENT_TIME % start_time_second
        
        start_parts = start_time_text.split(" ")
        end_parts = end_time_text.split(" ")
        start_date, start_time = start_parts[0], start_parts[1]
        end_date, end_time = end_parts[0], end_parts[1]
        
        begin_text = ""
        end_text = ""
        
        if start_date != end_date:
            start_date_parts = start_date.split("-")
            end_date_parts = end_date.split("-")
            begin_text += start_date_parts[2] + "/" + start_date_parts[1] + " "
            end_text += end_date_parts[2] + "/" + end_date_parts[1] + " "
        
        begin_text += start_time
        end_text += end_time
        
        return localeInfo.NORMAL_EVENT_TIME % (begin_text, end_text)
    
    def _get_map_name(self, map_index):
        """Get map name from map index"""
        map_names = {
            61: localeInfo.MOUNT_SOHAN_MAP_NAME,
            62: localeInfo.MOUNT_DOYUMHWAN_MAP_NAME,
            63: localeInfo.MOUNT_YONGBI_MAP_NAME,
        }
        return map_names.get(map_index, "Unknown Map Name")
    
    def OverInItem(self, day_index):
        """Handle mouse over item to show tooltip"""
        interface = constInfo.GetInterfaceInstance()
        if not interface or not interface.tooltipItem:
            return
        
        tooltip_item = interface.tooltipItem
        tooltip_item.ClearToolTip()
        tooltip_item.ShowToolTip()
        tooltip_item.SetTitle(
            localeInfo.EVENT_TOOLTIP_TITLE % 
            "%04d-%02d-%02d" % (self.current_year, self.current_month, day_index)
        )
        tooltip_item.AppendSpace(5)
        
        if day_index in server_event_data:
            self._add_event_tooltips(tooltip_item, server_event_data[day_index])
        else:
            tooltip_item.AppendTextLine(localeInfo.EVENT_TOOLTIP_DOESNT_HAVE_EVENT)
    
    def _add_event_tooltips(self, tooltip_item, event_list):
        """Add event information to tooltip"""
        for event_id, event_data in event_list.items():
            self._add_single_event_tooltip(tooltip_item, event_data)
    
    def _add_single_event_tooltip(self, tooltip_item, event_data):
        """Add a single event's information to tooltip"""
        event_name = ""
        top_info = ""
        
        empire_texts = [
            localeInfo.ALL_KINGDOMS, localeInfo.RED_KINGDOM,
            localeInfo.YELLOW_KINGDOM, localeInfo.BLUE_KINGDOM
        ]
        
        empire_flag = event_data[EVENT_EMPIRE_FLAG]
        if empire_flag >= len(empire_texts):
            empire_flag = 0
        top_info += empire_texts[empire_flag] + ", "
        
        if event_data[EVENT_CHANNEL_FLAG] == 0:
            top_info += "|cFF97AE99" + localeInfo.ALL_CHANNEL + "|r "
        else:
            top_info += ("|cFF97AE99" + localeInfo.ONLY_CHANNEL + "|r") % event_data[EVENT_CHANNEL_FLAG]
        
        if self._handle_special_event_tooltip(tooltip_item, event_data):
            return
        
        event_index = event_data[EVENT_INDEX]
        if event_index == player.BONUS_EVENT:
            if event_data[EVENT_VALUE0] > 0 and event_data[EVENT_VALUE1] > 0:
                event_name += (events_default_data[event_index][1] + " " + 
                             self._get_bonus_name(event_data[EVENT_VALUE0], event_data[EVENT_VALUE1]))
            else:
                event_name += events_default_data[event_index][1] + " " + localeInfo.NONE_AFFECT
        elif event_index in (player.ITEM_DROP_EVENT, player.EXP_EVENT):
            event_name += events_default_data[event_index][1] % event_data[EVENT_VALUE0]
        else:
            event_name += events_default_data[event_index][1]
        
        tooltip_item.AppendTextLine(event_name)
        tooltip_item.AppendSpace(5)
        tooltip_item.AppendTextLine(top_info)
        tooltip_item.AppendSpace(5)
        tooltip_item.AppendTextLine(
            self._calculate_time(event_index, event_data[EVENT_START_TEXT], 
                               event_data[EVENT_END_TEXT], event_data[EVENT_END_TIME])
        )
        tooltip_item.AppendSpace(5)
        tooltip_item.AppendTextLine("-" * 41)
        tooltip_item.ResizeToolTipWidth(272)
        tooltip_item.AlignTextLineHorizonalCenter()
    
    def _handle_special_event_tooltip(self, tooltip_item, event_data):
        """Handle special event types that need custom tooltip formatting"""
        event_index = event_data[EVENT_INDEX]
        
        if event_index == player.NPC_SEARCH_EVENT:
            tooltip_item.AppendTextLine(localeInfo.NPC_SEARCH)
            tooltip_item.AppendTextLine(localeInfo.NPC_SEARCH_TEXT)
            
            for j in range(4):
                if event_data[EVENT_VALUE0 + j] > 0:
                    tooltip_item.AppendTextLine(self._get_map_name(event_data[EVENT_VALUE0 + j]))
            
            tooltip_item.AppendSpace(5)
            tooltip_item.AppendTextLine(
                self._calculate_time(event_index, event_data[EVENT_START_TEXT], 
                                   event_data[EVENT_END_TEXT], event_data[EVENT_END_TIME])
            )
            tooltip_item.AppendSpace(5)
            tooltip_item.AppendTextLine("-" * 41)
            tooltip_item.AppendTextLine("")
            return True
        
        elif event_index == player.SWITCH_AVERAGE_EVENT:
            tooltip_item.AppendTextLine(localeInfo.SWITCH_AVERAGE_EVENT)
            tooltip_item.AppendTextLine(localeInfo.SWITCH_AVERAGE_EVENT_TEXT)
            tooltip_item.AppendSpace(5)
            tooltip_item.AppendTextLine(
                self._calculate_time(event_index, event_data[EVENT_START_TEXT], 
                                   event_data[EVENT_END_TEXT], event_data[EVENT_END_TIME])
            )
            tooltip_item.AppendSpace(5)
            tooltip_item.AppendTextLine("-" * 41)
            return True
        
        elif event_index == player.SWITCH_RUNE_EVENT:
            tooltip_item.AppendTextLine(localeInfo.SWITCH_RUNE_EVENT)
            tooltip_item.AppendTextLine(localeInfo.SWITCH_RUNE_EVENT_TEXT)
            tooltip_item.AppendSpace(5)
            tooltip_item.AppendTextLine(
                self._calculate_time(event_index, event_data[EVENT_START_TEXT], 
                                   event_data[EVENT_END_TEXT], event_data[EVENT_END_TIME])
            )
            tooltip_item.AppendSpace(5)
            tooltip_item.AppendTextLine("-" * 41)
            return True
        
        return False


class MovableImage(ImageBoxSpecial):
    """Movable image widget for displaying active events"""
    
    def __init__(self):
        super(MovableImage, self).__init__(is_mini_icon=True)
        self._initialize_movable_attributes()
        self._create_ui_elements()
    
    def __del__(self):
        super(MovableImage, self).__del__()
    
    def _initialize_movable_attributes(self):
        """Initialize attributes specific to movable image"""
        self.window = None
        self.event_cache = []
        self.time_list = []
        self.time_text = None
        self.time_text_ex = None
    
    def Destroy(self):
        """Clean up movable image resources"""
        self.window = None
        self.event_cache = []
        self.time_list = []
        self.time_text = None
        super(MovableImage, self).Destroy()
    
    def _create_ui_elements(self):
        """Create UI elements for the movable image"""
        # Create window container
        window = ui.Window()
        window.SetParent(self)
        window.AddFlag("not_pick")
        window.OnUpdate = ui.__mem_func__(self.OnUpdate)
        window.Show()
        self.window = window
        
        # Create time text
        time_text = ui.TextLine()
        time_text.SetParent(self)
        time_text.AddFlag("not_pick")
        time_text.SetHorizontalAlignCenter()
        time_text.SetPosition(25, 55)
        time_text.SetOutline()
        time_text.Show()
        self.time_text = time_text
        
        # Create additional time text
        time_text_ex = ui.TextLine()
        time_text_ex.SetParent(self)
        time_text_ex.AddFlag("not_pick")
        time_text_ex.SetHorizontalAlignCenter()
        time_text_ex.SetPosition(25, 73)
        time_text_ex.SetText(localeInfo.BONUS_NEXT_EVENT)
        time_text_ex.SetOutline()
        time_text_ex.Show()
        self.time_text_ex = time_text_ex
    
    def Clear(self):
        """Clear all event data"""
        self.event_cache = []
        self.time_list = []
        self.time_text.SetText("")
        self.time_text_ex.Hide()
        super(MovableImage, self).Clear()
        self.Hide()
    
    def Refresh(self):
        """Refresh all events from server data"""
        self.Clear()
        for day_index, event_list in server_event_data.items():
            for event_id, event_data in event_list.items():
                self.AppendEvent(
                    event_data[EVENT_ID], event_data[EVENT_START_TIME],
                    event_data[EVENT_END_TIME], event_data[EVENT_IS_ACTIVE]
                )
    
    def LoadTime(self, event_id, start_time, end_time, is_already_start):
        """Load time information for an event"""
        self.AppendImage(event_id)
        self.time_list.append([start_time, end_time, is_already_start])
        
        if len(self.time_list) > 1:
            self.time_text_ex.Show()
        else:
            self.time_text_ex.Hide()
        
        self.Show()
    
    def CheckCacheEvent(self):
        """Check cached events for upcoming starts"""
        if len(self.event_cache) == 0:
            return
        
        client_global_time = app.GetGlobalTimeStamp()
        for j in range(len(self.event_cache)):
            start_time = self.event_cache[j][1] - client_global_time
            if 0 <= start_time <= (60 * 30):  # 30 minutes
                self.Refresh()
                return
    
    def AppendEvent(self, event_id, start_time, end_time, is_already_start):
        """Add an event to the display"""
        client_global_time = app.GetGlobalTimeStamp()
        
        new_start_time = start_time - client_global_time if start_time != 0 else 0
        new_end_time = end_time - client_global_time if end_time != 0 else 0
        
        if self._is_permanent_event(start_time, end_time, new_start_time, is_already_start):
            self.LoadTime(event_id, start_time, end_time, 2)
        elif new_start_time <= 0 and new_end_time <= 0:
            return
        elif 0 < new_start_time <= (60 * 30):
            self.LoadTime(event_id, start_time, end_time, 0)
        elif new_end_time > 0 and is_already_start:
            self.LoadTime(event_id, start_time, end_time, 1)
        else:
            self.event_cache.append([event_id, start_time, end_time, is_already_start])
        
        if len(self.time_list) > 1:
            self.time_text_ex.Show()
        else:
            self.time_text_ex.Hide()
    
    def _is_permanent_event(self, start_time, end_time, new_start_time, is_already_start):
        """Check if event is a permanent/ongoing event"""
        return ((start_time != 0 and new_start_time <= 0 and end_time == start_time and is_already_start) or
                (start_time != 0 and new_start_time <= 0 and end_time == 0 and is_already_start))
    
    def DeleteEvent(self, index):
        """Remove an event from the display"""
        self.DeleteImage(index)
        if 0 <= index < len(self.time_list):
            del self.time_list[index]
        
        if len(self.time_list) <= 1:
            self.time_text_ex.Hide()
    
    def FormatTime(self, seconds):
        """Format seconds into human-readable time"""
        if seconds == 0:
            return ""
        
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%02dh %02dm %02ds" % (h, m, s)
    
    def OnUpdate(self):
        """Update the movable image display"""
        super(MovableImage, self).OnUpdate()
        self.CheckCacheEvent()
        
        if self.image_index < len(self.time_list):
            time_data = self.time_list[self.image_index]
            self._update_time_display(time_data)
    
    def _update_time_display(self, time_data):
        """Update the time display based on event status"""
        if time_data[2] == 0:  # Event starting soon
            left_time = time_data[0] - app.GetGlobalTimeStamp()
            if left_time > 0:
                self.time_text.SetText("Za�ne za: " + localeInfo.BONUS_START_IN % self.FormatTime(left_time))
                if not self.time_text.IsShow():
                    self.time_text.Show()
        
        elif time_data[2] == 1:  # Event ending soon
            left_time = time_data[1] - app.GetGlobalTimeStamp()
            if left_time > 0:
                self.time_text.SetText(
                    "{} ".format(emoji.AppendEmoji("icon/emoji/image-example-007.png")) +
                    localeInfo.BONUS_END_IN % self.FormatTime(left_time)
                )
                self.time_text.SetFontName("Tahoma:14")
                if not self.time_text.IsShow():
                    self.time_text.Show()
        
        elif time_data[2] == 2:  # Permanent event
            if self.time_text.IsShow():
                self.time_text.Hide()


# Module-level functions for backward compatibility
def CalculateDayCount(month, year):
    return EventDataManager.calculate_day_count(month, year)

def SetEventStatus(eventID, eventStatus, endTime, endTimeText):
    EventDataManager.set_event_status(eventID, eventStatus, endTime, endTimeText)

def SetServerData(dayIndex, eventID, eventIndex, startTime, endTime, empireFlag, 
                 channelFlag, value0, value1, value2, value3, startRealTime, 
                 endRealTime, isAlreadyStart):
    EventDataManager.set_server_data(dayIndex, eventID, eventIndex, startTime, endTime, 
                                   empireFlag, channelFlag, value0, value1, value2, value3, 
                                   startRealTime, endRealTime, isAlreadyStart)

def IsEventIDActive(eventID):
    return EventDataManager.is_event_id_active(eventID)

def IsEventIndexActive(eventIndex):
    return EventDataManager.is_event_index_active(eventIndex)

def GetEventIndexData(eventIndex):
    return EventDataManager.get_event_index_data(eventIndex)

def GetEventIDData(eventID):
    return EventDataManager.get_event_id_data(eventID)
	