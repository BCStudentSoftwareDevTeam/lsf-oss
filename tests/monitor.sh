if [[ `pwd` =~ tests$ ]]; then
    cd ../
fi

ptw --verbose -c --runner "bash tests/run_tests.sh $@" --ext=".py,.sh"
