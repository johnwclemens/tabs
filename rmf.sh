#bash
#C:\Users\Owner\Documents\GitHub\tabs\venv\Scripts\

function cleanup {
  dir="$1"
  ext="$2"
  lvl="$3"
  dirs="$4"
  echo BGN cleanup dir = "$dir",  ext = "$ext",  lvl = "$lvl",  dirs = "$dirs"
  for dir2 in "${dirs[@]}"  ; do
    echo dir2 = "$dir2"
  done
  ls "$dir"
  for file in "$dir"/*; do
    if   [[ $lvl = 1 ]]; then
      if [[ $file = *.[0-9].$ext ]]; then
        echo rm "$file", lvl = "$lvl"
        rm "$file"
      fi
    elif [[ $lvl = 2 ]]; then
      if [[ $file = *.*.$ext ]]; then
        echo rm "$file", lvl = "$lvl"
        rm "$file"
      fi
    elif [[ $lvl = 3 ]]; then
      if [[ $file = *.$ext ]]; then
        echo rm "$file", lvl = "$lvl"
        rm "$file"
      fi
    elif [[ $lvl = 4 ]]; then
      echo rm "$file", lvl = "$lvl"
      rm "$file"
    else
      echo exit Error - Invalid value, lvl = "$lvl" check cmd line arg2 - Exit
      exit
    fi
  done
  echo ls "$dir"
  ls "$dir"
  echo END cleanup dir = "$dir",  ext = "$ext",  lvl = "$lvl",  dirs = "$dirs"
}

echo ARG1 \(root\) = "$1"
if [[ $1 = "" ]]; then
  echo exit Error - Missing arg1 \(root dir name\) - Exit
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

echo ARG2 \(lvl\) = "$2"
if   [[ $2 = "" ]]; then
  echo exit Error - Missing arg2 \(lvl\) - Exit
  exit
elif [[ $2 = 1 || $2 = 2 || $2 = 3 || $2 = 4 ]]; then
  echo lvl = "$2"
  lvl=$2
else
  echo exit Error - Invalid value, lvl = "$lvl" check cmd line arg2 - Exit
  exit
fi

dir=.
echo exts=\(csv   log   png   txt\)
exts=(     "csv" "log" "png" "txt")
echo "   >>> Removing Files from root Dir =" "$root" ">>> ..."
for ext in "${exts[@]}"  ; do
  echo cleanup "$dir" "$ext" "$lvl" "$dirs"
  cleanup      "$dir" "$ext" "$lvl" "$dirs"
done

echo dirs=\(cats   csvs   data   logs   pngs   text\)
dirs=(     "cats" "csvs" "data" "logs" "pngs" "text")

echo exts=\(cat   csv   dat   log   png   txt\)
exts=(     "cat" "csv" "dat" "log" "png" "txt")
echo "   >>> Removing Files from SubDirs of" "$root" "with type" "cat csv dat log png txt >>> ..."
for ext in "${exts[@]}"  ; do
  if   [[ $ext = "dat" ]]; then
    dir="$ext"a
    echo cleanup "$dir" "$ext" "$lvl" "${dirs[@]}"
    cleanup      "$dir" "$ext" "$lvl" "${dirs[@]}"
  elif [[ $ext = "std" ]]; then
    dir="$ext"o
    echo cleanup "$dir" "$ext" "$lvl" "${dirs[@]}"
    cleanup      "$dir" "$ext" "$lvl" "${dirs[@]}"
  elif [[ $ext = "txt" ]]; then
    dir="text"
    echo cleanup "$dir" "$ext" "$lvl" "${dirs[@]}"
    cleanup      "$dir" "$ext" "$lvl" "${dirs[@]}"
  else
    dir="$ext"s
    echo cleanup "$dir" "$ext" "$lvl" "${dirs[@]}"
    cleanup      "$dir" "$ext" "$lvl" "${dirs[@]}"
  fi
done
