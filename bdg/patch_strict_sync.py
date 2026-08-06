with open('/home/ubuntu/saranya/bdg/bot.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Ensure getNumberSize explicitly enforces 0-4 Small, 5-9 Big
size_func_old = """function getNumberSize(num) {
    const n = parseInt(num);
    if (isNaN(n)) return "Unknown";
    return n >= 5 ? "Big" : "Small";
}"""

size_func_new = """function getNumberSize(num) {
    const n = parseInt(num);
    if (isNaN(n)) return "Unknown";
    return n >= 5 ? "BIG" : "SMALL";
}"""

content = content.replace(size_func_old, size_func_new)

# Also update getNumInfo to enforce strict 0-4 Small, 5-9 Big
num_info_old = """function getNumInfo(item) {
    const n = parseInt(item.number || item.winNumber || 0);
    const size = n >= 5 ? "BIG" : "SMALL";"""

num_info_new = """function getNumInfo(item) {
    const n = parseInt(item.number || item.winNumber || 0);
    const size = n >= 5 ? "BIG" : "SMALL"; // 0-4 Small, 5-9 Big"""

# In runPredict, ensure we call pollAndStoreApiResults() right before deciding prediction to guarantee latest data
run_predict_target = "    const signal = decidePrediction(list);"
run_predict_replacement = "    await pollAndStoreApiResults();\n    const signal = decidePrediction(list);"

content = content.replace(run_predict_target, run_predict_replacement)

with open('/home/ubuntu/saranya/bdg/bot.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated pre-prediction sync and strict sizing rules!")
