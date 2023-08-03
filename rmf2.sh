#bash
#C:\Users\Owner\Documents\GitHub\tabs\venv\Scripts\

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
    echo "... Removing Files from root Dir = $root ..."

    for ext in "${exts[@]}"; do
        fileHits=()
        while IFS= read -r -d $'\0'; do
            fileHits+=("$REPLY")
        done < <(find . -maxdepth 1 -type f -name "*$ext" -print0)

        if [[ ${#fileHits[@]} -gt 0 ]]; then
            for file in "${fileHits[@]}"; do
                if [[ $ext = ".dat" ]]; then
                    if [[ $lvl = 4 ]]; then
                        echo "$ext = ext, $lvl = lvl (A)"
                        ls "$file"
#                        rm "$file"
                    fi
                elif [[ $lvl = 3 || $lvl = 4 ]]; then
                    echo "$ext = ext, $lvl = lvl (B)"
                    ls "$file"
#                    rm "$file"
                fi
            done
        else
            echo "There are no files with ext '$ext' in the root dir '$root'"
        fi
    done
else
    echo "ERROR: root = '$root' directory does not exist."
fi
