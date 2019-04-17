import  asyncio
import logging; logging.basicConfig(level=logging.INFO)
import aiomysql

@asyncio.coroutine
def create_pool(loop,**kv):
    logging.info("db connection")
    global  __pool
    __pool=yield from aiomysql.create_pool{
        
    }
    


