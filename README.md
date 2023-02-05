
# Wordle Helper

## K čemu program slouží

Jednoduchý program, který umí vyhledávat v českém slovníku slov o pěti písmenech 
a je možné ho použít jako pomůcku pro řešení wordle.

Je možné zadat známá písmena, písmena, která se v hledaném slově vyskytují, ale 
jsou na nesprávných místech, a také písmena, která se v hledaném slově nevyskytují. 
Jinými slovy, právě ty informace, které jsou známé k určitém tahu hádanky Wordle.

Program pak vypíše dvě sady informací.
+ **Nejlepší slova** - Slova, která splňují uvedená kritéria, seřazená podle toho, 
jak často se v nich vyskytují frekventovaná písmena. Frekvence písmen se ale 
nebere z celého slovníku, ale jen z té sady slov, která splňuje zadaná kritéria.  
Příklad: pokud je známý pattern ==se=, pak bude mezi nejlepšími slovy nejspíše slovo
s písmenem n na posledním místě, protože v zadaném slovníku existuje 17 slov, která
splňují daný pattern a z toho 6 končí písmenem n (ň).
+ **Četnosti znaků** - Pro každou pozici ve slově ukáže, jaké znaky se na dané pozici
mohou vyskytovat a s jakou četností. Opět jde jen o slova, která splňují daný pattern.

## Diakritika

Pokud jde o diakritiku, funguje program stejně jako český [Wordle](https://www.wordle.cz/),
tedy pracuje s klávesnicí bez diakritiky, ale ve výsledcích se diakritika zobrazuje.

## Slovník

Pochází odsud [http://ceskeforum.com/viewtopic.php?f=112&t=15201](http://ceskeforum.com/viewtopic.php?f=112&t=15201), 
ale i když obsahuje skoro 2000 tisíce slov, občas v něm chybí i něco obyčejného.

## Technicky

Jde o jednoduchou webovou stránku, která využívá Flask.
 