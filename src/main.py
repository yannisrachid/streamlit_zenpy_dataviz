import sys
from streamlit import cli as stcli

if __name__ == '__main__':
    APP_FILE = 'app.py'
    sys.argv = ["streamlit", "run", APP_FILE]
    sys.exit(stcli.main())
