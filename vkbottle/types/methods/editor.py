import os
import re

for file_name in os.listdir("."):
    if not file_name.startswith("__") and file_name not in ["editor.py", "access.py"]:
        with open(file_name, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "for k, v in locals().items()" in line:
                    line = line.replace(
                        "for k, v in locals().items()",
                        "for k, v in {**locals(), **self.kwargs}.items()",
                    )
                    lines[i] = line
            with open(file_name, "w") as fw:
                fw.writelines(lines)
