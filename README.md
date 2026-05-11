Cześć,

Chciałbym, żebyście napisali program,
który rozdzieli mandaty w wyborach parlamentarnych
zgodnie z metodą D’Hondta na podstawie liczby głosów oddanych na partie.
Program powinien wczytać liczbę partii.
Dla każdej partii wczytujemy jej nazwę i liczbę głosów, które otrzymała.
Następnie wczytujemy liczbę mandatów do przydzielenia.
Uwzględniamy próg wyborczy (partia musi mieć min. 5% głosów, żeby brać
udział w przydzielaniu mandatów).
Stosujemy metodę D’Hondta:
liczymy ilorazy:  głosy / (1, 2, 3, ..., n) gdzie n jest liczbą mandatów,
wybieramy największą liczbę i przydzielamy
mandat partii, która miała największy iloraz, następnie usuwamy ten największy
iloraz i powtarzamy rozumowanie do momentu gdy rozdamy wszystkie mandaty.
Jeżeli dwa lub więcej ilorazów są sobie równe, to przydzielamy mandat w sposób losowy.
Po wyznaczeniu liczby mandatów dla partii wyświetlamy wynik w postaci wykresu słupkowego.
Rozwiązanie powinno zostać zaimplementowane obiektowo oraz optymalnie zarówno
pod względem czasowym jak i pamięciowym.

Powodzenia