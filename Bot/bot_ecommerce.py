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

        if "produto" in user_input:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{API_BASE_URL}/products/")
                    response.raise_for_status()
                    products = response.json()

                if not products:
                    await turn_context.send_activity("📦 Nenhum produto disponível.")
                    return

                product_list = "\n".join([f"- {p['productName']} — R$ {p['price']:.2f}" for p in products])
                await turn_context.send_activity(f"🛒 Produtos disponíveis:\n{product_list}")
            except Exception:
                await turn_context.send_activity("⚠️ Erro ao consultar os produtos.")
            return

        elif "pedido" in user_input:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{API_BASE_URL}/orders/")
                    response.raise_for_status()
                    orders = response.json()

                user_orders = [
                    o for o in orders
                    if o.get("user_email", "").lower() == user_email.lower()
                ]

                if not user_orders:
                    await turn_context.send_activity("📭 Você ainda não tem pedidos.")
                    return

                reply = f"📦 Seus pedidos ({user_email}):\n"
                for o in user_orders:
                    reply += (
                        f"- ID: `{o['_id']}`\n"
                        f"  💰 Total: R$ {o['total_price']:.2f}\n"
                        f"  📌 Status: {o['status']}\n"
                        f"  📅 Data: {o['created_at'][:10]}\n\n"
                    )
                await turn_context.send_activity(reply)
            except Exception as e:
                await turn_context.send_activity(f"⚠️ Erro ao buscar seus pedidos.")

            return
        
        elif "extrato" in user_input:
            try:
                async with httpx.AsyncClient() as client:
                    
                    response = await client.get(f"{API_BASE_URL}/users/")
                    response.raise_for_status()
                    users = response.json()

                    matched_user = next(
                        (u for u in users if u["email"].lower() == user_email.lower()), None
                    )
                    if not matched_user:
                        await turn_context.send_activity("❌ Usuário não encontrado. Verifique o e-mail.")
                        return

                    user_id = matched_user["id"]

                    
                    response = await client.get(f"{API_BASE_URL}/users/{user_id}/cards/")
                    response.raise_for_status()
                    cards = response.json()

                    if not cards:
                        await turn_context.send_activity("💳 Nenhum cartão encontrado.")
                        return

                    msg = "💳 Seus cartões:\n\n"
                    for card in cards:
                        numero = card['number']
                        numero_oculto = f"{'*' * (len(numero) - 4)}{numero[-4:]}"  
                        msg += (
                            f"- Número: `{numero_oculto}`\n"
                            f"  📆 Validade: {card['expiration_date']}\n"
                            f"  💰 Saldo: R$ {card['balance']:.2f}\n\n"
                        )
                    await turn_context.send_activity(msg)

            except Exception:
                await turn_context.send_activity("⚠️ Erro ao buscar seus cartões.")
            return

        await turn_context.send_activity(
            "🤖 Comando não reconhecido. Digite `produtos`, `pedidos` ou `sair`."
        )

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)
        await self.conversation_state.save_changes(turn_context)
