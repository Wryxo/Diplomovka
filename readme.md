grammarCreator.py - Program, ktory na zaklade vstupneho suboru vytvori pravdepodobnostnu bezkontextovu gramatiku na generovanie hesiel

phpbb-withcount.txt - Ukazkovy vstupny subor s heslami

PCFGGenerator.py - Program generujuci hesla na zaklade vstupnej gramatiky vytvorenej programom grammarCreator.py

markovGenerator.py - Program vyuzivajuci Markovovske zdroje na generovanie potencialnych hesiel

markovGenerator-optimized.py - To iste co markovGenerator.py avsak s optimalizaciou prvkov co si treba pamatat

markovGeneratorV2.py - Nami navrhnuta varianta Markovovskych zdrojov generujuca aj retazce, ktore neboli videne vo vstupnom slovniku