#!/bin/bash

THISDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PRJDIR="$THISDIR/src"
ENV="venv"

set -e
set -u

function build_help() {
cat <<ENDHELP
       build [cmd]

       Build commands for "$THISDIR"

           build:               Build the python
           citest:              Run unit tests
           default:             Same as restore, build, citest, report
           install:             Prints instructions for turning on completion
           pack:                Create packages
           publish:             Publish packages
           coverage:            Generate coverage report
           profile:             Gemerate profile report
           restore:             Update dependencies in environment $ENV
           setup:               Install prerequisites
           test:                Create packages and run integration tests
           test_nopack:         Run integration tests without creating packages
           regress:             Run regression tests
           regress_nopack:      Run regression tests without creating packages
        After clone, run setup
        After checkout or pull run restore
        Before commit run default

ENDHELP
}

function build_build() {
    python -m mypy "$PRJDIR" --config-file "$THISDIR/mypy.ini"
    (
        cd "$THISDIR"
        flake8 "$PRJDIR" --ignore=W504 && echo "Passed Flake8"
    )
}

# function build_profile() {
#     python -m cProfile -o risk.prof "$PRJDIR/risk.py"
#     snakeviz risk.prof
# }

function build_citest() {
     coverage run --branch --source="$PRJDIR" -m pytest --pyargs "$PRJDIR" "$PRJDIR"
}

function build_restore() {
    if ! which python | grep -w "$ENV" > /dev/null ; then
        python3 -m venv "$ENV"
    fi
    source "$ENV/bin/activate"
    pip install -r requirements.txt
}


function run_cmd() {
    local script=$1
    shift
    printf '==== %-10s    ====\n' "$script"
    "build_$script" "$@"
}

function build_default() {
    run_cmd setup
    run_cmd restore
    run_cmd build
    run_cmd citest
    run_cmd report
}

function build_setup() {
    command virtualenv --version > /dev/null || { echo "Missing virtualenv - you need to install it." ; exit 1 ; }
    command pip --version > /dev/null || { echo "Missing pip - you need to install it." ; exit 2 ; }
}

# function build_pack() {
#     #work out how to use the inbuild ppi
#     :
# }

# function build_publish() {
#     #pass
#     :
# }

function build_report() {
    coverage report --fail-under 75 --omit='./venv/*'
    coverage html --fail-under 75 --omit='./venv/*'
}

# function build_docs() {
#   :
# }

cmd="${1:-default}"
shift || true
"build_$cmd" "$@"
