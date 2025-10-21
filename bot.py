import os
from flask import Flask, request
import telebot
from datetime import datetime
import schedule
import threading
import time as time_module

TOKEN = '8095142428:AAE_A7_bobIVyc59NBg92Ue7IqXrqM_IwsE'
CHAT_ID = '-1003087885971'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
trabajos_del_dia = []

@app.route('/trabajo', methods=['POST'])
def recibir_trabajo():
    try:
        data = request.json
        trabajos_del_dia.append(data)
        print(f"✅ Trabajo recibido: {data['maquina']}")
        return {'status': 'ok'}, 200
    except Exception as e:
        return {'status': 'error'}, 500

def generar_resumen():
    if not trabajos_del_dia:
        bot.send_message(CHAT_ID, "📊 RESUMEN DEL DÍA\n━━━━━━━━━━━━━━━━━━━━\n\n❌ No hay trabajos.")
        return
    
    trabajos = sorted(trabajos_del_dia, key=lambda x: x.get('openTime', ''))
    resumen = f"📊 RESUMEN - {datetime.now().strftime('%d/%m/%Y')}\n━━━━━━━━━━━━━━━━━━━━\n\n"
    resumen += f"🔧 TRABAJOS: {len(trabajos)}\n\n"
    
    for i, t in enumerate(trabajos, 1):
        resumen += f"{i}. {t['maquina']} - {t['tipo']} ({t['duracion']}m)\n"
    
    bot.send_message(CHAT_ID, resumen)
    trabajos_del_dia.clear()

@bot.message_handler(commands=['resumen'])
def comando_resumen(message):
    if str(message.chat.id) == CHAT_ID:
        generar_resumen()

schedule.every().day.at("21:00").do(generar_resumen)

def run_schedule():
    while True:
        schedule.run_pending()
        time_module.sleep(60)

def run_bot():
    bot.infinity_polling()

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

if __name__ == '__main__':
    import os
    schedule_thread = threading.Thread(target=run_schedule, daemon=True)
    schedule_thread.start()
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    run_bot()
```

6. **Pega el código** (Ctrl + V)
7. **Guarda** (Ctrl + S)
8. **Cierra el archivo**
9. **Ahora renombra el archivo:**
   - Click derecho en `bot.txt`
   - "Cambiar nombre"
   - Borra `.txt` y escribe `.py`
   - Debe quedar: `bot.py`
   - Si te dice "Cambiar extensión puede hacer que el archivo no funcione" → Click "Sí"

---

### **Archivo 2: requirements.txt**

1. **Click derecho** en la carpeta
2. **"Nuevo" → "Documento de texto"**
3. **Nombra:** `requirements.txt` (con .txt)
4. **Abre el archivo**
5. **Pega esto:**
```
pyTelegramBotAPI==4.14.0
Flask==3.0.0
schedule==1.2.0
gunicorn==21.2.0
```
6. **Guarda y cierra**

---

### **Archivo 3: Procfile**

1. **Click derecho** en la carpeta
2. **"Nuevo" → "Documento de texto"**
3. **Nombra:** `Procfile` (SIN .txt, solo "Procfile")
4. **Abre el archivo**
5. **Pega esto:**
```

web: python bot.py
