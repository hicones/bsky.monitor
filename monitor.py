import os
import sqlite3
import requests
import asyncio
import websockets
import json
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

load_dotenv()

VALID_TOKENS = set(os.getenv("VALID_TOKENS").split(","))

profile_ids = os.getenv("PROFILE_IDS").split(",")

connected_clients = set()

async def notify_clients(new_post):
    if connected_clients:
        print(f"Notificação enviada para {len(connected_clients)} clientes: {new_post}")
        await asyncio.gather(*(client.send(new_post) for client in connected_clients))

async def websocket_handler(websocket, path):
    query_params = parse_qs(urlparse(path).query)
    token = query_params.get("token", [None])[0]

    if token is None or token not in VALID_TOKENS:
        await websocket.close(reason="Token de autenticação inválido ou não fornecido")
        return

    connected_clients.add(websocket)
    print(f"Conexão estabelecida com {websocket.remote_address}")

    try:
        async for message in websocket:
            print(f"Mensagem recebida de {websocket.remote_address}: {message}")

    except websockets.ConnectionClosed as e:
        print(f"Conexão fechada com {websocket.remote_address}: {e}")

    finally:
        connected_clients.remove(websocket)
        print(f"Conexão encerrada com {websocket.remote_address}")

async def start_server():
    server = await websockets.serve(websocket_handler, "0.0.0.0", 3000)
    print("Servidor WebSocket online em ws://localhost:3000")
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
                    if not post_cid_exists(post_id):
                        save_post_cid(post_id)
                        print(f"Novo post detectado: {post}")
                        await notify_clients(json.dumps(post))
        await asyncio.sleep(30)

init_db()

async def main():
    await asyncio.gather(
        start_server(),
        monitor_profiles()
    )

asyncio.run(main())
