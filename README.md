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
