
## Installation

### Clone & Run Locally
Clone this repository, enter the `Sabre-Web` directory, then run:
```
> python -m venv venv  # must be python3.6+
> venv/bin/pip install -r requirements.txt
> venv/bin/python -m sabre-web
serving on http://127.0.0.1:5000
```

## API
```
> sabre-web --help
usage: sabre-web [-h] [-p PORT] [--host HOST] [--debug] [--version]
                 [--command COMMAND] [--cmd-args CMD_ARGS]

A fully functional SABRE-TOC in your browser.
https://github.com/aidden-laoch/sabre

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port to run server on (default: 5000)
  --host HOST           host to run server on (use 0.0.0.0 to allow access
                        from other hosts) (default: 127.0.0.1)
  --debug               debug the server (default: False)
  --version             print version and exit (default: False)
  --command COMMAND     Command to run in the terminal (default: bash)
  --cmd-args CMD_ARGS   arguments to pass to command (i.e. --cmd-args='arg1
                        arg2 --flag') (default: )

```
