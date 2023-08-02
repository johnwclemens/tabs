#bash
#C:\Users\Owner\Documents\GitHub\tabs\venv\Scripts\

function cleanRoot {
  lvl="$1"
  exts="$2"
  pwd
  echo find . -maxdepth 1 -type f ">>>"
  find      . -maxdepth 1 -type f
  echo BGN cleanRoot \(lvl exts\) = \("$lvl ${exts[*]}"\)
  for ext in "${exts[@]}"  ; do
    if   [[ $lvl = 2 ]]; then
      ls -l -- *."$ext"
    fi
    if [[ $lvl = 3 ]]; then
      ls -l -- *.dat;    break
    else
      echo ext = "$ext"
    fi
  done
  echo END cleanRoot \(lvl exts\) = \("$lvl ${exts[*]}"\)
}

function cleanSubDir {
  dirs="$1"
  ext="$2"
  lvl="$3"
  echo BGN cleanSubDir \(dirs ext lvl\) = \("$dirs $ext $lvl"\)
  ls -l "$dir"
  for file in "$dir"/*  ; do
    if   [[ $lvl = 1 ]]; then
      if [[ $file = *.[0-9].$ext ]]; then
        echo rm "$file" ">>>" lvl = "$lvl"
        rm "$file"
      fi
    elif [[ $lvl = 2 ]]; then
      if [[ $file = *.*.$ext ]]; then
        echo rm "$file" ">>>" lvl = "$lvl"
        rm "$file"
      fi
    elif [[ $lvl = 3 ]]; then
      if [[ $file = *.$ext ]]; then
        echo rm "$file" ">>>" lvl = "$lvl"
        rm "$file"
      fi
    elif [[ $lvl = 4 ]]; then
      echo rm "$file" ">>>" lvl = "$lvl"
      rm "$file"
    else
      echo exit ">>>" Error - Invalid value, lvl = "$lvl" check cmd line arg2 - Exit
      exit
    fi
  done
  echo ls "$dir"
  ls "$dir"
  echo END cleanSubDir \(dir ext lvl\) = \("$dir" "$ext" "$lvl"\)
}

echo ARG1 \(root\) = "$1"
if [[ $1 = "" ]]; then
  echo exit ">>>" Error - Missing arg1 \(root dir name\) ">>>" exit
  exit
fi

echo pwd
pwd
root="/c/Users/Owner/Documents/GitHub/Tabs/$1"
echo cd "$root" || exit
cd      "$root" || exit
echo pwd
pwd
echo ls
ls

echo ARG2 \(lvl\) = "$2"
if   [[ $2 = "" ]]; then
  echo exit ">>>" Error - Missing arg2 \("$2"\) = \(lvl\) ">>>" exit
  exit
elif [[ $2 = 1 || $2 = 2 || $2 = 3 || $2 = 4 ]]; then
  echo lvl = "$2"
  lvl=$2
else
  echo exit ">>>" Error - Invalid value, arg2 = "$2", lvl = "$lvl", check cmd line arg2 ">>>" exit
  exit
fi

echo dirs=\(cats   csvs   data   logs   pngs   text\)
dirs=(     "cats" "csvs" "data" "logs" "pngs" "text")

echo exts=\(csv   log   png   txt\)
exts=(     "csv" "log" "png" "txt")
echo "... Removing Files from root Dir = $root ..."

echo cleanRoot "$lvl" "${exts[@]}"
cleanRoot      "$lvl" "${exts[@]}"

echo exit ">>>"
exit

echo exts=\(cat   csv   dat   log   png   txt\)
exts=(     "cat" "csv" "dat" "log" "png" "txt")
echo "... Removing Files from SubDirs of $root with type cat csv dat log png txt ..."
for ext in "${exts[@]}"  ; do
  if   [[ $ext = "dat" ]]; then
    dir="$ext"a
    echo cleanSubDir "$dir" "$ext" "$lvl"
    cleanSubDir      "$dir" "$ext" "$lvl"
  elif [[ $ext = "std" ]]; then
    dir="$ext"o
    echo cleanSubDir "$dir" "$ext" "$lvl"
    cleanSubDir      "$dir" "$ext" "$lvl"
  elif [[ $ext = "txt" ]]; then
    dir="text"
    echo cleanSubDir "$dir" "$ext" "$lvl"
    cleanSubDir      "$dir" "$ext" "$lvl"
  else
    dir="$ext"s
    echo cleanSubDir "$dir" "$ext" "$lvl"
    cleanSubDir      "$dir" "$ext" "$lvl"
  fi
done

