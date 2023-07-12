#bash
#C:\Users\Owner\Documents\GitHub\tabs\venv\Scripts\

function cleanup {
  dir="$1"
  ext="$2"
  echo BGN cleanup "$ext" files: in "$dir"
  ls "$dir"
  for file in "$dir"/*; do
    if [[ $file = *[0-9]*.$ext ]]; then
      echo rm "$file"
      rm      "$file"
    fi
  done
  echo END cleanup "$ext" files: in "$dir"
  ls "$dir"
}

echo pwd
pwd

echo cd "test" || exit
cd      "test" || exit

echo pwd
pwd
echo ls
ls

echo exts='("csv" "dat" "log" "png" "std")'
exts=(      "csv" "dat" "log" "png" "std")
#echo exts='("csv" "dat" "log" "png" "std" "cat")'
#exts=(      "csv" "dat" "log" "png" "std" "cat")

for ext in "${exts[@]}"  ; do
  if   [[ $ext = "dat" ]]; then
    dir="$ext"a
    echo cleanup "$dir" "$ext"
    cleanup      "$dir" "$ext"
  elif [[ $ext = "std" ]]; then
    dir="$ext"o
    echo cleanup "$dir" "$ext"
    cleanup      "$dir" "$ext"
  else
    dir="$ext"s
    echo cleanup "$dir" "$ext"
    cleanup      "$dir" "$ext"
  fi
done
