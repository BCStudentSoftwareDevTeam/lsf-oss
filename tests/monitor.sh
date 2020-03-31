if [[ `pwd` =~ tests$ ]]; then
    cd ../
fi

ptw --verbose -c --runner "sh tests/run_tests.sh" --ext=".py,.sh"
