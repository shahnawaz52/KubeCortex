from app.tools.pod_logs import _decode_logs


def test_decode_logs_decodes_bytes() -> None:
    assert _decode_logs(b"Error: connection refused to database\n") == (
        "Error: connection refused to database\n"
    )


def test_decode_logs_handles_strings_and_none() -> None:
    assert _decode_logs("plain log") == "plain log"
    assert _decode_logs(None) == ""
