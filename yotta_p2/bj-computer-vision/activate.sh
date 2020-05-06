function activate_venv() {
    # try to activate with conda
    conda activate yp2 || \
        # if it fails, try to activate a "regular .venv"
        #./.venv/bin/activate || \
        # if it fails: warn the user and exit
        ( echo ""; echo "ERROR: failed to activate virtual environment yp2! ask for advice on #dev "; return 1 )
}

activate_venv && (
    echo ""
    echo "************************************************************************************"
    echo "Successfuly activated the virtual environment; you are now using this python:"
    echo "$ which python3"
    echo "$(which python3)"
    echo "************************************************************************************"
    echo ""
)

export PYTHONPATH="$PYTHONPATH:$(pwd)"
