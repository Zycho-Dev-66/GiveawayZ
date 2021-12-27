#!/usr/bin/env python

from re import A, I, U
from telegram.utils import helpers
import logging
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    Filters,
    CallbackContext,
    MessageHandler,
)
import os
from time import sleep, strftime
from datetime import datetime
from pymongo import MongoClient
from config import (
    ABOUT,
    TOKEN,
    GROUP,
    GROUP2,
    GROUP3,
    USERNAME,
    USERNAME2,
    USERNAME3,
    TEAM,
    IMAGE,
    OWNER,
    ACC_LIST,
    POINT_LIST,
    PROOFS_ID,
    PROOFS_USERNAME,
    HOWTO_HEADER,
    HOWTO_CONTEXT,
    HOWTO_FOOTER,
    MONGODB
)

q_panel = 0
target = 0
starttime = datetime.now()

# Enable logging
logging.basicConfig(
    format='[ACCBOT] %(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


def start(update: Update, context: CallbackContext) -> None:
    global userdb
    payload = context.args
    username = str(update.message.from_user.username)
    item = ""
    bot = context.bot
    url = helpers.create_deep_linked_url(bot.username, username)
    share = f"https://t.me/share/url?url={url}"
    for i in payload:
        item = str(i)
    if item != "":
        if item == username:
            update.message.reply_text("""
*❌ You can't click on your own link ❌*\n""".format(item),
                                      reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="🔗 Share 🔗", url=share)]]), parse_mode='Markdown')
        else:

            invite = userdb.find_one({"username": f'{item}'})

            balance = invite["wallet"] + 1
            reflistvar = invite["reflist"]
            status = invite["status"]
            ref_val = reflistvar.count(username)

            if status == "banned":
                update.message.reply_photo(
                    photo=IMAGE, caption=f'*❌ Hey @{username}, You are banned from our community!\n\nAsk an admin to unban you..*', parse_mode='Markdown')
            else:
                if ref_val > 0:
                    update.message.reply_photo(photo=IMAGE, caption="*❌ One refferal link can be used only once by a user!*",
                                               reply_markup=InlineKeyboardMarkup(
                                                   [[InlineKeyboardButton(text="💰 Earn 💰", callback_data='Earn')]]), parse_mode='Markdown')

                else:
                    reflistvar.append(username)

                    userdb.update_one({"username": f'{item}'}, {
                        "$set": {"wallet": balance}})
                    userdb.update_one({"username": f'{item}'}, {
                        "$set": {"reflist": reflistvar}})

                    update.message.reply_photo(photo=IMAGE, caption="*🔥 Hi! @{} welcome to the {} Premium Acc Giveaways..\n\nYou were invited by @{}*".format(username, TEAM, item),
                                               reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="💰 Earn 💰", callback_data='Earn')]]), parse_mode='Markdown')

    else:
        update.message.reply_photo(photo=IMAGE, caption=f"""
*🔥Welcome to the {TEAM} Premium Acc Generator Bot!*\n
You were not invited!

*🔥Earn points and withdraw premium accounts!*""",
                                   reply_markup=InlineKeyboardMarkup(
                                       [[InlineKeyboardButton(text="💰 Earn 💰", callback_data='Earn')]]), parse_mode='Markdown')


def query_handler(update: Update, context: CallbackContext) -> None:
    global userdb
    global user
    global starttime
    query = update.callback_query
    query.answer()
    bot = context.bot
    userid = query.from_user.id
    username = query.from_user.username
    if query.data == "Earn":
        query.edit_message_caption("""
*💡 You must join all our channels to use this bot..\n
Join and press [♻ VERIFY ♻]*
""", parse_mode='Markdown',
                                   reply_markup=InlineKeyboardMarkup(
                                       [
                                           [InlineKeyboardButton(
                                               text=f"📌 {GROUP} 📌", url=f'http://t.me/{USERNAME}')],
                                           [InlineKeyboardButton(
                                               text=f"📌 {GROUP2} 📌", url=f'http://t.me/{USERNAME2}')],
                                           [InlineKeyboardButton(
                                               text=f"📌 {GROUP3} 📌", url=f'http://t.me/{USERNAME3}')],
                                           [InlineKeyboardButton(
                                               text="♻ VERIFY ♻", callback_data='Verify')],
                                       ]
                                   ))
    if query.data == "Verify":
        query.edit_message_caption(
            "*♻ Verifying..*", parse_mode='Markdown')
        sleep(1)
        try:
            query.edit_message_caption(
                f"♻ Retrieving user lists..", parse_mode='Markdown')
            os.system('python client.py')
            from database import users as db
            query.edit_message_caption(
                f"*♻ Verifying user..*\nUser id :{userid}", parse_mode='Markdown')
            valid = 'N'
            for id in db:
                if id == userid:
                    valid = 'Y'
            if valid == "Y":
                query.edit_message_caption(
                    f"*💡 User verified..*\n\nID :{userid}", parse_mode='Markdown')

                query.delete_message()

                bot.send_message(userid, f'*🔥 Welcome to the {TEAM} Premium Accounts Giveaway bot*\n\n*Select from the Menu*', parse_mode='Markdown',
                                 reply_markup=ReplyKeyboardMarkup([
                                     [KeyboardButton(
                                         '🚀 Refferal 🚀')],
                                     [KeyboardButton('💰 Balance 💰')],
                                     [KeyboardButton(
                                         '💳 Withdraw Accounts 💳')],
                                     [KeyboardButton('🔩 Point Limits 🔩'), KeyboardButton(
                                         '🍻 Proofs 🍻')],
                                     [KeyboardButton('🔥 About us 🔥'), KeyboardButton(
                                         '🔔 Contact 🔔')],
                                     [KeyboardButton(
                                         '💡 How To Use 💡')],
                                     [KeyboardButton(
                                         '🗽 Premium 🗽')],
                                 ]))
            else:
                query.edit_message_caption(
                    f"*❌ Please Join all the chats..*", parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(
                                text=f"📌 {GROUP} 📌", url=f'http://t.me/{USERNAME}')],
                            [InlineKeyboardButton(
                                text=f"📌 {GROUP2} 📌", url=f'http://t.me/{USERNAME2}')],
                            [InlineKeyboardButton(
                                text=f"📌 {GROUP3} 📌", url=f'http://t.me/{USERNAME3}')],
                            [InlineKeyboardButton(
                                text="♻ VERIFY ♻", callback_data='Verify')],
                        ]
                    ))

        except Exception as e:
            query.edit_message_caption(
                "*❌ System Error!*\nYou may pass..", parse_mode='Markdown')
            query.delete_message()
            print(e)
            bot.send_message(userid, f'*🔥 Welcome to the {TEAM} Premium Accounts Giveaway bot*\n\n*Select from the Menu*', parse_mode='Markdown',
                             reply_markup=ReplyKeyboardMarkup([
                                 [KeyboardButton(
                                     '🚀 Refferal 🚀')],
                                 [KeyboardButton('💰 Balance 💰')],
                                 [KeyboardButton(
                                     '💳 Withdraw Accounts 💳')],
                                 [KeyboardButton('🔩 Point Limits 🔩'), KeyboardButton(
                                     '🍻 Proofs 🍻')],
                                 [KeyboardButton('🔥 About us 🔥'), KeyboardButton(
                                     '🔔 Contact 🔔')],
                                 [KeyboardButton(
                                     '💡 How To Use 💡')],
                                 [KeyboardButton(
                                     '🗽 Premium 🗽')],
                             ]))

    if query.data == "register":
        query.edit_message_text(
            "🔥 *Initialized Registration..*", parse_mode='Markdown')
        new_user = {
            "username": f"{query.from_user.username}",
            "wallet": 0,
            "reflist": [],
            "status": "user",
            "withdrawals": []
        }
        query.edit_message_text(
            "🔥 *Uploading Registration Details..*", parse_mode='Markdown')
        sleep(0.5)
        register = userdb.insert_one(new_user)
        query.edit_message_text(
            "🔥 *Registered successfully!*\n\nRegistration ID :{}".format(register.inserted_id), parse_mode='Markdown')
        sleep(0.5)
        query.edit_message_text(
            "🔥 *Now send [🚀 Refferal 🚀] once again to obtain your refferal link and view details*", parse_mode='Markdown')

    if query.data == '0':
        username = query.from_user.username
        index = int(query.data)
        try:
            pointslimit = POINT_LIST[index]
            account = ACC_LIST[index]
            userinfo = userdb.find_one({"username": f"{username}"})
            withdrawals = userinfo["withdrawals"]
            wallet = int(userinfo["wallet"])
            if wallet > pointslimit:
                try:
                    r_wallet = wallet - pointslimit
                    withdrawals.append(account)
                    bot.send_message(
                        PROOFS_ID, f'*withdrawals🔥🔥🔥 Withdrawal Request 🔥🔥🔥\n\n🔥 Status : Approved\n🔥 From : @{username}\n🔥 Account : {account}\n🔥 Date : {datetime.now().strftime("%x")}\n\n🔥 Powered by @{OWNER}\n\n🔥🔥🔥 Request Listed 🔥🔥🔥*', parse_mode='Markdown')
                    query.edit_message_text(
                        f'*🔥 Requested an account from the sponsers {TEAM}..\n\nAccount type : {account}\nPoints cost : {pointslimit}\n\n🔥 Request Sent*', parse_mode='Markdown')
                    userdb.update_one({"username": f'{username}'}, {
                        "$set": {"wallet": r_wallet}})
                    userdb.update_one({"username": f'{username}'}, {
                        "$set": {"withdrawals": withdrawals}})
                except Exception as e:
                    query.edit_message_text(
                        f'*⚠ Failed to request an account from the sponsers {TEAM}..\n\nAccount type : {account}\nPoints cost : {pointslimit}\n\n⚠ Request Unsent ⚠\n\nPlease forward this message to @{OWNER}*', parse_mode='Markdown')
                    print(e)
        except:
            pass

    if query.data == '1':
        username = query.from_user.username
        index = int(query.data)
        try:
            pointslimit = POINT_LIST[index]
            account = ACC_LIST[index]
            userinfo = userdb.find_one({"username": f"{username}"})
            withdrawals = userinfo["withdrawals"]
            wallet = int(userinfo["wallet"])
            if wallet > pointslimit:
                try:
                    r_wallet = wallet - pointslimit
                    withdrawals.append(account)
                    bot.send_message(
                        PROOFS_ID, f'*withdrawals🔥🔥🔥 Withdrawal Request 🔥🔥🔥\n\n🔥 Status : Approved\n🔥 From : @{username}\n🔥 Account : {account}\n🔥 Date : {datetime.now().strftime("%x")}\n\n🔥 Powered by @{OWNER}\n\n🔥🔥🔥 Request Listed 🔥🔥🔥*', parse_mode='Markdown')
                    query.edit_message_text(
                        f'*🔥 Requested an account from the sponsers {TEAM}..\n\nAccount type : {account}\nPoints cost : {pointslimit}\n\n🔥 Request Sent*', parse_mode='Markdown')
                    userdb.update_one({"username": f'{username}'}, {
                        "$set": {"wallet": r_wallet}})
                    userdb.update_one({"username": f'{username}'}, {
                        "$set": {"withdrawals": withdrawals}})
                except Exception as e:
                    query.edit_message_text(
                        f'*⚠ Failed to request an account from the sponsers {TEAM}..\n\nAccount type : {account}\nPoints cost : {pointslimit}\n\n⚠ Request Unsent ⚠\n\nPlease forward this message to @{OWNER}*', parse_mode='Markdown')
                    print(e)
        except:
            pass

    if query.data == '2':
        username = query.from_user.username
        index = int(query.data)
        try:
            pointslimit = POINT_LIST[index]
            account = ACC_LIST[index]
            userinfo = userdb.find_one({"username": f"{username}"})
            withdrawals = userinfo["withdrawals"]
            wallet = int(userinfo["wallet"])
            if wallet > pointslimit:
                try:
                    r_wallet = wallet - pointslimit
                    withdrawals.append(account)
                    bot.send_message(
                        PROOFS_ID, f'*withdrawals🔥🔥🔥 Withdrawal Request 🔥🔥🔥\n\n🔥 Status : Approved\n🔥 From : @{username}\n🔥 Account : {account}\n🔥 Date : {datetime.now().strftime("%x")}\n\n🔥 Powered by @{OWNER}\n\n🔥🔥🔥 Request Listed 🔥🔥🔥*', parse_mode='Markdown')
                    query.edit_message_text(
                        f'*🔥 Requested an account from the sponsers {TEAM}..\n\nAccount type : {account}\nPoints cost : {pointslimit}\n\n🔥 Request Sent*', parse_mode='Markdown')
                    userdb.update_one({"username": f'{username}'}, {
                        "$set": {"wallet": r_wallet}})
                    userdb.update_one({"username": f'{username}'}, {
                        "$set": {"withdrawals": withdrawals}})
                except Exception as e:
                    query.edit_message_text(
                        f'*⚠ Failed to request an account from the sponsers {TEAM}..\n\nAccount type : {account}\nPoints cost : {pointslimit}\n\n⚠ Request Unsent ⚠\n\nPlease forward this message to @{OWNER}*', parse_mode='Markdown')
                    print(e)
        except:
            pass

    if query.data == '3':
        username = query.from_user.username
        index = int(query.data)
        try:
            pointslimit = POINT_LIST[index]
            account = ACC_LIST[index]
            userinfo = userdb.find_one({"username": f"{username}"})
            withdrawals = userinfo["withdrawals"]
            wallet = int(userinfo["wallet"])
            if wallet > pointslimit:
                try:
                    r_wallet = wallet - pointslimit
                    withdrawals.append(account)
                    bot.send_message(
                        PROOFS_ID, f'*🔥🔥🔥 Withdrawal Request 🔥🔥🔥\n\n🔥 Status : Approved\n🔥 From : @{username}\n🔥 Account : {account}\n🔥 Date : {datetime.now().strftime("%x")}\n\n🔥 Powered by @{OWNER}\n\n🔥🔥🔥 Request Listed 🔥🔥🔥*', parse_mode='Markdown')
                    query.edit_message_text(
                        f'*🔥 Requested an account from the sponsers {TEAM}..\n\nAccount type : {account}\nPoints cost : {pointslimit}\n\n🔥 Request Sent*', parse_mode='Markdown')
                    userdb.update_one({"username": f'{username}'}, {
                        "$set": {"wallet": r_wallet}})
                    userdb.update_one({"username": f'{username}'}, {
                        "$set": {"withdrawals": withdrawals}})
                except Exception as e:
                    query.edit_message_text(
                        f'*⚠ Failed to request an account from the sponsers {TEAM}..\n\nAccount type : {account}\nPoints cost : {pointslimit}\n\n⚠ Request Unsent ⚠\n\nPlease forward this message to @{OWNER}*', parse_mode='Markdown')
                    print(e)
        except:
            pass

    if query.data == '4':
        username = query.from_user.username
        index = int(query.data)
        try:
            pointslimit = POINT_LIST[index]
            account = ACC_LIST[index]
            userinfo = userdb.find_one({"username": f"{username}"})
            wallet = int(userinfo["wallet"])
            withdrawals = userinfo["withdrawals"]
            if wallet > pointslimit:
                try:
                    r_wallet = wallet - pointslimit
                    withdrawals.append(account)
                    bot.send_message(
                        PROOFS_ID, f'*withdrawals🔥🔥🔥 Withdrawal Request 🔥🔥🔥\n\n🔥 Status : Approved\n🔥 From : @{username}\n🔥 Account : {account}\n🔥 Date : {datetime.now().strftime("%x")}\n\n🔥 Powered by @{OWNER}\n\n🔥🔥🔥 Request Listed 🔥🔥🔥*', parse_mode='Markdown')
                    query.edit_message_text(
                        f'*🔥 Requested an account from the sponsers {TEAM}..\n\nAccount type : {account}\nPoints cost : {pointslimit}\n\n🔥 Request Sent*', parse_mode='Markdown')
                    userdb.update_one({"username": f'{username}'}, {
                        "$set": {"wallet": r_wallet}})
                    userdb.update_one({"username": f'{username}'}, {
                        "$set": {"withdrawals": withdrawals}})
                except Exception as e:
                    query.edit_message_text(
                        f'*⚠ Failed to request an account from the sponsers {TEAM}..\n\nAccount type : {account}\nPoints cost : {pointslimit}\n\n⚠ Request Unsent ⚠\n\nPlease forward this message to @{OWNER}*', parse_mode='Markdown')
                    print(e)
        except:
            pass

    if query.data == '5':
        username = query.from_user.username
        index = int(query.data)
        try:
            pointslimit = POINT_LIST[index]
            account = ACC_LIST[index]
            userinfo = userdb.find_one({"username": f"{username}"})
            withdrawals = userinfo["withdrawals"]
            wallet = int(userinfo["wallet"])
            if wallet > pointslimit:
                try:
                    r_wallet = wallet - pointslimit
                    withdrawals.append(account)
                    bot.send_message(
                        PROOFS_ID, f'*🔥🔥🔥 Withdrawal Request 🔥🔥🔥\n\n🔥 Status : Approved\n🔥 From : @{username}\n🔥 Account : {account}\n🔥 Date : {datetime.now().strftime("%x")}\n\n🔥 Powered by @{OWNER}\n\n🔥🔥🔥 Request Listed 🔥🔥🔥*', parse_mode='Markdown')
                    query.edit_message_text(
                        f'*🔥 Requested an account from the sponsers {TEAM}..\n\nAccount type : {account}\nPoints cost : {pointslimit}\nCurrent Balance: {r_wallet}\n\n🔥 Request Sent*', parse_mode='Markdown')
                    userdb.update_one({"username": f'{username}'}, {
                        "$set": {"wallet": r_wallet}})
                    userdb.update_one({"username": f'{username}'}, {
                        "$set": {"withdrawals": withdrawals}})
                except Exception as e:
                    query.edit_message_text(
                        f'*⚠ Failed to request an account from the sponsers {TEAM}..\n\nAccount type : {account}\nPoints cost : {pointslimit}\n\n⚠ Request Unsent ⚠\n\nPlease forward this message to @{OWNER}*', parse_mode='Markdown')
                    print(e)
            else:
                update.message.reply_text(
                    '*❌ Insufficient Balance ❌*', parse_mode='Markdown')
        except:
            pass

    if query.data == "users":
        global q_panel
        q_panel = query
        q_panel.edit_message_text(
            "*🍻 Bot Control Panel 🍻\n\nSend the Target user's username as a reply [usr@username]*", parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    text='🔙 Back 🔙', callback_data='back_menu')]
            ]))

    if query.data == "search":
        search = userdb.find_one({"username": f"{user}"})
        try:
            query.edit_message_text(
                f"*🍻 Bot Control Panel 🍻\n\nSearch Results for @{user}\n\nUsername : @{user}\nBalance : {search['wallet']}\nStatus : {search['status']}\nRegistration ID : {search['_id']}*", parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        text='🔙 Back 🔙', callback_data='back_users')]
                ]))
        except:
            query.edit_message_text(
                f"*🍻 Bot Control Panel 🍻\n\nUser @{user} Not Found!*", parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        text='🔙 Back 🔙', callback_data='back_users')]
                ]))

    if query.data == "ban":
        print(user)
        if (user == "Zycho_66") or (user == "zycho_66"):
            query.edit_message_text(
                "*🍻 Bot Control Panel 🍻\n\nYou can't ban my developer!*", parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        text='🔙 Back 🔙', callback_data='back_users')]
                ]))
        else:
            try:
                userdb.update_one({"username": f"{user}"}, {
                                  "$set": {"status": "banned"}})
                query.edit_message_text(
                    f"*🍻 Bot Control Panel 🍻\n\n❌ User @{user} Banned!*", parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            text='🔙 Back 🔙', callback_data='back_users')]
                    ]))
            except:
                query.edit_message_text(
                    f"*🍻 Bot Control Panel 🍻\n\nUser @{user} Not Found!*", parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            text='🔙 Back 🔙', callback_data='back_users')]
                    ]))

    if query.data == "promote":
        if (user == "Zycho_66") or (user == "zycho_66"):
            query.edit_message_text(
                "*🍻 Bot Control Panel 🍻\n\n@Zycho_66 already has the developer permissions!*", parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        text='🔙 Back 🔙', callback_data='back_users')]
                ]))
        else:
            try:
                userdb.update_one({"username": f"{user}"}, {
                                  "$set": {"status": "admin"}})
                query.edit_message_text(
                    f"*🍻 Bot Control Panel 🍻\n\n❌ User @{user} Promoted!*", parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            text='🔙 Back 🔙', callback_data='back_users')]
                    ]))
            except:
                query.edit_message_text(
                    f"*🍻 Bot Control Panel 🍻\n\nUser @{user} Not Found!*", parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            text='🔙 Back 🔙', callback_data='back_users')]
                    ]))

    if query.data == "demote":
        if (user == "Zycho_66") or (user == "zycho_66"):
            query.edit_message_text(
                "*🍻 Bot Control Panel 🍻\n\nYou can't demote my developer!*", parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        text='🔙 Back 🔙', callback_data='back_users')]
                ]))
        else:
            try:
                userdb.update_one({"username": f"{user}"}, {
                                  "$set": {"status": "user"}})
                query.edit_message_text(
                    f"*🍻 Bot Control Panel 🍻\n\n❌ User @{user} Demoted!*", parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            text='🔙 Back 🔙', callback_data='back_users')]
                    ]))
            except:
                query.edit_message_text(
                    f"*🍻 Bot Control Panel 🍻\n\nUser @{user} Not Found!*", parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            text='🔙 Back 🔙', callback_data='back_users')]
                    ]))

    if query.data == "back_menu":
        query.edit_message_text(f'*🍻 Bot Control Panel 🍻\n\nAdmin : @{username}*', parse_mode='Markdown',
                                reply_markup=InlineKeyboardMarkup([
                                    [InlineKeyboardButton(
                                        text='💡 Users 💡', callback_data='users')],
                                    [InlineKeyboardButton(
                                        text='💳 Requests 💳', callback_data='requests')],
                                    [InlineKeyboardButton(
                                        text='🚀 Stats 🚀', callback_data='stats')]
                                ])
                                )

    if query.data == "back_users":
        query.edit_message_text(f"*🍻 Bot Control Panel 🍻\n\nTarget user : @{user}*", parse_mode='Markdown',
                                reply_markup=InlineKeyboardMarkup([
                                    [InlineKeyboardButton(
                                        text='♻ Search ♻', callback_data='search')],
                                    [InlineKeyboardButton(
                                        text='⚠ Ban ⚠', callback_data='ban')],
                                    [InlineKeyboardButton(
                                        text='⚡ Promote ⚡', callback_data='promote')],
                                    [InlineKeyboardButton(
                                        text='❌ Demote ❌', callback_data='demote')],
                                    [InlineKeyboardButton(
                                        text='🔙 Back 🔙', callback_data='back_menu')]
                                ]))

    if query.data == "requests":
        query.edit_message_text(
            text='*💡 Processing Query..*', parse_mode='Markdown')
        req_query = userdb.find({})
        msg = '*💳 Requests Processed 💳*\n'
        for req in req_query:
            for i in req['withdrawals']:
                if i != "admin-mode":
                    msg = msg + f"*\nRequest {i} for @{req['username']}*"

        query.edit_message_text(text=msg, parse_mode='Markdown',
                                reply_markup=InlineKeyboardMarkup([
                                    [InlineKeyboardButton(
                                        text='🔙 Back 🔙', callback_data='back_menu')]
                                ]))

    if query.data == "stats":
        query.edit_message_text(
            text='*🚀 Evaluating..*', parse_mode='Markdown')
        stat_q = userdb.find({})
        count = 0
        adminlist = '*🚀 Admins*'
        for stat in stat_q:
            count = count + 1
        admins_q = userdb.find({"status": "admin"})
        for admin in admins_q:
            adminlist = adminlist + '*\n@{}*'.format(admin['username'])

        msg = '*🚀 Bot Stats 🚀*\n\n' + \
            '*🚀 Users : {}\n\n*'.format(count) + adminlist

        query.edit_message_text(text=msg, parse_mode='Markdown',
                                reply_markup=InlineKeyboardMarkup([
                                    [InlineKeyboardButton(
                                        text='🔙 Back 🔙', callback_data='back_menu')]
                                ]))


def error(update: Update, context: CallbackContext) -> None:
    global userdb
    userid = update.effective_chat.id
    bot = context.bot
    bot.send_message(
        userid, "❌ *Oops! An error occured!*\n\nPlease notify my developers about this", parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="⚠ ZYCHO DEV ⚠", url='http://t.me/Zycho_66')]]))


def refferal(update: Update, context: CallbackContext) -> None:
    global userdb
    bot = context.bot
    username = str(update.message.from_user.username)
    url = helpers.create_deep_linked_url(bot.username, username)
    share = f"https://t.me/share/url?url={url}"

    registration = userdb.find_one({"username": f"{username}"})

    if registration:
        update.message.reply_text(f'🔥 *Yo-Yo! Your refferal link is here!*',
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(text="♻ Refferal Link ♻", url=url)], [InlineKeyboardButton(text="🔗 Share 🔗", url=share)]]),
                                  parse_mode='Markdown')
    else:
        update.message.reply_text(f'🔥 *Please Register For The {TEAM} Premium Account Generator Bot*',
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton(text="♻ Register ♻", callback_data='register')], [InlineKeyboardButton(text="🔗 Share 🔗", url=share)]]),
                                  parse_mode='Markdown')


def proof(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("""🍻 Not sure? Check this channel out and confirm yourself..\n""", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text='🍻 PROOFS 🍻', url=f'http://t.me/{PROOFS_USERNAME}')]
    ]))


def about(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"""*🔥 About us 🔥*\n\n{ABOUT}\n\n*Bot Developed by @Zycho_66*""", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text='🔥 OWNER 🔥', url=f'http://t.me/{OWNER}')],
        [InlineKeyboardButton(
            text='🔥 DEVELOPER 🔥', url=f'http://t.me/Zycho_66')]
    ]))


def balance(update: Update, context: CallbackContext) -> None:
    global userdb
    username = update.message.from_user.username
    userinfo = userdb.find_one({"username": f"{username}"})
    balance = userinfo["wallet"]
    reflistvar = userinfo["reflist"]
    reg_id = userinfo["_id"]
    reflist = ""

    for i in reflistvar:
        reflist = reflist + f'\n⚫ @{i}'

    update.message.reply_text("""*💳 Your Wallet 💳

💰 Balance : {} points

♻ Refferal List : {}

🚀 Registration ID : {}*""".format(balance, reflist, reg_id), parse_mode='Markdown')


def howto(update: Update, context: CallbackContext) -> None:
    global userdb
    update.message.reply_text(
        f"""*💡 How To Use 💡*\n\n{HOWTO_HEADER}\n\n{HOWTO_CONTEXT}\n\n{HOWTO_FOOTER}\n\n*Bot Developed by @Zycho_66*""", parse_mode='Markdown')


def contact(update: Update, context: CallbackContext) -> None:
    global userdb
    update.message.reply_text(f"""*🔔 Contact Us 🔔*\n\n- Contact the sponser for giveaway inquiries and claims..\n- Contact the developer for any error feedbacks..\n\n*Bot Developed by @Zycho_66*""", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text='🔔 Sponsers 🔔', url=f'http://t.me/{OWNER}')],
        [InlineKeyboardButton(
            text='🔔 Developer 🔔', url=f'http://t.me/Zycho_66')]
    ]))


def withdraw(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("*🚀 Please select an account type to withdraw..*", parse_mode='Markdown',
                              reply_markup=InlineKeyboardMarkup(
                                  [
                                      [InlineKeyboardButton(
                                          text=f"💳 {ACC_LIST[0]} 💳", callback_data='0')],
                                      [InlineKeyboardButton(
                                          text=f"💳 {ACC_LIST[1]} 💳", callback_data='1')],
                                      [InlineKeyboardButton(
                                          text=f"💳 {ACC_LIST[2]} 💳", callback_data='2')],
                                      [InlineKeyboardButton(
                                          text=f"💳 {ACC_LIST[3]} 💳", callback_data='3')],
                                      [InlineKeyboardButton(
                                          text=f"💳 {ACC_LIST[4]} 💳", callback_data='4')],
                                  ]))


def getreply(update: Update, context: CallbackContext) -> None:
    global q_panel
    global user
    global user
    rep_len = len(update.message.text)
    user = update.message.text[4:rep_len]
    trigger = update.message.text[0:4]
    if trigger == "usr@":
        q_panel.edit_message_text(f"*🍻 Bot Control Panel 🍻\n\nTarget user : @{user}*", parse_mode='Markdown',
                                  reply_markup=InlineKeyboardMarkup([
                                      [InlineKeyboardButton(
                                          text='♻ Search ♻', callback_data='search')],
                                      [InlineKeyboardButton(
                                          text='⚠ Ban ⚠', callback_data='ban')],
                                      [InlineKeyboardButton(
                                          text='⚡ Promote ⚡', callback_data='promote')],
                                      [InlineKeyboardButton(
                                          text='❌ Demote ❌', callback_data='demote')],
                                      [InlineKeyboardButton(
                                          text='🔙 Back 🔙', callback_data='back_menu')]
                                  ]))


def pointlist(update: Update, context: CallbackContext) -> None:
    msg = f"*🔩 Point List 🔩\n\n🔩 {ACC_LIST[0]} - {POINT_LIST[0]} Points\n🔩 {ACC_LIST[1]} - {POINT_LIST[1]} Points\n🔩 {ACC_LIST[2]} - {POINT_LIST[2]} Points\n🔩 {ACC_LIST[3]} - {POINT_LIST[3]} Points\n🔩 {ACC_LIST[4]} - {POINT_LIST[4]} Points\n🔩 {ACC_LIST[5]} - {POINT_LIST[5]} Points\n*"
    update.message.reply_text(msg, parse_mode='Markdown')


def ping(update: Update, context: CallbackContext) -> None:
    global userdb
    start = datetime.now()
    pingmsg = update.message.reply_text("Pong!")
    end = datetime.now()
    pingms = (end-start).microseconds / 1000
    pingmsg.edit_text(f"Pong! I'm awake!\n{pingms} ms")


def premium(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'*🗽 Contact me 🗽\n\nPurchase premium accounts for low prices*', parse_mode='Markdown',
                              reply_markup=InlineKeyboardMarkup([
                                  [InlineKeyboardButton(
                                      text='🗽 Contact Me 🗽', url=f'http://t.me/{OWNER}')]
                              ]))


def panel(update: Update, context: CallbackContext) -> None:
    username = update.message.from_user.username
    records = userdb.find({"username": f"{username}"})
    usr_stat = ""
    for record in records:
        if record["status"] == "admin":
            usr_stat = "admin"

    if usr_stat == "admin":
        update.message.reply_text(f'*🍻 Bot Control Panel 🍻\n\nAdmin : @{username}*', parse_mode='Markdown',
                                  reply_markup=InlineKeyboardMarkup([
                                      [InlineKeyboardButton(
                                          text='💡 Users 💡', callback_data='users')],
                                      [InlineKeyboardButton(
                                          text='💳 Requests 💳', callback_data='requests')],
                                      [InlineKeyboardButton(
                                          text='🚀 Stats 🚀', callback_data='stats')]
                                  ])
                                  )
    else:
        update.message.reply_text(
            f'*❌ Access Denied ❌\n\n Hey @{username}, you do not have access to my internal databases..*', parse_mode='Markdown')


def main() -> None:

    print("[ACCBOT] {} Ready to go..".format(
        datetime.now().strftime('[ %X ]')))

    os.system('python mongo.py')

    print("[ACCBOT] {} Initializing Accbot..".format(
        datetime.now().strftime('[ %X ]')))

    Token = TOKEN
    # pass bot's token.
    updater = Updater(Token)
    print("[ACCBOT] {} Configured Token..".format(
        datetime.now().strftime('[ %X ]')))

    # dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("ping", ping))
    dispatcher.add_handler(CommandHandler("panel", panel))
    dispatcher.add_handler(CallbackQueryHandler(query_handler))

    # Reply Keyboard handlers
    dispatcher.add_handler(MessageHandler(
        Filters.regex('🚀 Refferal 🚀'), refferal))
    dispatcher.add_handler(MessageHandler(
        Filters.regex('🍻 Proofs 🍻'), proof))
    dispatcher.add_handler(MessageHandler(
        Filters.regex('🔥 About us 🔥'), about))
    dispatcher.add_handler(MessageHandler(
        Filters.regex('🔔 Contact 🔔'), contact))
    dispatcher.add_handler(MessageHandler(
        Filters.regex('💡 How To Use 💡'), howto))
    dispatcher.add_handler(MessageHandler(
        Filters.regex('🗽 Premium 🗽'), premium))
    dispatcher.add_handler(MessageHandler(
        Filters.regex('💰 Balance 💰'), balance))
    dispatcher.add_handler(MessageHandler(
        Filters.regex('🔩 Point Limits 🔩'), pointlist))
    dispatcher.add_handler(MessageHandler(
        Filters.regex('💳 Withdraw Accounts 💳'), withdraw))
    dispatcher.add_handler(MessageHandler(
        Filters.reply, getreply))
    print("[ACCBOT] {} Added handlers..".format(
        datetime.now().strftime('[ %X ]')))
    print("[ACCBOT] {} Starting the bot..".format(
        datetime.now().strftime('[ %X ]')))

    # error handlers
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,SIGTERM or SIGABRT.
    updater.idle()


print("[ACCBOT] {} Connecting to MongoDB..".format(
    datetime.now().strftime('[ %X ]')))

client = MongoClient(MONGODB)
db = client["accbot"]
userdb = db["users"]

if __name__ == "__main__":
    main()

# ❌🔗⚡💡🚀⚠📌⏩💰🔮💳🔩🔥🔔❤🗽♻🍻🔜⚫🔙
