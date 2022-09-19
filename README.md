# python-accounts

Import CSV statements into a database for analysis

## Usage
```
Usage: load [OPTIONS]

Options:
  -c, --config FILE   Read option defaults from the specified INI file
                      [default: config/default.ini]
  -f, --file FILE
  -i, --in-dir PATH   Input directory  [required]
  -o, --out-dir PATH  Directory for processed files  [required]
  -d, --db-path FILE  Path to sqlite DB file  [required]
  --help              Show this message and exit.
```

## Development
```
pyenv local 3.10.7
poetry install
poetry run load [OPTIONS]
```

### Run tests
```
poetry run pytest
```