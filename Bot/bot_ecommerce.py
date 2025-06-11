from botbuilder.core import TurnContext, ActivityHandler, ConversationState
from botbuilder.schema import ChannelAccount
import httpx

API_BASE_URL = "https://api-ecommerce-bigdata-b3b7c7g2e8emg7et.brazilsouth-01.azurewebsites.net"

class EcommerceBot(ActivityHandler):
    def __init__(self, conversation_state: ConversationState):
        self.conversation_state = conversation_state
        self.user_state_accessor = conversation_state.create_property("user_email")

    async def on_message_activity(self, turn_context: TurnContext):
        user_input = turn_context.activity.text.strip().lower()
        user_email = await self.user_state_accessor.get(turn_context)

        if user_input == "sair":
            await self.user_state_accessor.set(turn_context, None)
            await turn_context.send_activity("🔒 Você saiu da conta. Digite seu e-mail para entrar novamente.")
            return

        if not user_email:
            try:
                await turn_context.send_activity("🔎 Verificando seu e-mail...")
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{API_BASE_URL}/orders/")
                    response.raise_for_status()
                    orders = response.json()

                if any(order["user_email"].lower() == user_input for order in orders):
                    await self.user_state_accessor.set(turn_context, user_input)
                    await turn_context.send_activity(
                        f"✅ Login realizado com sucesso como **{user_input}**!\nVocê pode digitar:\n- `produtos`\n- `pedidos`\n- `extrato`\n- `sair`"
                    )
                else:
                    await turn_context.send_activity("❌ E-mail não encontrado em pedidos. Tente novamente.")
            except Exception as e:
                await turn_context.send_activity("⚠️ Erro ao verificar o e-mail. Tente novamente mais tarde.")
            return

        await turn_context.send_activity(
            "🤖 Comando não reconhecido. Digite `produtos`, `pedidos` ou `sair`."
        )

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)
        await self.conversation_state.save_changes(turn_context)
