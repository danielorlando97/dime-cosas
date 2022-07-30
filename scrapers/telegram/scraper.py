import asyncio
import configparser
from sqlite3 import Date
from telethon import TelegramClient
import telethon
import pandas as pd
from telethon.tl.types import Chat, Dialog
from telethon.errors.rpcerrorlist import ChannelPrivateError
import os
from message_info import TelegramGroupMessageInfo, TelegramUserInfo
from datetime import timedelta, date, datetime

config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
api_hash = str(api_hash)

# phone = config['Telegram']['phone']
# username = config['Telegram']['username']
file_name = config['Telegram']['file_name']

client = TelegramClient(file_name, api_id, api_hash)
to_be_processed = set()
done = set()
edges = {}
package_dir = os.path.dirname(os.path.abspath(__file__))

async def main():
    """
        Scraper Initial Method 
            - start the telegram client 
            - list the user's groups 
    """

    global groups, edges, to_be_processed, done, package_dir    
    
    # Getting information about User
    me = await client.get_me()	

    # "me" is a user object. You can pretty-print
    # any Telegram object with the "stringify" method:
    print(me.stringify())   


    # Init Scarper Data Dumps with pd.pickle 
    await init_empty()


async def init_empty():
    """
    This method has to be used when no pickle file is available.
    It iters through the dialogs, collect links and general data from them 
    and it finally saves the pickle files on the host machine.
    """
    to_be_processed = set()
    edges = {}
    done = set()
    groups = []
    
    # Get today's date
    today = datetime.now()
    
    # Yesterday date
    yesterday = today - timedelta(days = 1)

    async for dialog in client.iter_dialogs():
    
    	if dialog.is_group:   
            await get_all_sms(dialog, yesterday)

            # temp_to_be_processed = await gather_links(dialog)
            # edges = update_edges(edges, temp_to_be_processed, dialog)
            # to_be_processed = to_be_processed.union(temp_to_be_processed)   
            # df_tbp = pd.DataFrame(list(to_be_processed))
            # df_tbp.to_pickle(os.path.join(package_dir,'to_be_processed'))   
            # groups.append(await collect_data(dialog, ""))   
            # df_groups = pd.DataFrame.from_dict(groups)
            # df_groups.to_pickle(os.path.join(package_dir,'groups')) 
            # done.add(str(dialog.entity.id)) 
            # df_done = pd.DataFrame(list(done))
            # df_done.to_pickle(os.path.join(package_dir,'done')) 
            # df_edges = pd.DataFrame(list(edges.items()), columns = ['destination vertex','origin vertices'])
            # df_edges.to_pickle(os.path.join(package_dir,'edges'))
    
    print("	---[✓✓] Init completed!")

# TODO: Replies Analyze 
async def get_all_sms(dialog: Dialog, limit_date : Date = None):
    result = []
    try:
        async for message in client.iter_messages(dialog.id, limit=1000000):
            if message.date < limit_date: break
            result.append(TelegramGroupMessageInfo(
                text=message.message,
                sender= TelegramUserInfo(
                    name= message.sender.first_name,
                    username= message.sender.username,
                    phone= message.sender.phone
                ),
                date=message.date,
                group=dialog.name,
                dialog_id=dialog.id,
                sms_url= None
            ))
            
    except ChannelPrivateError as e:
        pass
    except TypeError as e:
        pass

	# l = set()
    # try:
    #     async for message in client.iter_messages(dialog.id, search="https://t.me/", limit=1000000):
    #         pass
    #     print("	---[✓] Links collected succesfully in: "+str(dialog.entity.id))
	# except telethon.errors.rpcerrorlist.ChannelPrivateError as e:
	# 	print(e)
	# 	return l
	# except TypeError as e:
	# 	pass

	# return l


with client:
	client.loop.run_until_complete(main())
	client.disconnect()
