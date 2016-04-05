Write-Host "Starting"
Write-Host "CFGrammar 12 4 N"
Measure-Command {python ./CFGrammar.py 12 4 ./rockyou-withcount.txt 12-4-N.gr} > 12-4-N.time
Write-Host "CFGrammar 12 5 N"
Measure-Command {python ./CFGrammar.py 12 5 ./rockyou-withcount.txt 12-5-N.gr} > 12-5-N.time

Write-Host "CFGrammar 12 4 A"
Measure-Command {python ./CFGrammar.py 12 4 ./rockyou-withcount.txt 12-4-A.gr 1} > 12-4-A.time
Write-Host "CFGrammar 12 5 A"
Measure-Command {python ./CFGrammar.py 12 5 ./rockyou-withcount.txt 12-5-A.gr 1} > 12-5-A.time

Write-Host "CFGrammar 13 4 N"
Measure-Command {python ./CFGrammar.py 13 4 ./rockyou-withcount.txt 13-4-N.gr} > 13-4-N.time
Write-Host "CFGrammar 14 4 N"
Measure-Command {python ./CFGrammar.py 14 4 ./rockyou-withcount.txt 14-4-N.gr} > 14-4-N.time