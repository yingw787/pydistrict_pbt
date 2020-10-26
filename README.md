# `pydistrict_pbt`: Code samples to go along with PyDistrict presentation on property-based testing

## Getting Started

1.  Clone the repository:

    ```bash
    git clone git@github.com:yingw787/pydistrict_pbt.git
    cd pydistrict_pbt
    ```

2.  Ensure that system dependencies are installed and the correct version:

    ```bash
    make check
    ```

3.  Start the container:

    ```bash
    make docker-bash
    ```

Additionally, the following commands are available:

- `update-deps`: Update Python-specific app/test/tooling dependencies using
  `pip-compile`.

## Running source code

### Running password validator

1.  Run:

    ```bash
    make docker-run "python /app/examples/password_validation.py '$PASSWORD'"
    ```

    Where `$PASSWORD` is some password, like `aBcD1234@`. You should see `False`
    or `True` printed to the console.

### Running web server

1.  Run:

    ```bash
    make docker-web-server
    ```

    This should create a running Flask application that accepts URL parameters
    and writes them to a database `web_server.sqlite3`. To call the API
    endpoint, run in a separate terminal:

    ```bash
    curl 'localhost:5000/init'
    curl 'localhost:5000/test?name=Ted&age=25'
    ```

    Both valid + invalid inputs should return a JSON response, with a status
    code and either an error message or some amount of data.

### Running data pipeline

1.  Run:

    ```bash
    make docker-data-pipeline
    ```

    This should create a never-ending process that creates log file
    `${GIT_REPO_ROOT}/examples/data_pipeline.txt`, and print out log messages to
    both stdout and the log file.

    Note that while for each device, log messages are ordered, log messages for
    the total body of stdout / file are out-of-order. This is accomplished by
    adding `time.sleep(random.random())` in the `Formatter` class, where source
    code has access to the point where `logging` generates the timestamp, but
    does not release it. This is to simulate clock jitter / skew and / or
    network latency and other forms of delays.

## Running tests
