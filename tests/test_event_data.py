from vkbottle import OpenAppEvent, OpenLinkEvent, ShowSnackbarEvent


def test_event_data_export():
    some_str = "vkbottle"
    some_int = 1_054_204

    assert (
        ShowSnackbarEvent(text=some_str).json()
        == f'{{"type": "show_snackbar", "text": "{some_str}"}}'
    )

    assert OpenLinkEvent(link=some_str).json() == f'{{"type": "open_link", "link": "{some_str}"}}'

    assert (
        OpenAppEvent(app_id=some_int, hash=some_str).json()
        == f'{{"type": "open_app", "owner_id": null, "app_id": {some_int}, "hash": "{some_str}"}}'
    )
