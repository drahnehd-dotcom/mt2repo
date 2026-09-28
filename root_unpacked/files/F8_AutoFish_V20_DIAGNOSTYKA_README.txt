V20 Auto Fish - diagnostyka

- Okno Auto Fish 560x500.
- Statystyki: Łowienia, Wyłowione, Niepowodzenia.
- Suwak czasu oczekiwania po wyniku 1.0-10.0 s.
- Zakres losowego opóźnienia między kolejnymi użyciami skilla w ms (domyślnie 20-100).
- Szczegółowe logi na czacie [F8 Auto Fish]: ładowanie skilla, slot/index, cooldown, wykrycie brania, każde użycie skilla, callback sukces/porażka, koniec cyklu.
- Parser instrukcji x2/x3 usuwa kody koloru/formatowania klienta przed dopasowaniem.
- Dokładna liczba x jest używana, jeśli komunikat przejdzie przez Python chat hook.
- Jeśli komunikat jest tworzony bezpośrednio w natywnym CPythonChat, OnFishingNotify nadal loguje moment brania.
- Wbudowany fallback uiFarmFishing w uiRespawn.py został zaktualizowany do tej samej wersji.
