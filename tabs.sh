#bash
#C:\Users\Owner\Documents\GitHub\tabs\venv\Scripts\
echo pwd
pwd
path=test/stdo
echo ls -l $path
ls      -l $path
echo cksum $path/test*.txt
cksum      $path/test*.txt
echo cp    $path/test.txt $path/test._.txt
cp         $path/test.txt $path/test._.txt
echo ls -l $path
ls      -l $path
echo cksum $path/tabs*.txt
cksum      $path/tabs*.txt
echo python tabsC.py -i 1 8 8 8 -n 1 1 10 5 -w 0 0 0 0 -d 1 -L -S 0 -f test 2&> $path/test.txt
python      tabsC.py -i 1 8 8 8 -n 1 1 10 5 -w 0 0 0 0 -d 1 -L -S 0 -f test 2&> $path/test.txt
echo ls -l $path
ls      -l $path
echo cksum $path/test*.txt
cksum      $path/test*.txt

#C:\Program Files\Git\usr\bin
#python tabsC.py -i 1 8 8 8 -n 1 1 10 5 -w 0 0 0 0 -d 1 -L -S 0 -f test | iconv -f cp1252 -t UTF-8 2&> $path/tabs.txt
#python tabsC.py -i 1 1 1 6 -n 1 1 10 5 -w 0 0 0 0 -d 1 -t -x 0 -L -S 0 -f test
#python tabsC.py -i 1 1 1 6 -n 1 1 10 6 -w 0 0 0 0 -t -L -S 0 -f test 2&> test/tabs.txt
#python tabsC.py -f BlackMagicWoman.4.2.50.dat -n 4 2 50 6 -S 0 1 3 -i 1 1 1 6
#python tabsC.py -f GiantSteps.50.dat -n 3 2 50 6 -S 0 1 3 -i 1 1 1 6
#python tabsC.py -f LydianTriads.50.dat -n 3 2 50 6 -S 0 1 3 -i 1 1 1 6 -L
#python tabsC.py -f Lydian.50.dat -n 3 2 50 6 -S 0 1 3 -L
#python tabsC.py -f PinkPanther.50.dat -n 1 2 50 6 -S 0 1 -L
#python tabsC.py -f improv_10_6_22.1.dat -n 1 2 30 6 -S 0 1 2 3 -L
#python tabsC.py -f C_Improv_11_24_22.0.dat -n 2 2 50 6 -S 0 1 3 -F
# 2&> $path/tabs.txt
