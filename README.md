```markdown
# GC-Checker

A Python tool to check balances of Croma gift cards using their API. Generates random card suffixes for the prefix `100134004` and notifies via Telegram when positive balances are found.

## Features

- ✅ Automated random card number generation (9-digit prefix + 7-digit suffix)
- ✅ Balance checking via Croma's official API
- ✅ Real-time Telegram notifications for cards with balance > ₹0
- ✅ Rate limiting to avoid API bans
- ✅ Detailed console logging
- ✅ Graceful error handling

## Prerequisites

- Python 3.7+
- `requests` library (`pip install requests`)

## Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/GC-Checker
cd GC-Checker
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure your credentials**
Edit `config.py` or set environment variables:
```bash
export CROMA_AUTH_TOKEN="your_auth_token_here"
export TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
```

## Configuration

Create `config.py`:
```python
CROMA_AUTH_TOKEN = "your_croma_auth_token"
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"
PREFIX = "100134004"  # Croma gift card prefix
```

## Usage

### Basic Usage (Infinite Loop)
```bash
python checker.py
```
- Press `Ctrl+C` to stop
- Cards with balance are sent to Telegram automatically

### Limited Iterations
```bash
python checker.py --iterations 1000
```

### Usage with Arguments
```bash
usage: checker.py [-h] [--iterations ITERATIONS] [--prefix PREFIX] [--delay DELAY]

optional arguments:
  -h, --help         show this help message and exit
  --iterations ITERATIONS
                      Number of cards to check (default: infinite)
  --prefix PREFIX    Card prefix (default: 100134004)
  --delay DELAY      Delay between requests in seconds (default: 0.5)
```

## Example Output

```
🔄 Starting card checking loop...
PREFIX: 100134004 (9 digits)
Generating random 7-digit suffixes...

[1] Checking card: 1001340041234567... 
-----------------------
Card Number : 1001340041234567
Status      : Active
Balance     : ₹0
-----------------------

[2] Checking card: 1001340049876543... 
✅ Message sent to Telegram
-----------------------
Card Number : 1001340049876543
Status      : Active
Balance     : ₹1250.00
-----------------------
```

## API Details

**Endpoint**: `https://api.croma.com/qwikcilver/v1/transactions`

**TransactionTypeId**: `306` (Balance Check)

**Request Format**:
```json
{
  "TransactionTypeId": 306,
  "InputType": "1",
  "Cards": [{"CardNumber": "1001340041234567"}]
}
```

## Telegram Setup

1. Create a bot via [@BotFather](https://t.me/botfather)
2. Get your `BOT_TOKEN`
3. Send a message to your bot, then get `CHAT_ID` from:
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```

## Rate Limiting

- Default delay: 0.5 seconds between requests
- Adjustable via `--delay` parameter
- Handles HTTP errors gracefully

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `401 Unauthorized` | Check `CROMA_AUTH_TOKEN` |
| `Telegram errors` | Verify `BOT_TOKEN` and `CHAT_ID` |
| `Rate limited` | Increase `--delay` value |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |

## Disclaimer

For legitimate gift card balance verification only. Ensure you have proper authorization for API access. Rate limiting is implemented to respect API terms of service.

---

**⭐ Star this repo if you found it helpful!**  
**🐛 Found a bug? [Open an issue](https://github.com/wtfadi/GC-Checker/issues)**

---

```bash
# Quick start
git clone https://github.com/yourusername/GC-Checker
cd GC-Checker
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your tokens
python checker.py
```

---

**Made with ❤️ for the cybersecurity community**
```

