import sys
import warnings

warnings.warn(
    "Imports from vkbottle.tools.dev is deprecated, use vkbottle.tools instead",
    FutureWarning,
    stacklevel=0,
)

sys.modules["vkbottle.tools.dev"] = sys.modules["vkbottle.tools"]
