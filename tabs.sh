#bash
#C:\Users\Owner\Documents\GitHub\tabs\venv\Scripts\
export LC_CTYPE=en_US.UTF-8

echo pwd
pwd
echo name=stdo
name=stdo
echo ext=std
ext=std
echo path=test/$name
path=test/$name
echo ls -l $path
ls      -l $path
echo cksum $path/$name*.$ext
cksum      $path/$name*.$ext
echo cp    $path/$name.$ext $path/$name._.$ext
cp         $path/$name.$ext $path/$name._.$ext
echo ls -l $path
ls      -l $path
echo cksum $path/$name*.$ext
cksum      $path/$name*.$ext
echo "!! execute the script !!"
echo python tabs.py -i 3 1 1 6 -n 3 1 10 6 -w 0 0 0 0 -d 0 -o -J 4 -S 0 -f test | iconv -f cp1252 -t UTF-8 &> $path/$name.$ext
python      tabs.py -i 3 1 1 6 -n 3 1 10 6 -w 0 0 0 0 -d 0 -o -J 4 -S 0 -f test | iconv -f cp1252 -t UTF-8 &> $path/$name.$ext
echo "!! script has returned !!"
echo ls -l $path
ls      -l $path
echo cksum $path/$name*.$ext
cksum      $path/$name*.$ext

#C:\Program Files\Git\usr\bin
#python tabs.py -i 1 1 1 6 -n 1 1 10 6 -w 0 0 0 0 -d 0 -L -S 0 -f test 2> test/stdo/stdo.std
#python tabs.py -i 1 8 8 8 -n 1 1 10 5 -w 0 0 0 0 -d 1 -L -S 0 -f test | iconv -f cp1252 -t UTF-8 2&> $path/tabs.txt
#python tabs.py -i 1 1 1 6 -n 1 1 10 5 -w 0 0 0 0 -d 1 -t -x 0 -L -S 0 -f test
#python tabs.py -i 1 1 1 6 -n 1 1 10 6 -w 0 0 0 0 -t -L -S 0 -f test 2&> test/tabs.txt
#python tabs.py -f BlackMagicWoman.4.2.50.dat -n 4 2 50 6 -S 0 1 3 -i 1 1 1 6
#python tabs.py -f GiantSteps.50.dat -n 3 2 50 6 -S 0 1 3 -i 1 1 1 6
#python tabs.py -f LydianTriads.50.dat -n 3 2 50 6 -S 0 1 3 -i 1 1 1 6 -L
#python tabs.py -f Lydian.50.dat -n 3 2 50 6 -S 0 1 3 -L
#python tabs.py -f PinkPanther.50.dat -n 1 2 50 6 -S 0 1 -L
#python tabs.py -f improv_10_6_22.1.dat -n 1 2 30 6 -S 0 1 2 3 -L
#python tabs.py -f C_Improv_11_24_22.0.dat -n 2 2 50 6 -S 0 1 3 -F
# 2&> $path/tabs.txt
