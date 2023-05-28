#bash
#C:\Users\Owner\Documents\GitHub\tabs\venv\Scripts\

function cleanup {
  for file in "$1"s/*
  do
    if [[ $file = *[0-9]*.$1 ]]; then
      echo rm "$file"
      rm "$file"
    fi
  done
  echo ls -l "$1"
  ls      -l "$1"
}

echo pwd
pwd

echo "dirs=(logs pngs csvs cats)"
dirs=("log" "png" "csv" "cat")

for dir in "${dirs[@]}"s; do
  cleanup "$dir"
done

echo "done cleaning file dirs"
echo "### ### ### ### ### ### ### ### ### ###"
echo "ls -lt logs pngs csvs cats"
ls -lt logs pngs csvs cats
