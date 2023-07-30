#!/usr/bin/env python3

import logging
from pathlib import Path
from os import environ
from traceback import format_exc
from logging.handlers import SysLogHandler
from sys import exit as sys_exit
from sys import argv as sys_argv
from json import loads as json_loads
from json import dumps as json_dumps
from subprocess import Popen as subprocess_popen
from subprocess import PIPE as subprocess_pipe

DEBUG = True
OVPN_SERVER = 'test'
TIMEOUT_SEC = 5
AUTH_CONFIG_FILE = 'auth.json'

SYSLOG = True
SYSLOG_IDENTIFIER = 'openvpn_auth_test'
LOG_FILE = '/var/log/openvpn/openvpn_test_auth.log'
SERVER_PLACEHOLDER = '$server_name'

if len(sys_argv) == 1:
    print('ERROR: MISSING ARGUMENT 1 - CREDENTIAL FILE')
    sys_exit(1)

CREDENTIAL_FILE = sys_argv[1]
CWD = Path(__file__).parent
AUTH_CONFIG_FILE_PATH = f'{CWD}/{AUTH_CONFIG_FILE}'
LOG_FILE = LOG_FILE.replace(SERVER_PLACEHOLDER, OVPN_SERVER)
SYSLOG_IDENTIFIER = SYSLOG_IDENTIFIER.replace(SERVER_PLACEHOLDER, OVPN_SERVER)

if SYSLOG:
    # syslog logging
    syslog_handler = SysLogHandler(address='/dev/log')
    syslog_handler.ident = SYSLOG_IDENTIFIER
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(syslog_handler)

else:
    class Logger:
        @staticmethod
        def log(msg: str, prefix: str):
            with open(LOG_FILE, 'a', encoding='utf-8') as file:
                file.write(f"{prefix} | {msg}\n")

        @classmethod
        def critical(cls, msg: str):
            cls.log(prefix='CRIT', msg=msg)

        @classmethod
        def warning(cls, msg: str):
            cls.log(prefix='WARN', msg=msg)

        @classmethod
        def debug(cls, msg: str):
            cls.log(prefix='DEBUG', msg=msg)


    logger = Logger()


def log(msg: str, level=3):
    msg = f': {msg}'

    if level == 1:
        logger.critical(msg)

    elif level == 2:
        logger.warning(msg)

    elif DEBUG:
        logger.debug(msg)


def _authentication_script(cmd: list) -> bool:
    with subprocess_popen(
        cmd,
        shell=True,
        stdout=subprocess_pipe,
        stderr=subprocess_pipe
    ) as process:
        auth_error = process.communicate(timeout=TIMEOUT_SEC)[1].decode('utf-8')
        exit_code = process.returncode

    if exit_code != 0 and auth_error not in [None, '', ' ']:
        log(f"Authentication failed with message: '{auth_error}'")

    return exit_code == 0


# pylint: disable=W0718
try:
    log('Processing authentication')
    environ['OVPN_SERVER'] = OVPN_SERVER
    environ['OVPN_CREDENTIAL_FILE'] = CREDENTIAL_FILE

    if not Path(AUTH_CONFIG_FILE_PATH).is_file():
        log(f"Unable to load config from file: '{AUTH_CONFIG_FILE_PATH}'", level=1)
        sys_exit(1)

    log(f"Loading authentication config from file: '{AUTH_CONFIG_FILE_PATH}'")
    AUTH_CONFIG = json_loads(AUTH_CONFIG_FILE_PATH)

    results = []

    for provider_name, provider_config in AUTH_CONFIG.items():
        log(f"Processing authentication provider '{provider_name}'")
        environ['OVPN_AUTH_PROVIDER'] = provider_name
        environ['OVPN_AUTH_CONFIG'] = json_dumps(provider_config)

        provider_result = _authentication_script(provider_config['cmd'])

        if not provider_result:
            log(f"Authentication using provider '{provider_name}' failed!", level=2)

        results.append(provider_result)

    log(f'Finished authentication - results: {results}')

    if len(results) > 0 and all(results):
        sys_exit(0)

except Exception as error:
    traceback = ' | '.join(str(format_exc()).split('\n'))
    log(f"Unexpected authentication error: '{error}' => '{traceback}'", level=1)

sys_exit(1)
