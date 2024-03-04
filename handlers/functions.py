import sqlite3
connect = sqlite3.connect("db/redshark.db")
cursor = connect.cursor()
def status_users(message_id):
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",
                                 (message_id,))
    user_status = cursor.fetchone()
    if user_status[0] == 'Rab':
        user_status2 = '<b>♦️ Developer</b>'
    if user_status[0] == 'Owner':
        user_status2 = '<b>👨‍💻 Owner</b>'
    if user_status[0] == 'Helper_Admin':
        user_status2 = '<b>⛔️ Helper_Admin</b>'        
    if user_status[0] == 'Admin':
        user_status2 = '<b>⛔️ Admin</b>'

    if user_status[0] == 'Player':
        user_status2 = '<b>💤 Игрок</b>'
    if user_status[0] == 'Titanium':
        user_status2 = '<b>👾 TITANIUM</b>'
    if user_status[0] == 'Deluxe':
        user_status2 = '<b>🔥 DELUXE</b>'
    if user_status[0] == 'Vip':
        user_status2 = '<b>❤️ Вип</b>'
    if user_status[0] == 'Chem':
        user_status2 = '<b>🏆 Чемпион</b>'
    if user_status[0] == 'Korol':
        user_status2 = '<b>👑 Король</b>'
    if user_status[0] == 'Donater':
        user_status2 = '<b>😈 Донатер</b>'        
    return user_status2



## Можете сравнить с корректным результатом, всё 1-в-1:
# result = 7 - math.sin(3.141592 * 0.75) + math.cos(2.718281)

