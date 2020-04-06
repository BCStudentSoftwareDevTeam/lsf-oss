if [[ `pwd` =~ tests$ ]]; then
    cd ../
fi

export VERIFY_BASE_URL=true
export PYTEST_BASE_URL=http://localhost:8080
python -m pytest --verbose --capture=no --disable-pytest-warnings tests/smoke_test.py
