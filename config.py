import sys
import os
import datetime

import pyauto
from keyhac import *


def configure(keymap):
    # --------------------------------------------------------------------
    # Text editer setting for editting config.py file

    # Setting with program file path (Simple usage)
    if 1:
        keymap.editor = "notepad++.exe"

    # Setting with callable object (Advanced usage)
    if 0:

        def editor(path):
            shellExecute(None, "notepad.exe", '"%s"' % path, "")

        keymap.editor = editor

    # --------------------------------------------------------------------
    # Customizing the display

    # Font
    keymap.setFont("MS Gothic", 12)

    # Theme
    keymap.setTheme("black")

    # --------------------------------------------------------------------

    # Simple key replacement
    # keymap.replaceKey( "LWin", 235 )
    # keymap.replaceKey( "RWin", 255 )
    # keymap.replaceKey( "(124)", 255 )

    # User modifier key definition
    F13 = 124
    keymap.defineModifier(F13, "User0")
    # カタカナひらがなキーをそのまま使うとキーが押されっぱなし状態になる。
    # レジストリ書き換えで別キー（F13）に割り当てておく。

    # Global keymap which affects any windows

    if 1:
        keymap_global = keymap.defineWindowKeymap()

        for modifier in ("", "S-", "C-", "A-", "C-S-", "C-A-", "S-A-", "C-A-S-"):
            # 上下左右
            keymap_global[modifier + "U0-H"] = modifier + "Left"
            keymap_global[modifier + "U0-J"] = modifier + "Down"
            keymap_global[modifier + "U0-K"] = modifier + "Up"
            keymap_global[modifier + "U0-L"] = modifier + "Right"
            # Home / End / PageUp / PageDown
            keymap_global[modifier + "U0-N"] = modifier + "Home"
            keymap_global[modifier + "U0-Period"] = modifier + "End"
            keymap_global[modifier + "U0-M"] = modifier + "PageDown"
            keymap_global[modifier + "U0-Comma"] = modifier + "PageUp"

        # U0モディファイアでの記号類入力
        u0_keys_dict = {
            # U0 上段
            "Q": "S-1",
            "W": "AtMark",
            "E": "S-3",
            "R": "S-4",
            "T": "S-5",
            "Y": "Caret",
            "U": "S-6",  # &
            "I": "S-Colon",  # *
            "O": "S-8",  # (
            "P": "S-9",  # )
            # U0 中段
            "A": "S-7",  # '
            "S": "S-2",  # "
            "D": "OpenBracket",  # [
            "F": "CloseBracket",  # ]
            "G": "S-AtMark",  # `
            "Semicolon": "Colon",  # `
            # U0 下段
            "Z": "Minus",  # -
            "X": "S-Minus",  # =
            "C": "S-OpenBracket",  # {
            "V": "S-CloseBracket",  # }
            "B": "S-Caret",  # ~
        }
        for k_in, k_out in u0_keys_dict.items():
            keymap_global["U0-" + k_in] = k_out

        # Clipboard history related
        keymap_global[
            "C-A-V"
        ] = keymap.command_ClipboardList  # Open the clipboard history list
        # keymap_global[ "C-S-X"   ] = keymap.command_ClipboardRotate   # Move the most recent history to tail
        # keymap_global[ "C-S-A-X" ] = keymap.command_ClipboardRemove   # Remove the most recent history
        keymap.quote_mark = "> "  # Mark for quote pasting

    # Customizing clipboard history list
    if 1:
        # Enable clipboard monitoring hook (Default:Enabled)
        keymap.clipboard_history.enableHook(True)

        # Maximum number of clipboard history (Default:1000)
        keymap.clipboard_history.maxnum = 1000

        # Total maximum size of clipboard history (Default:10MB)
        keymap.clipboard_history.quota = 10 * 1024 * 1024

        # Fixed phrases
        fixed_items = [
            ("name@server.net", "name@server.net"),
            ("Address", "San Francisco, CA 94128"),
            ("Phone number", "03-4567-8901"),
        ]

        # Return formatted date-time string
        def dateAndTime(fmt):
            def _dateAndTime():
                return datetime.datetime.now().strftime(fmt)

            return _dateAndTime

        # Date-time
        datetime_items = [
            ("YYYY/MM/DD HH:MM:SS", dateAndTime("%Y/%m/%d %H:%M:%S")),
            ("YYYY/MM/DD", dateAndTime("%Y/%m/%d")),
            ("HH:MM:SS", dateAndTime("%H:%M:%S")),
            ("YYYYMMDD_HHMMSS", dateAndTime("%Y%m%d_%H%M%S")),
            ("YYYYMMDD", dateAndTime("%Y%m%d")),
            ("HHMMSS", dateAndTime("%H%M%S")),
        ]

        # Add quote mark to current clipboard contents
        def quoteClipboardText():
            s = getClipboardText()
            lines = s.splitlines(True)
            s = ""
            for line in lines:
                s += keymap.quote_mark + line
            return s

        # Indent current clipboard contents
        def indentClipboardText():
            s = getClipboardText()
            lines = s.splitlines(True)
            s = ""
            for line in lines:
                if line.lstrip():
                    line = " " * 4 + line
                s += line
            return s

        # Unindent current clipboard contents
        def unindentClipboardText():
            s = getClipboardText()
            lines = s.splitlines(True)
            s = ""
            for line in lines:
                for i in range(4 + 1):
                    if i >= len(line):
                        break
                    if line[i] == "\t":
                        i += 1
                        break
                    if line[i] != " ":
                        break
                s += line[i:]
            return s

        full_width_chars = "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！”＃＄％＆’（）＊＋，−．／：；＜＝＞？＠［￥］＾＿‘｛｜｝～０１２３４５６７８９　"
        half_width_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}～0123456789 "

        # Convert to half-with characters
        def toHalfWidthClipboardText():
            s = getClipboardText()
            s = s.translate(str.maketrans(full_width_chars, half_width_chars))
            return s

        # Convert to full-with characters
        def toFullWidthClipboardText():
            s = getClipboardText()
            s = s.translate(str.maketrans(half_width_chars, full_width_chars))
            return s

        # Save the clipboard contents as a file in Desktop directory
        def command_SaveClipboardToDesktop():
            text = getClipboardText()
            if not text:
                return

            # Convert to utf-8 / CR-LF
            utf8_bom = b"\xEF\xBB\xBF"
            text = text.replace("\r\n", "\n")
            text = text.replace("\r", "\n")
            text = text.replace("\n", "\r\n")
            text = text.encode(encoding="utf-8")

            # Save in Desktop directory
            fullpath = os.path.join(
                getDesktopPath(),
                datetime.datetime.now().strftime("clip_%Y%m%d_%H%M%S.txt"),
            )
            fd = open(fullpath, "wb")
            fd.write(utf8_bom)
            fd.write(text)
            fd.close()

            # Open by the text editor
            keymap.editTextFile(fullpath)

        # Menu item list
        other_items = [
            ("Quote clipboard", quoteClipboardText),
            ("Indent clipboard", indentClipboardText),
            ("Unindent clipboard", unindentClipboardText),
            ("", None),
            ("To Half-Width", toHalfWidthClipboardText),
            ("To Full-Width", toFullWidthClipboardText),
            ("", None),
            ("Save clipboard to Desktop", command_SaveClipboardToDesktop),
            ("", None),
            ("Edit config.py", keymap.command_EditConfig),
            ("Reload config.py", keymap.command_ReloadConfig),
        ]

        # Clipboard history list extensions
        keymap.cblisters += [
            ("Fixed phrase", cblister_FixedPhrase(fixed_items)),
            ("Date-time", cblister_FixedPhrase(datetime_items)),
            ("Others", cblister_FixedPhrase(other_items)),
        ]
