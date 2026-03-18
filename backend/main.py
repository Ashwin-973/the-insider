import asyncio
import os

import uvicorn

'''
selector event loop provides better compatability with 
aiosqlite and psycopg than the default 
proactor event loop policy
'''
if os.name=="nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())



if __name__=="__main__":
    uvicorn.run("src.app:app",host="127.0.0.1",port=1999,reload=True)