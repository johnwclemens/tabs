#bash
#C:\Users\Owner\Documents\GitHub\tabs\venv\Scripts\
echo pwd
pwd

function cleanup {
  for file in "$1"s/*
  do
    if [[ $file = *[0-9]*.$1 ]]; then
      echo rm "$file"
      rm "$file"
    fi
  done
  echo ls -l "$1"s
  ls      -l "$1"s
}

cleanup "log"
cleanup "png"
cleanup "csv"
cleanup "cat"
