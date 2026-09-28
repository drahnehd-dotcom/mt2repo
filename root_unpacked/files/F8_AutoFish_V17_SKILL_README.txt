F8 AUTO FISH V17

Zmiana względem V16:
- okno Auto Fish ma dwa pola: PRZYNĘTA oraz SKILL ŁOWIENIA z V;
- skill można przeciągnąć bezpośrednio z okna V do pola skilla;
- bot używa player.ClickSkillSlot() zamiast wciskania SPACE;
- pierwszy użycie skilla zarzuca wędkę;
- po natywnym callbacku OnFishingNotify bot używa tego samego skilla ponownie jako akcji wyławiania;
- liczba akcji jest obsługiwana przez natywny wynik łowienia, a jako fallback bot wykonuje maksymalnie 3 użycia (obserwowany zakres 2x/3x);
- OnFishingSuccess / OnFishingFailure / OnFishingWrongPlace są przekazane bezpośrednio do Auto Fish;
- parsowanie chat.AppendChat pozostaje tylko jako dodatkowy fallback, nie jest wymagane do głównego sterowania.

Wymagane:
- wyposażona wędka,
- przynęta w EQ,
- skill SKILL_INDEX_FISHING dostępny w oknie V.
