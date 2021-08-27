from vkbottle import ShowSnackbar, OpenLink, OpenApp


def test_event_data_constructor():
    show_snackbar = ShowSnackbar(text="test").get_data()
    assert show_snackbar.get("type") == "show_snackbar"
    assert show_snackbar.get("text") == "test"

    open_link = OpenLink(link="test").get_data()
    assert open_link.get("type") == "open_link"
    assert open_link.get("link") == "test"

    open_app = OpenApp(app_id=1, hash="test").get_data()
    assert open_app.get("app_id") == 1
    assert open_app.get("hash") == "test"
    assert "owner_id" not in open_app
