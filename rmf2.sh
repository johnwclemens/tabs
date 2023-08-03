#bash
#C:\Users\Owner\Documents\GitHub\tabs\venv\Scripts\

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
#                ls "$file"
                rm "$file"
            fi
        elif [[ $lvl = 2 ]]; then
            if [[ $file = *.*.$ext ]]; then
                echo rm "$file" ">>>" lvl = "$lvl"
#                ls "$file"
                rm "$file"
            fi
        elif [[ $lvl = 3 ]]; then
            if [[ $file = *.$ext ]]; then
                echo rm "$file" ">>>" lvl = "$lvl"
#                ls "$file"
                rm "$file"
            fi
        elif [[ $lvl = 4 ]]; then
            echo rm "$file" ">>>" lvl = "$lvl"
#            ls "$file"
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

echo arg1 = "$1"
if   [[ $1 = "" ]]; then
    root="/c/Users/Owner/Documents/GitHub/Tabs/test"
else
    root="$1"
fi
echo root = "$root"

echo arg2 = "$2"
if   [[ $2 = "" ]]; then
    lvl=1
elif [[ $2 = 1 || $2 = 2 || $2 = 3 || $2 = 4 ]]; then
    lvl=$2
else
    echo exit ">>>" ERROR: lvl = "$lvl" is invalid, check cmd line arg2
    exit
fi
echo lvl = "$lvl"

if [[ -d "$root" ]]; then
    cd  "$root" || exit 1

    echo exts=\( csv    dat    log    png    txt\)
    exts=(     ".csv" ".dat" ".log" ".png" ".txt")

    echo "... Removing Files from root dir $root ..."
    for ext in "${exts[@]}"; do
        fileHits=()
        while IFS= read -r -d $'\0'; do
            fileHits+=("$REPLY")
        done < <(find . -maxdepth 1 -type f -name "*$ext" -print0)

        if [[ ${#fileHits[@]} -gt 0 ]]; then
            for file in "${fileHits[@]}"; do
                if [[ $ext = ".dat" ]]; then
                    if [[ $lvl = 4 ]]; then
#                        echo "$ext = ext, $lvl = lvl (A)"
#                        ls "$file"
                        rm "$file"
                    fi
                elif [[ $lvl = 3 || $lvl = 4 ]]; then
#                    echo "$ext = ext, $lvl = lvl (B)"
#                    ls "$file"
                    rm "$file"
                fi
            done
        else
            echo "There are no files with ext '$ext' in the root dir '$root'"
        fi
    done

    echo "... Removing files from sub dirs of root dir $root ..."
    for ext in "${exts[@]}"; do
        ext="${ext:1}"
        if   [[ $ext = "dat" ]]; then
            dir="$ext"a
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
else
    echo "ERROR: root = '$root' directory does not exist."
fi
