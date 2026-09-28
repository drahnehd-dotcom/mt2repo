# -*- coding: iso-8859-1 -*-
import net
import ui
import uiToolTip
import player
import item
import exception
import chat
import constInfo


class BonusChangerConfig(object):
    """Configuration class for bonus changer constants and settings."""
    
    MAX_BONUSES = 5

    # Domyslny kolor linii bonusu (taki sam jak "color" w uiscript/bonuschanger.py).
    # Uzywany dla bonusow, ktore nie sa maksymalne, i jako fallback.
    DEFAULT_BONUS_COLOR = 0xff89b88d

    # UI component names
    UI_COMPONENTS = {
        'title_bar': "TitleBar",
        'items_slots': "ItemsSlots", 
        'change_button': "ChangeButton",
        'bonus_names': ["BonusName1", "BonusName2", "BonusName3", "BonusName4", "BonusName5"]
    }
    
    # Item slots
    ITEM_SLOT = 0
    CHANGER_SLOT = 1


class ItemSlotManager(object):
    """Manages item slot operations and validation."""
    
    @staticmethod
    def is_valid_item_type():
        """Check if current item type is valid for bonus changing."""
        return (item.GetItemType() == item.WEAPON or 
                item.GetItemType() == item.ARMOR)
    
    @staticmethod
    def get_item_attributes(position, max_bonuses):
        """Get item attributes for the specified position."""
        return [player.GetItemAttribute(position, i) for i in range(max_bonuses)]
    
    @staticmethod
    def get_item_info(position):
        """Get item index and count for the specified position."""
        return {
            'index': player.GetItemIndex(position),
            'count': player.GetItemCount(position)
        }


class BonusFormatter(object):
    """Handles bonus name formatting and display."""
    
    def __init__(self, tooltip_instance):
        self.tooltip = tooltip_instance
    
    def get_bonus_name(self, affect_type, affect_value):
        """Get formatted bonus name string."""
        if affect_type == 0 or affect_value == 0:
            return None
        
        try:
            return self.tooltip.AFFECT_DICT[affect_type](affect_value)
        except (TypeError, KeyError):
            return None
    
    def get_bonus_color(self, index, affect_type, affect_value):
        """Kolor bonusu wg kolorystyki tooltipa (bonus maksymalny = zloto)."""
        try:
            return self.tooltip.GetAttributeColor(index, affect_value, affect_type)
        except (TypeError, KeyError, AttributeError):
            return BonusChangerConfig.DEFAULT_BONUS_COLOR

    def format_bonus_list(self, attributes):
        """Format a list of bonus attributes -> [(text, color), ...]."""
        bonus_entries = []
        for index, (attr_type, attr_value) in enumerate(attributes):
            bonus_name = self.get_bonus_name(attr_type, attr_value)
            if not bonus_name:
                bonus_entries.append(("", BonusChangerConfig.DEFAULT_BONUS_COLOR))
                continue

            bonus_entries.append(
                (bonus_name, self.get_bonus_color(index, attr_type, attr_value))
            )
        return bonus_entries


class ChangerWindow(ui.ScriptWindow):
    """Enhanced bonus changer window with modern Python practices."""
    
    def __init__(self):
        super(ChangerWindow, self).__init__()
        
        # Initialize state
        self._changer_position = None
        self._item_position = None
        self._changers_count = 0
        self._is_loaded = False
        # Snapshot stanu obu slotow - OnUpdate leci co KLATKE (CWindow::Update),
        # wiec przerysowujemy dopiero gdy cos sie naprawde zmienilo.
        self._last_slots_state = None

        # UI components (will be initialized in LoadWindow)
        self.TitleBar = None
        self.ItemsSlots = None
        self.Bonuses = []
        self.ChangeBonusButton = None
        self.ItemToolTip = None
        
        # Helper objects
        self._bonus_formatter = None
    
    def __del__(self):
        super(ChangerWindow, self).__del__()
    
    def LoadWindow(self):
        """Load and initialize the window UI."""
        if self._is_loaded:
            return
        
        try:
            PythonScriptLoader = ui.PythonScriptLoader()
            PythonScriptLoader.LoadScriptFile(self, "UIScript/bonuschanger.py")
        except:
            exception.Abort("ChangerWindow.LoadDialog.LoadObject")
        
        self._bind_ui_components()
        self._setup_events()
        self._initialize_tooltip()
        
        self._is_loaded = True
    
    def _bind_ui_components(self):
        """Bind UI components from the script."""
        try:
            config = BonusChangerConfig.UI_COMPONENTS
            
            self.TitleBar = self.GetChild(config['title_bar'])
            self.ItemsSlots = self.GetChild(config['items_slots'])
            self.ChangeBonusButton = self.GetChild(config['change_button'])
            
            # Bind bonus name components
            self.Bonuses = []
            for bonus_name in config['bonus_names']:
                self.Bonuses.append(self.GetChild(bonus_name))
                
        except:
            exception.Abort("ChangerWindow.LoadDialog.BindObject")
    
    def _setup_events(self):
        """Setup event handlers for UI components."""
        self.ChangeBonusButton.SetEvent(ui.__mem_func__(self.ChangeBonus))
        self.TitleBar.SetCloseEvent(ui.__mem_func__(self.Close))
        self.ItemsSlots.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
        self.ItemsSlots.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
    
    def _initialize_tooltip(self):
        """Initialize the item tooltip."""
        self.ItemToolTip = uiToolTip.ItemToolTip()
        self.ItemToolTip.Hide()
        self._bonus_formatter = BonusFormatter(self.ItemToolTip)
    
    def OverInItem(self, slot):
        """Handle mouse over item event."""
        if not self._is_valid_tooltip_state():
            return
        
        if slot == BonusChangerConfig.ITEM_SLOT:
            self.ItemToolTip.SetInventoryItem(self._item_position)
            self.ItemToolTip.Show()
        elif slot == BonusChangerConfig.CHANGER_SLOT:
            self.ItemToolTip.SetInventoryItem(self._changer_position)
            self.ItemToolTip.Show()
    
    def OverOutItem(self):
        """Handle mouse out item event."""
        if self.ItemToolTip:
            self.ItemToolTip.Hide()
    
    def _is_valid_tooltip_state(self):
        """Check if tooltip can be displayed."""
        return (self.ItemToolTip and 
                self._item_position is not None and 
                self._changer_position is not None)
    
    def AddItems(self, item_position, changer_position):
        """Add items to the changer window."""
        if not ItemSlotManager.is_valid_item_type():
            return

        # Check if item has at least 1 bonus
        attributes = ItemSlotManager.get_item_attributes(item_position, BonusChangerConfig.MAX_BONUSES)
        if not any(attr_value != 0 for _, attr_value in attributes):
            return

        # Store positions
        self._item_position = item_position
        self._changer_position = changer_position
        
        # Update item display
        self._update_item_slots()
        self._update_bonus_display()
        
        # Update changer count and open window
        changer_info = ItemSlotManager.get_item_info(self._changer_position)
        self._changers_count = changer_info['count']
        
        self.Open()
    
    def _update_item_slots(self):
        """Update the item slot display."""
        if self._item_position is None or self._changer_position is None:
            return

        if not self.ItemsSlots:
            return

        item_info = ItemSlotManager.get_item_info(self._item_position)
        changer_info = ItemSlotManager.get_item_info(self._changer_position)
        
        self.ItemsSlots.SetItemSlot(
            BonusChangerConfig.ITEM_SLOT, 
            item_info['index'], 
            0
        )
        self.ItemsSlots.SetItemSlot(
            BonusChangerConfig.CHANGER_SLOT, 
            changer_info['index'], 
            changer_info['count']
        )
    
    def _update_bonus_display(self):
        """Update the bonus display for the current item."""
        if self._item_position is None or not self._bonus_formatter:
            return

        # Kolory bonusow zaleza od typu/podtypu przedmiotu (tooltip trzyma osobne
        # tablice MAX_AFFECT_VALUE dla broni/zbroi, pasa i rekawic), a te czyta sie
        # z aktualnie wybranego itemu - trzeba go wybrac przed liczeniem kolorow.
        # OnUpdate leci przy kazdym odswiezeniu ekwipunku, wiec selekcja moze byc inna.
        itemVnum = player.GetItemIndex(self._item_position)
        if itemVnum:
            item.SelectItem(itemVnum)

        attributes = ItemSlotManager.get_item_attributes(
            self._item_position,
            BonusChangerConfig.MAX_BONUSES
        )

        bonus_entries = self._bonus_formatter.format_bonus_list(attributes)

        for i, (bonus_text, bonus_color) in enumerate(bonus_entries):
            if i < len(self.Bonuses) and self.Bonuses[i]:
                self.Bonuses[i].SetText(bonus_text)
                self.Bonuses[i].SetPackedFontColor(bonus_color)
    
    def ChangeBonus(self):
        """Execute bonus change operation."""
        if not self._can_change_bonus():
            return
        
        if self._changers_count > 0:
            self._execute_bonus_change()
    
    def _can_change_bonus(self):
        """Check if bonus change is possible."""
        return (self._changer_position is not None and 
                self._item_position is not None)
    
    def _execute_bonus_change(self):
        """Execute the actual bonus change."""
        # Samo wyslanie pakietu. Slot zmianki NIE jest odswiezany optymistycznie:
        # w tym momencie klient ma jeszcze stary stan ekwipunku, a serwer zbija
        # count dopiero po przetworzeniu pakietu. Nowa ilosc dojdzie przez
        # RefreshInventory -> UpdateBonusChanger -> OnUpdate.
        net.SendItemUseToItemPacket(self._changer_position, self._item_position)

    def _get_slots_state(self):
        """Snapshot stanu obu slotow - do wykrywania zmian bez pracy co klatke."""
        if self._item_position is None or self._changer_position is None:
            return None

        attributes = ItemSlotManager.get_item_attributes(
            self._item_position,
            BonusChangerConfig.MAX_BONUSES
        )

        return (
            player.GetItemIndex(self._item_position),
            player.GetItemIndex(self._changer_position),
            player.GetItemCount(self._changer_position),
            tuple(attributes),
        )

    def OnUpdate(self):
        """Handle window updates."""
        if not constInfo.IS_BONUS_CHANGER:
            return

        state = self._get_slots_state()
        if state is None or state == self._last_slots_state:
            return

        self._last_slots_state = state

        # Ilosc zmianek trzymamy zsynchronizowana z ekwipunkiem - inaczej licznik
        # w slocie stoi na wartosci z chwili otwarcia okna, a ChangeBonus() puszcza
        # pakiety mimo zuzycia calego stacka.
        self._changers_count = state[2]

        self._update_item_slots()
        self._update_bonus_display()
    
    def Destroy(self):
        """Destroy the window and clean up resources."""
        self._cleanup_state()
        self.Close()
    
    def _cleanup_state(self):
        """Clean up internal state."""
        self._changer_position = None
        self._item_position = None
        self._changers_count = 0
        self._last_slots_state = None

        if self.ItemToolTip:
            self.ItemToolTip.Hide()
    
    def OnPressEscapeKey(self):
        """Handle escape key press."""
        self.Close()
        return True
    
    def Close(self):
        """Close the window."""
        if self.IsShow():
            self._cleanup_state()
            constInfo.IS_BONUS_CHANGER = False
            self.Hide()
    
    def Open(self):
        """Open the window."""
        self.LoadWindow()
        constInfo.IS_BONUS_CHANGER = True
        self.Show()
        self.SetCenterPosition()
    
    @property
    def ChangerPosition(self):
        """Legacy property accessor."""
        return self._changer_position
    
    @ChangerPosition.setter
    def ChangerPosition(self, value):
        """Legacy property setter."""
        self._changer_position = value
    
    @property
    def ItemPosition(self):
        """Legacy property accessor."""
        return self._item_position
    
    @ItemPosition.setter
    def ItemPosition(self, value):
        """Legacy property setter."""
        self._item_position = value
    
    @property
    def ChangersCount(self):
        """Legacy property accessor."""
        return self._changers_count
    
    @ChangersCount.setter
    def ChangersCount(self, value):
        """Legacy property setter."""
        self._changers_count = value
		