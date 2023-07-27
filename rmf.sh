#bash
#C:\Users\Owner\Documents\GitHub\tabs\venv\Scripts\

function cleanup {
  dir="$1"
  ext="$2"
  all="$3"
  echo BGN cleanup all = "$all" "$ext" files: in "$dir"
  ls "$dir"
  for file in "$dir"/*; do
    if [[ $all = 0 ]]; then
      if [[ $file = *[0-9]*.$ext ]]; then
        echo rm "$file"
        rm      "$file"
      fi
    else
      if [[ $file = *.$ext ]]; then
        echo rm "$file"
        rm      "$file"
      fi
    fi
  done
  echo END cleanup "$ext" files: in "$dir"
  ls "$dir"
}

echo ARG1 \(root\) = "$1"
if [[ $1 = "" ]]; then
  echo "Error - Missing arg1 (root dir name) - Exit"
  exit
fi
root="$1"

echo pwd
pwd
echo cd "$root" || exit
cd      "$root" || exit
echo pwd
pwd
echo ls
ls

echo ARG2 \(all\) = "$2"
if [[ $2 = "all" ]]; then
  all=1
else
  all=0
fi
echo "all =" "$all"

dir=.
echo exts='("csv" "log" "png" "txt")'
exts=(      "csv" "log" "png" "txt")
echo "   >>> Removing Files from root Dir =" "$root" ">>> ..."
for ext in "${exts[@]}"  ; do
  echo cleanup "$dir" "$ext" "$all" files
  cleanup      "$dir" "$ext" "$all"
done

echo exts='("cat" "csv" "dat" "log" "png" "txt")'
exts=(      "cat" "csv" "dat" "log" "png" "txt")
echo "   >>> Removing Files from SubDirs of" "$root" "with type" "cat csv dat log png txt >>> ..."
for ext in "${exts[@]}"  ; do
  if   [[ $ext = "dat" ]]; then
    dir="$ext"a
    echo cleanup "$dir" "$ext" "$all"
    cleanup      "$dir" "$ext" "$all"
  elif [[ $ext = "std" ]]; then
    dir="$ext"o
    echo cleanup "$dir" "$ext" "$all"
    cleanup      "$dir" "$ext" "$all"
  elif [[ $ext = "txt" ]]; then
    dir="text"
    echo cleanup "$dir" "$ext" "$all"
    cleanup      "$dir" "$ext" "$all"
  else
    dir="$ext"s
    echo cleanup "$dir" "$ext" "$all"
    cleanup      "$dir" "$ext" "$all"
  fi
done
