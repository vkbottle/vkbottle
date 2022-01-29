from typing import TYPE_CHECKING, Any, Dict, Optional, Type

if TYPE_CHECKING:
    from .action import ABCAction
    from .color import KeyboardButtonColor


class KeyboardButton:
    def __init__(
        self,
        action: "ABCAction",
        color: Optional["KeyboardButtonColor"] = None,
        data: Optional[dict] = None,
    ):
        self.action = action
        self.color = color
        self.data = data

    @classmethod
    def from_typed(
        cls: Type["KeyboardButton"],
        action: "ABCAction",
        color: Optional["KeyboardButtonColor"] = None,
    ) -> "KeyboardButton":
        return cls(action, color, None)

    @classmethod
    def from_dict(cls: Type["KeyboardButton"], data: dict) -> "KeyboardButton":
        color = data.get("color")
        keyboard_data = {"action": data}
        if color is not None:
            keyboard_data["action"].pop("color")
            keyboard_data["color"] = color
        return cls(cls.action, cls.color, keyboard_data)  # type: ignore

    def get_data(self) -> dict:
        if self.data is not None:
            return self.data

        data: Dict[str, Any] = {"action": self.action.get_data()}
        if (
            self.action.type
            in (
                "text",
                "callback",
            )
            and self.color
        ):
            data["color"] = self.color.value
        return data
