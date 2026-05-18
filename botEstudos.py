import os
import asyncio
import json
import random
from datetime import datetime, date
from pathlib import Path
import pytz
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ─── CONFIGURAÇÃO ────────────────────────────────────────────────
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = int(os.environ["CHAT_ID"])
TIMEZONE  = "America/Sao_Paulo"
DATA_FILE = "estudos.json"
# ─────────────────────────────────────────────────────────────────

MENSAGENS = [
    "📚 Bora estudar! Já faz 30 min, não para agora.",
    "📖 Tá estudando? Continua firme! 💪",
    "🧠 Lembrete: seus estudos te esperam!",
    "⏰ 30 minutinhos se passaram — foco total!",
    "🎯 Cada sessão conta. Bora lá!",
    "📝 Não deixa o tempo passar — abre o material!",
    "🚀 Você no futuro agradece você de agora. Estuda!",
]

# ─── PERSISTÊNCIA ────────────────────────────────────────────────

def carregar_dados() -> dict:
    if Path(DATA_FILE).exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"registros": {}}

def salvar_dados(dados: dict):
    with open(DATA_FILE, "w") as f:
        json.dump(dados, f)

def hoje_str() -> str:
    return datetime.now(pytz.timezone(TIMEZONE)).strftime("%Y-%m-%d")

# ─── LEMBRETE ────────────────────────────────────────────────────

async def enviar_lembrete(bot):
    tz = pytz.timezone(TIMEZONE)
    agora = datetime.now(tz)
    # Seg=0 ... Sáb=5, Dom=6
    if agora.weekday() == 6:
        return
    await bot.send_message(
        chat_id=CHAT_ID,
        text=random.choice(MENSAGENS)
    )

# ─── COMANDOS ────────────────────────────────────────────────────

async def cmd_estudei(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "ℹ️ Me diz quantas horas você estudou!\nEx: /estudei 2.5"
        )
        return

    try:
        horas = float(context.args[0].replace(",", "."))
    except ValueError:
        await update.message.reply_text("❌ Número inválido. Ex: /estudei 2 ou /estudei 1.5")
        return

    dados = carregar_dados()
    hoje = hoje_str()
    dados["registros"][hoje] = {"estudou": True, "horas": horas}
    salvar_dados(dados)

    registros = dados["registros"]
    total_dias = sum(1 for r in registros.values() if r["estudou"])
    total_horas = sum(r["horas"] for r in registros.values() if r["estudou"])

    await update.message.reply_text(
        f"✅ Registrado! {horas}h de estudos hoje.\n\n"
        f"📊 *Seu progresso:*\n"
        f"📅 Dias estudados: *{total_dias}*\n"
        f"⏱️ Total de horas: *{total_horas:.1f}h*",
        parse_mode="Markdown"
    )

async def cmd_nao_estudei(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dados = carregar_dados()
    hoje = hoje_str()
    dados["registros"][hoje] = {"estudou": False, "horas": 0}
    salvar_dados(dados)
    await update.message.reply_text(
        "😔 Ok, registrado. Amanhã é um novo dia — bora recuperar! 💪"
    )

async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dados = carregar_dados()
    registros = dados["registros"]

    if not registros:
        await update.message.reply_text("Nenhum registro ainda. Use /estudei ou /nao_estudei!")
        return

    total_dias = sum(1 for r in registros.values() if r["estudou"])
    total_horas = sum(r["horas"] for r in registros.values() if r["estudou"])
    dias_sem = sum(1 for r in registros.values() if not r["estudou"])
    media = total_horas / total_dias if total_dias > 0 else 0

    await update.message.reply_text(
        f"📊 *Seus estudos*\n\n"
        f"✅ Dias estudados: *{total_dias}*\n"
        f"❌ Dias sem estudar: *{dias_sem}*\n"
        f"⏱️ Total de horas: *{total_horas:.1f}h*\n"
        f"📈 Média por dia: *{media:.1f}h*",
        parse_mode="Markdown"
    )

async def cmd_ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 *Bot de Estudos*\n\n"
        "Comandos:\n"
        "/estudei 2.5 — Registra que estudou (informe as horas)\n"
        "/nao\\_estudei — Registra que não estudou hoje\n"
        "/stats — Ver total de dias e horas\n"
        "/ajuda — Ver esta mensagem\n\n"
        "⏰ Lembretes de 30 em 30 min das 16h às 22h (seg a sáb)",
        parse_mode="Markdown"
    )

# ─── MAIN ────────────────────────────────────────────────────────

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    bot = app.bot

    app.add_handler(CommandHandler("estudei", cmd_estudei))
    app.add_handler(CommandHandler("nao_estudei", cmd_nao_estudei))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("ajuda", cmd_ajuda))

    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    scheduler.add_job(
        enviar_lembrete,
        "cron",
        day_of_week="mon-sat",
        hour="16-21",
        minute="0,30",
        args=[bot]
    )
    scheduler.start()

    print("📚 Bot de estudos rodando!")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
