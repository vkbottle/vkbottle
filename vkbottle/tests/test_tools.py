from vkbottle import OpenAppEvent, OpenLinkEvent, ShowSnackbarEvent


def test_event_data_constructor():
    show_snackbar = ShowSnackbarEvent(text="test").dict()
    assert show_snackbar.get("type") == "show_snackbar"
    assert show_snackbar.get("text") == "test"

    open_link = OpenLinkEvent(link="test").dict()
    assert open_link.get("type") == "open_link"
    assert open_link.get("link") == "test"

    open_app = OpenAppEvent(app_id=1, hash="test").dict()
    assert open_app.get("app_id") == 1
    assert open_app.get("hash") == "test"
