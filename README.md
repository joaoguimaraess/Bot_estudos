# 📚 Bot Telegram — Estudos

Bot que manda lembretes de 30 em 30 min das 16h às 22h (seg a sáb) e registra seus dias e horas de estudo.

-----

## Passo 1 — Criar o bot no Telegram

1. Abra o Telegram e procure por **@BotFather**
1. Envie `/newbot`
1. Escolha um nome (ex: `Estudos Bot`) e um username (ex: `meus_estudos_bot`)
1. Guarde o **token** gerado
1. Abra o bot e clique em **Start**

-----

## Passo 2 — Descobrir seu Chat ID

1. Acesse no navegador (substituindo pelo seu token):
   
   ```
   https://api.telegram.org/bot<SEU_TOKEN>/getUpdates
   ```
1. Procure por `"chat": { "id": 123456789` — esse é o seu `CHAT_ID`

-----

## Passo 3 — Deploy no Railway

1. Crie um novo repositório no GitHub e suba `bot_estudos.py` e `requirements_estudos.txt`
- Renomeie `requirements_estudos.txt` para `requirements.txt` no repositório
- Renomeie `bot_estudos.py` para `bot.py` no repositório
1. No Railway: **New Project → Deploy from GitHub repo**
1. Vá em **Variables** e adicione:
   
   |Nome       |Valor                      |
   |-----------|---------------------------|
   |`BOT_TOKEN`|o token que o BotFather deu|
   |`CHAT_ID`  |seu ID numérico (sem aspas)|
1. Em **Settings → Start Command**:
   
   ```
   python bot.py
   ```
1. Clique em **Deploy** ✅

-----

## Como usar

|Comando       |O que faz                           |
|--------------|------------------------------------|
|`/estudei 2.5`|Registra que estudou X horas hoje   |
|`/nao_estudei`|Registra que não estudou hoje       |
|`/stats`      |Mostra dias estudados, horas e média|
|`/ajuda`      |Lista todos os comandos             |

-----

## Lembretes

- Disparados de **30 em 30 minutos** das **16h às 22h**
- Somente de **segunda a sábado**
- 7 mensagens diferentes sortidas aleatoriamente