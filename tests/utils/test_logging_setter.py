import logging
import pathlib

from brain_computer_interface.utils import setup_logging


def test_different_records(caplog, capsys):
    file_only = 'file_only'
    also_screen = 'also_screen'
    also_syslog = 'also_syslog'
    all_of_them = 'all_of_them'
    msg_suffix = '_msg'
    file_only_logger = setup_logging(file_only, stream_to_syslog=False,
                                     stream_to_screen=False)
    also_screen_logger = setup_logging(also_screen, stream_to_syslog=False)
    also_syslog_logger = setup_logging(also_syslog, stream_to_screen=False)
    all_of_them_logger = setup_logging(all_of_them)
    file_only_logger.critical(file_only + msg_suffix)
    also_screen_logger.critical(also_screen + msg_suffix)
    also_syslog_logger.critical(also_syslog + msg_suffix)
    all_of_them_logger.critical(all_of_them + msg_suffix)
    # log records check
    records_msg = [record.message for record in caplog.records]
    for log in [file_only, also_screen, also_syslog, all_of_them]:
        assert any(log + msg_suffix in msg for msg in records_msg)
    # file check
    log_dir = pathlib.Path('logs')
    for log in [file_only, also_screen, also_syslog, all_of_them]:
        assert log + msg_suffix in (log_dir / f'{log}.log').read_text()
    # stdout check
    capture = capsys.readouterr().err
    assert 'file_only_msg' not in capture
    assert 'also_screen_msg' in capture
    assert 'also_syslog_msg' not in capture
    assert 'all_of_them_msg' in capture
    # syslog check
    # I need to handle more than one OS and it's annoying


def test_different_levels(caplog):
    info_logger = setup_logging('info', logging.INFO)
    should_see_this = 'my guy'
    info_logger.info(should_see_this)
    should_not_see_this = 'you guys'
    info_logger.debug(should_not_see_this)
    assert any(should_see_this in record.message for record in caplog.records)
    assert all(should_not_see_this not in record.message
               for record in caplog.records)
    # setting another logger to make sure it doesn't effect the first
    setup_logging('error', logging.ERROR)
    should_still_see_this = 'should_still_see_this'
    info_logger.info(should_still_see_this)
    assert any(should_still_see_this in record.message
               for record in caplog.records)
