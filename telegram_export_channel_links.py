#!/usr/bin/env python3

__prog__ = "telegram-export-channel-links"
__version__ = "0.0.1"
__desc__ = "Export public channel and group links of telegram account."

import argparse
import sys

from telethon.sync import TelegramClient
from telethon import utils
from telethon.tl.functions.channels import GetFullChannelRequest

def tohex(val, nbits):
  return hex((val + (1 << nbits)) % (1 << nbits))

def main():
    parser = argparse.ArgumentParser(
        prog=__prog__,
        description=__desc__,
    )
    parser.add_argument(
        "--app-id",
        type=int,
        default=17349,
        help="Test credentials are used by default",
    )
    parser.add_argument(
        "--app-hash",
        type=str,
        default="344583e45741c457fe1862106095a5eb",
        help="Test credentials are used by default",
    )
    args = parser.parse_args()

    with TelegramClient(__prog__, args.app_id, args.app_hash) as client:
        def write_dialog(dialog):
            try:
                print("=======")
                chat = client.get_entity(dialog.id)
                real_id, peer_type = utils.resolve_id(dialog.id)
                print(
                    "id: ", hex(dialog.id), sep=""
                )
                print(
                    "real_id: ", real_id, sep=""
                )

                #print(
                #        "is group: ", dialog.is_group, sep=""
                #    )
                #print(
                #        "is channel: ", dialog.is_channel, sep=""
                #    )
                #print(
                #        "is private: ", dialog.is_private, sep=""
                #    )

                title = utils.get_display_name(chat)
                print(
                        "title: ", title, sep=""
                    )

                username = chat.username
                if username:
                    print(
                        "link: https://t.me/", username, sep=""
                    )

                chatClient = client(GetFullChannelRequest(channel=chat))
                description = chatClient.full_chat.about
                if description:
                    print(
                        description
                    )

            except AttributeError:
                pass

            for dialog in client.iter_dialogs():
                if dialog.is_group or dialog.is_channel:
                    write_dialog(dialog)

if __name__ == "__main__":
    main()
