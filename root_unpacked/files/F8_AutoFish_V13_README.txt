F8 AUTO FISH V13

Dodano do panelu F8:
- przycisk RYBY otwierający okno Auto Fish,
- wybór przynęty przez przeciągnięcie jej z normalnego EQ do slotu,
- Start / Stop,
- automatyczne użycie wybranej przynęty,
- automatyczny zarzut wędki przez natywny stan ataku,
- automatyczne naciskanie SPACE zgodnie z wykrytą liczbą X.

Ważne:
Klient EXE posiada natywny komunikat „To catch a fish, you must press %dx Space”,
ale obecny interfejs Python nie udostępnia wartości %d jako argumentu callbacka.
Moduł uiFarmFishing.py ma hook chat.AppendChat/AppendChatWithDelay i rozpoznaje
komunikat, jeżeli dana wersja klienta przekazuje go przez warstwę Python.

Jeżeli po teście komunikat X=2/X=3 pojawia się na czacie, ale bot nie reaguje,
oznacza to, że ta konkretna wersja EXE dodaje ten komunikat bezpośrednio w
CPythonChat. Wtedy potrzebna jest mała zmiana natywnego bindingu C++/EXE:
GetLastChatLine() albo bezpośredni callback z parametrem liczby SPACE.
Reszta automatycznego cyklu jest już przygotowana.
