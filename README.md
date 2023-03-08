pydoc-quarto
================

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

## Install

``` sh
pip install pydoc_quarto
```

## Usage

``` python
!pydoc_quarto -h
```

    usage: pydoc_quarto [-h] lib dest_dir

    Generate Markdown API docs

    positional arguments:
      lib         the name of the python library
      dest_dir    the destination directory the markdown files will be rendered into

    options:
      -h, --help  show this help message and exit

## Example

This will generate markdown files for the `requests` library:

``` python
!pydoc_quarto requests _test_dir/
!ls _test_dir/
```

    requests.adapters.qmd     requests.cookies.qmd      requests.packages.qmd
    requests.api.qmd          requests.exceptions.qmd   requests.sessions.qmd
    requests.auth.qmd         requests.help.qmd         requests.status_codes.qmd
    requests.certs.qmd        requests.hooks.qmd        requests.structures.qmd
    requests.compat.qmd       requests.models.qmd       requests.utils.qmd
