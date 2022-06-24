import pytest
from pytest import MonkeyPatch
from npkn import utils
from npkn.constants import RUNTIMES
import logging


def test_log_error_and_exit_with_string(caplog):
    caplog.set_level(logging.ERROR)
    test_err_message = "test error"

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        utils.log_error_and_exit(test_err_message)

    assert test_err_message in caplog.text
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_log_error_and_exit_with_base_exception(caplog):
    caplog.set_level(logging.ERROR)
    test_err_message = "test error"

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        utils.log_error_and_exit(BaseException(test_err_message))

    assert test_err_message in caplog.text
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def _add(a, b, c=0):
    return a + b + c


def test_run_with_loading_message(capsys):
    sample_message = "Adding"
    res = utils.run_with_loading_message(_add, sample_message, args=[1, 2])
    sysouterr = capsys.readouterr()

    assert res == 3
    assert not sysouterr.err
    assert sysouterr.out == 'Adding ⌛\rAdding ✅\n'


def test_run_with_loading_message_with_kwargs(capsys):
    sample_message = "Adding"
    res = utils.run_with_loading_message(_add, sample_message, args=[1, 2], kwargs={'c': 3})
    sysouterr = capsys.readouterr()

    assert res == 6
    assert not sysouterr.err
    assert sysouterr.out == 'Adding ⌛\rAdding ✅\n'


def test_load_config_no_envs(caplog):
    with MonkeyPatch.context() as mp:
        mp.delenv("NPKN_ACCOUNT_ID")
        mp.delenv("NPKN_SECRET_KEY")
        mp.delenv("NPKN_DEFAULT_RUNTIME")
        mp.delenv("NPKN_API_HOST")

        with caplog.at_level(logging.DEBUG):
            config = utils.load_config()
            assert len(caplog.records) == 2
            assert caplog.records[0].levelno == logging.DEBUG
            assert caplog.records[0].message == "No default runtime set"
            assert caplog.records[1].levelno == logging.INFO
            assert caplog.records[1].message == "Credentials not set"

        assert config['account_id'] is None
        assert config['secret_key'] is None
        assert config['default_runtime'] is None
        assert config['api_host'] == "https://api.napkin.io"


def test_load_config_all_envs(caplog):
    with MonkeyPatch.context() as mp:
        mp.setenv("NPKN_ACCOUNT_ID", "abcde12345")
        mp.setenv("NPKN_SECRET_KEY", "password")
        mp.setenv("NPKN_DEFAULT_RUNTIME", "python3.8")
        mp.setenv("NPKN_API_HOST", "http://localhost")

        config = utils.load_config()

        assert config['account_id'] == "abcde12345"
        assert config['secret_key'] == "password"
        assert config['default_runtime'] == "python3.8"
        assert config['api_host'] == "http://localhost"


def test_load_config_invalid_default_runtime(caplog):
    with MonkeyPatch.context() as mp:
        mp.delenv("NPKN_ACCOUNT_ID")
        mp.delenv("NPKN_SECRET_KEY")
        mp.setenv("NPKN_DEFAULT_RUNTIME", "BASIC")
        mp.delenv("NPKN_API_HOST")

        with caplog.at_level(logging.DEBUG):
            config = utils.load_config()
            assert len(caplog.records) == 2
            assert caplog.records[0].levelno == logging.ERROR
            assert caplog.records[0].message == f"Invalid default runtime value set: BASIC. Must be one of: {RUNTIMES}"
            assert caplog.records[1].levelno == logging.INFO
            assert caplog.records[1].message == "Credentials not set"

        assert config['account_id'] is None
        assert config['secret_key'] is None
        assert config['default_runtime'] is None
        assert config['api_host'] == "https://api.napkin.io"


