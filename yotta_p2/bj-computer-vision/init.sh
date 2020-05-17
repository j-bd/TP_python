# exit on error
set -e

    # try to create a .venv with conda
conda create -n yp2 python=3.7  || \
    # if it fails, try using python
    python -m venv .venv  || \
    # if it fails: warn the user (clean the .venv if it was partially created)
    (rm -rf .venv && echo "ERROR: failed to create the .venv : do it yourself!" && exit 1);


echo "*********************************************************"
echo "Successfully created the virtual environment! it is located at:"
echo "$(pwd)/.venv"
echo "In order to activate this venv:"
echo "$ source activate.sh"
echo "*********************************************************"
echo ""
