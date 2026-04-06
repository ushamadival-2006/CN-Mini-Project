import asyncio
import websockets

clients = {}
rooms = {}

async def handler(websocket):
    try:
        # Receive username and room
        username = await websocket.recv()
        room = await websocket.recv()

        clients[websocket] = (username, room)

        if room not in rooms:
            rooms[room] = []

        rooms[room].append(websocket)

        print(f"{username} joined {room}")
        print("Rooms:", rooms)

        await websocket.send("Connected to server!")

        async for message in websocket:

            # ---------- FILE ----------
            if message.startswith("FILE|"):
                try:
                    _, filename, filedata = message.split("|", 2)

                    print(f"{username} sent file {filename}")

                    for client in rooms[room]:
                        if client != websocket:
                            try:
                                await client.send(f"FILE|{filename}|{filedata}")
                            except:
                                pass
                except Exception as e:
                    print("File error:", e)

            # ---------- MESSAGE ----------
            else:
                formatted = f"{username}: {message}"

                for client in rooms[room]:
                    if client != websocket:
                        try:
                            await client.send(formatted)
                        except:
                            pass

    except Exception as e:
        print("Connection error:", e)

    finally:
        username, room = clients.get(websocket, ("Unknown", "Unknown"))

        if room in rooms and websocket in rooms[room]:
            rooms[room].remove(websocket)

        clients.pop(websocket, None)

        print(f"{username} disconnected")


async def main():
    server = await websockets.serve(
        handler,
        "0.0.0.0",   # 🔥 IMPORTANT (allows other devices)
        12345,
        max_size=10_000_000
    )
    print("WebSocket server running...")
    await server.wait_closed()

asyncio.run(main())