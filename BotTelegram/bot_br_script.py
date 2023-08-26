import random
import asyncio
from datetime import datetime, timedelta
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest


# Substitua 'SEU_TOKEN_AQUI' pelo token do seu bot
TOKEN = '6460980793:AAHITXuEPK3ndJtAyrMZZxBhpad-ogBgHvo'

# Substitua 'ID_DO_CHAT' pelo ID do grupo ou chat onde você deseja enviar as mensagens
ID_DO_CHAT = '-1001913779835'

# Seu link personalizado
LINK_COMUM = 'sinaisdomestre.com'

# Lista de mensagens personalizadas
messages_fortune_tiger = [
    """*🕵️‍♂️ OPORTUNIDADE ENCONTRADA 🕵️‍♂️*

🍀 *PLATAFORMA NOVA BUGADA APROVEITE*
🐯 *FORTUNE TIGER {versao_jogo}*
🔥 *Nº de Jogadas:* {num_jogadas}
⏰ *Tolerância:* 3 minutos
🎰 *Gire:* {giros_turbo}x no *TURBO* e recarregue o jogo
Depois gire {giros_manual}x *MANUAL*
🔴 *SAIA NO PRIMEIRO GRANDE GANHO*

🚨 *FUNCIONA APENAS NA PLATAFORMA ABAIXO!* ⬇️
🖥 *Plataforma:* [CliqueAqui]({LINK_COMUM})

👇⚠️ *FUNCIONA SOMENTE NESSA PLATAFORMA* ⚠️👇"""
    # Adicione mais mensagens personalizadas aqui
]

messages_fortune_ox = [
    """*🕵️‍♂️ OPORTUNIDADE ENCONTRADA 🕵️‍♂️*

🍀 *PLATAFORMA NOVA BUGADA APROVEITE*
🐂 *FORTUNE OX {versao_jogo}*
🔥 *Nº de Jogadas:* {num_jogadas}
⏰ *Tolerância:* 3 minutos
🎰 *Gire:* {giros_turbo}x no *TURBO* e recarregue o jogo
Depois gire {giros_manual}x *MANUAL*
🔴 *SAIA NO PRIMEIRO GRANDE GANHO*

🚨 *FUNCIONA APENAS NA PLATAFORMA ABAIXO!* ⬇️
🖥 *Plataforma:* [CliqueAqui]({LINK_COMUM})

👇⚠️ *FUNCIONA SOMENTE NESSA PLATAFORMA* ⚠️👇"""
    # Adicione mais mensagens personalizadas aqui
]

messages_fortune_mouse = [
    """*🕵️‍♂️ OPORTUNIDADE ENCONTRADA 🕵️‍♂️*

🍀 *PLATAFORMA NOVA BUGADA APROVEITE*
🐭 *FORTUNE MOUSE {versao_jogo}*
🔥 *Nº de Jogadas:* {num_jogadas}
⏰ *Tolerância:* 3 minutos
🎰 *Gire:* {giros_turbo}x no *TURBO* e recarregue o jogo
Depois gire {giros_manual}x *MANUAL*
🔴 *SAIA NO PRIMEIRO GRANDE GANHO*

🚨 *FUNCIONA APENAS NA PLATAFORMA ABAIXO!* ⬇️
🖥 *Plataforma:* [CliqueAqui]({LINK_COMUM})

👇⚠️ *FUNCIONA SOMENTE NESSA PLATAFORMA* ⚠️👇"""
    # Adicione mais mensagens personalizadas aqui
]

acertos = 0
erros = 0

data_ultima_atualizacao = datetime.now()

#ATUALIZAÇÃO DO JOGO !
async def send_random_message(bot, chat_id, game):
    global acertos, erros, versao_jogo, data_ultima_atualizacao

    if game == "Fortune Tiger":
        messages = messages_fortune_tiger
    elif game == "Fortune OX":
        messages = messages_fortune_ox
    elif game == "Fortune Mouse":
        messages = messages_fortune_mouse
    else:
        raise ValueError("Jogo inválido")

    versao_jogo = "v3.4"

    if (datetime.now() - data_ultima_atualizacao).days >= 25:
        # Atualiza a versão do jogo
        versao_numerica, versao_decimal = versao_jogo[1:].split(".")
        
        if versao_decimal == "9":
            nova_versao = int(versao_numerica) + 1
            versao_jogo = f"v{nova_versao}.0"
        else:
            nova_versao_decimal = int(versao_decimal) + 1
            versao_jogo = f"v{versao_numerica}.{nova_versao_decimal}"
        
        data_ultima_atualizacao = datetime.now()

    num_jogadas = random.randint(6, 23)
    soma_giros = num_jogadas
    while True:
        giros_turbo = random.randint(1, soma_giros - 1)
        giros_manual = soma_giros - giros_turbo
        if giros_manual >= 1:
            break
    
    # Escolha aleatoriamente entre vitória (95%) e derrota (5%)
    outcome = random.choices(['vitoria', 'derrota'], weights=[0.95, 0.05])[0]
    
    if outcome == 'vitoria':
        message = random.choice(messages).format(num_jogadas=num_jogadas, giros_turbo=giros_turbo, giros_manual=giros_manual, LINK_COMUM=LINK_COMUM,  versao_jogo=versao_jogo)
        acertos += 1
    else:
        message = "*🔴 LOSS 🔴* \n\n Infelizmente, não tivemos sucesso desta vez. Continue tentando!"
        erros += 1
    
    keyboard = [[InlineKeyboardButton("🎯 NÃO PERCA ESSA CHANCE!", url=LINK_COMUM)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    sent_message = await bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup, parse_mode='Markdown', disable_web_page_preview=True)
    
    print(f"Comando executado: send_random_message(bot, chat_id, '{game}')")
    
    return sent_message.message_id

async def send_victory_message(bot, chat_id):
    global acertos, erros
    
    victory_message = "*🍀 VITÓRIA CONFIRMADA 🍀*"
    
    keyboard = [[InlineKeyboardButton("🤑 VAI FICAR DE FORA?", url=LINK_COMUM)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await bot.send_message(chat_id=chat_id, text=victory_message, reply_markup=reply_markup, parse_mode='Markdown', disable_web_page_preview=True)
    
    await asyncio.sleep(1)  # Pequeno atraso para garantir que as mensagens sejam enviadas em ordem
    
    # Gera o relatório diário às 18:00 (horário de São Paulo)
    if datetime.now().hour == 18 and datetime.now().minute == 0:
        total_jogadas = acertos + erros
        porcentagem_acertos = (acertos / total_jogadas) * 100
        
        report_message = f"📊 *RELATÓRIO DIÁRIO* 📊\n\n" \
                         f"🎉 Acertos: {acertos}\n" \
                         f"❌ Erros: {erros}\n" \
                         f"📈 Porcentagem de Acertos: {porcentagem_acertos:.2f}%"
        
        await bot.send_message(chat_id=chat_id, text=report_message)
        acertos = 0
        erros = 0
        
game_messages = {
    "Fortune Tiger": messages_fortune_tiger,
    "Fortune OX": messages_fortune_ox,
    "Fortune Mouse": messages_fortune_mouse
}

async def main():
    bot = Bot(token=TOKEN)
    chat_id = ID_DO_CHAT
    analyzing_message_id = None  # ID da mensagem de análise

    while True:
        # Percorre os jogos aleatoriamente
        games = list(game_messages.keys())
        random.shuffle(games)
        
        for game in games:
            messages = game_messages[game]
            
            # Apaga a mensagem de análise anterior, se existir
            if analyzing_message_id is not None:
                try:
                    await bot.delete_message(chat_id=chat_id, message_id=analyzing_message_id)
                except Exception as e:
                    print(f"Error deleting message: {e}")
            
            # Envia mensagem aleatória para o jogo atual
            message_id = await send_random_message(bot, chat_id, game)
            
            await asyncio.sleep(180)  # Espera 3 minutos
            await send_victory_message(bot, chat_id)
            await asyncio.sleep(5)  # Espera 5 segundos
            
            analyzing_message = await bot.send_photo(
                chat_id=chat_id,
                photo="https://aqi.co.id/wp-content/uploads/2021/10/Tidak-Selalu-Jahat-Inilah-Pengertian-Hacker-yang-Sesungguhnya.jpg",
                caption="      🔍 *ANALISANDO ALGORITMO PARA POSSÍVEL ENTRADA* 🧐      \n\nNossos *robôs* estão trabalhando duro para identificar a *melhor oportunidade.* Fique ligado!🚀🔮",
                parse_mode='Markdown'
            )
            analyzing_message_id = analyzing_message.message_id  # Atualiza o ID da mensagem de análise

            await asyncio.sleep(random.randint(90, 180))  # Espera entre 1 minuto e meio e 3 minutos

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
