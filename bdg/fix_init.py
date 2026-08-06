with open('/home/ubuntu/saranya/bdg/bot.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove any leftover reference to loadData() or local JSON loading if present
content = content.replace("loadData();", "")
content = content.replace("loadDataFromSupabase();", "loadDataFromSupabase();")

with open('/home/ubuntu/saranya/bdg/bot.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully cleaned up initialization!")
