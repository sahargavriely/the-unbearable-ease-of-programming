import pathlib

from brain_computer_interface.utils import setup_logging


def test_setup_logging(caplog, capsys):
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
