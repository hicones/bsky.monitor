import os
import sqlite3
import requests
import asyncio
import websockets
from dotenv import load_dotenv

load_dotenv()

profile_ids = os.getenv("PROFILE_IDS").split(",")

connected_clients = set()

async def notify_clients(new_post):
    if connected_clients:
        await asyncio.wait([client.send(new_post) for client in connected_clients])

async def websocket_handler(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            pass
    finally:
        connected_clients.remove(websocket)

async def start_server():
    server = await websockets.serve(websocket_handler, "localhost", 6789)
    await server.wait_closed()

def init_db():
    conn = sqlite3.connect('posts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts (
                    cid TEXT PRIMARY KEY
                )''')
    conn.commit()
    conn.close()

def save_post_cid(post_id):
    conn = sqlite3.connect('posts.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO posts (cid) VALUES (?)', (post_id,))
    conn.commit()
    conn.close()

def post_cid_exists(post_id):
    conn = sqlite3.connect('posts.db')
    c = conn.cursor()
    c.execute('SELECT 1 FROM posts WHERE cid=?', (post_id,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def get_profile_posts(profile_id):
    url = f"https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor={profile_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("feed", [])
    else:
        return None

async def monitor_profiles():
    while True:
        for profile_id in profile_ids:
            posts = get_profile_posts(profile_id)
            if posts:
                for post_data in posts:
                    post = post_data["post"]
                    post_id = post["cid"]
                    content = post["record"]["text"]
                    author = post["author"]["displayName"]
                    if not post_cid_exists(post_id):
                        save_post_cid(post_id)
                        await notify_clients(f"Novo post de {author}: {content}")
        await asyncio.sleep(60)

init_db()
asyncio.get_event_loop().create_task(monitor_profiles())
asyncio.get_event_loop().run_until_complete(start_server())
