from pytest_response import response


def pytest_addoption(parser):
    """
    Pytest hook for adding cmd-line options.
    """
    parser.addoption(
        "--remote",
        dest="remote",
        action="store_true",
        default=False,
        help="Allow outgoing connections requests.",
    )
    parser.addoption(
        "--remote-capture",
        dest="remote_capture",
        action="store_true",
        default=False,
        help="Capture connections requests.",
    )
    parser.addoption(
        "--remote-response",
        dest="remote_response",
        action="store_true",
        default=False,
        help="Mock connections requests.",
    )


def pytest_configure(config):
    """
    Pytest hook for setting up monkeypatch, if ``--intercept-remote`` is ``True``
    """
    if not config.option.remote and config.option.verbose:
        print(f"Remote: {config.option.remote}")

    if config.option.remote_capture and config.option.remote_response:
        assert not config.option.remote_capture and config.option.remote_response  # either capture or mock_remote

    response.setup_database("basedata.json")
    response.register("urllib_quick")
    response.register("requests_quick")

    response.configure(
        remote=config.option.remote,
        capture=config.option.remote_capture,
        response=config.option.remote_response,
    )

    response.applyall()


# def pytest_runtest_setup(item):


# def pytest_runtest_teardown(item):


def pytest_unconfigure(config):
    """
    Pytest hook for cleaning up.
    """
    response.unapplyall()
    response.unregister()
