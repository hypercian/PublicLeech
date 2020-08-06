#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
LOGGER = logging.getLogger(__name__)

import os
import time
from pyrogram import CallbackQuery
from tobrot import (
    DOWNLOAD_LOCATION
)
from tobrot.helper_funcs.extract_link_from_message import extract_link
from tobrot.helper_funcs.youtube_dl_button import youtube_dl_call_back
from tobrot.helper_funcs.download_aria_p_n import (
    call_apropriate_function,
    aria_start,
    fake_etairporpa_call
)
from tobrot.helper_funcs.download_from_link import request_download
from tobrot.helper_funcs.display_progress import progress_for_pyrogram
from tobrot.helper_funcs.youtube_dl_extractor import extract_youtube_dl_formats


async def button(bot, update: CallbackQuery):
    if update.from_user.id != update.message.reply_to_message.from_user.id:
        await update.answer(
            text="who are you? 🤪🤔🤔🤔",
            show_alert=True,
            cache_time=0
        )
        return

    await update.answer()
    LOGGER.info(update)
    cb_data = update.data

    if cb_data.startswith("leech"):
        # get link from the incoming message
        dl_url, cf_name, _, _ = await extract_link(update.message.reply_to_message, "LEECH")
        LOGGER.info(dl_url)
        LOGGER.info(cf_name)
        if dl_url is not None:
            await update.message.edit_text("extracting links")
            # start the aria2c daemon
            aria_i_p = await aria_start()
            LOGGER.info(aria_i_p)
            if "_" in cb_data:
                current_user_id = update.from_user.id
                # create an unique directory
                new_download_location = os.path.join(
                    DOWNLOAD_LOCATION,
                    str(current_user_id),
                    str(time.time())
                )
                # create download directory, if not exist
                if not os.path.isdir(new_download_location):
                    os.makedirs(new_download_location)
                await update.message.edit_text("trying to download")
                # try to download the "link"
                sagtus, err_message = await fake_etairporpa_call(
                    aria_i_p,
                    dl_url,
                    new_download_location,
                    update.message,
                    int(cb_data.split("_")[2])
                    # maybe IndexError / ValueError might occur,
                    # we don't know, yet!!
                )
                if not sagtus:
                    # if FAILED, display the error message
                    await update.message.edit_text(err_message)
            else:
                is_zip = False
                if "a" in cb_data:
                    is_zip = True
                current_user_id = update.from_user.id
                # create an unique directory
                new_download_location = os.path.join(
                    DOWNLOAD_LOCATION,
                    str(current_user_id),
                    str(time.time())
                )
                # create download directory, if not exist
                if not os.path.isdir(new_download_location):
                    os.makedirs(new_download_location)
                await update.message.edit_text("trying to download")
                # try to download the "link"
                sagtus, err_message = await call_apropriate_function(
                    aria_i_p,
                    dl_url,
                    new_download_location,
                    update.message,
                    is_zip
                )
                if not sagtus:
                    # if FAILED, display the error message
                    await update.message.edit_text(err_message)
            
    elif "|" in cb_data:
        await youtube_dl_call_back(bot, update)
