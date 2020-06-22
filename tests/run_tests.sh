if [[ `pwd` =~ tests$ ]]; then
    cd ../
fi

BASE_URL=localhost:8080
SENSITIVE_URL=lsf.berea.edu
VERBOSE="--verbose "

FLAGS="${VERBOSE}--capture=no --disable-pytest-warnings --strict-markers --tb=short -rs"
UI_URLS="--verify-base-url --base-url $BASE_URL --sensitive-url $SENSITIVE_URL"

RED='\033[0;31m'
GREEN='\033[0;32m'
L_CYAN='\033[1;36m'
NC='\033[0m' # No Color

function header {
	echo -e "\n${GREEN}Running $1 tests${NC}, with args ($L_CYAN$FLAGS$NC)"
}

# ui
function ui {
	header smoke
	python -m pytest $FLAGS $UI_URLS tests/ui/smoke_test.py 
	header functional
	python -m pytest $FLAGS $UI_URLS tests/ui/functional_test.py
}

# no-ui
function no-ui {
	header unit
	python -m pytest $FLAGS -m unit

	header integration
	python -m pytest $FLAGS -m integration
}

case "$1" in
	"") ;&
	all)
		no-ui
		ui
		;;
	ui)
		ui
		;;
	fast)
		# in the future, we may need to remove the integration tests
		no-ui
		#header fast
		#python -m pytest $FLAGS -m fast
		;;
	no-ui)
		no-ui
		;;
esac
