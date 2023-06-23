#bash
#C:\Users\Owner\Documents\GitHub\tabs\venv\Scripts\

function cleanup {
  echo BGN cleanup: ls "$1"
  ls "$1"
  for file in "$1"/*; do
#    if [[ $file = *[0-9]*.$1 ]]; then
    echo rm "$file"
    rm      "$file"
  done
  echo END cleanup: ls "$1"
  ls "$1"
}

echo pwd
pwd
echo ls test
ls      test

echo cd "test" || exit
cd      "test" || exit

echo pwd
pwd
echo ls
ls

echo dirs='("csv" "dat" "log" "png" "std" "cat")'
dirs=(      "csv" "dat" "log" "png" "std" "cat")

for dir in "${dirs[@]}"  ; do
  if   [[ $dir = "dat" ]]; then
    echo cleanup "$dir"a
    cleanup      "$dir"a
  elif [[ $dir = "std" ]]; then
    echo cleanup "$dir"o
    cleanup      "$dir"o
  else
    echo cleanup "$dir"s
    cleanup      "$dir"s
  fi
done
