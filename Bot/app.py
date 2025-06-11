from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    BotFrameworkAdapter,
    ConversationState,
    MemoryStorage,
    TurnContext, 
)
from botbuilder.schema import Activity
from ecommerce_bot import EcommerceBot 
import asyncio

app = FastAPI()

memory = MemoryStorage()
conversation_state = ConversationState(memory)

bot = EcommerceBot(conversation_state)

adapter_settings = BotFrameworkAdapterSettings(app_id="", app_password="")
adapter = BotFrameworkAdapter(adapter_settings)

async def on_error(context: TurnContext, error: Exception):
    print(f"[on_error] Erro: {error}")
    await context.send_activity("Desculpe, ocorreu um erro ao processar sua solicitação.")

adapter.on_turn_error = on_error

@app.post("/api/messages")
async def messages(request: Request):
    body = await request.json()
    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")

    async def call_bot(turn_context):
        await bot.on_turn(turn_context)

    return await adapter.process_activity(activity, auth_header, call_bot)
