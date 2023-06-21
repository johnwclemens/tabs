#bash
#C:\Users\Owner\Documents\GitHub\tabs\venv\Scripts\

function cleanup {
  echo BGN cleanup "$1"
  echo ls "$1"
  ls "$1"
  for file in "$1"/*; do
    echo rm "$file"
    rm      "$file"
  done
  echo ls "$1"
  ls "$1"
  echo END cleanup "$1"
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

echo dirs='("log" "png" "csv" "cat")'
dirs=(     "log" "png" "csv" "cat")

for dir in "${dirs[@]}"; do
  echo cleanup "$dir"s
  cleanup      "$dir"s
done
