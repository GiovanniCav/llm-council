import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.error

# Configs
BASE_DIR = os.environ.get("ANTIGRAVITY_ROOT", "/Users/giovanni/Antigravity Projects")
RATE_LIMIT_FILE = os.path.join(BASE_DIR, "AIOS", "logs", "n8n_rate_limits.json")
MAX_REQUESTS_PER_HOUR = 5

def load_rate_limits():
    """Load the state of rate limits from the AIOS logs."""
    if not os.path.exists(RATE_LIMIT_FILE):
        return {}
    with open(RATE_LIMIT_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_rate_limits(limits):
    """Save the updated rate limits."""
    os.makedirs(os.path.dirname(RATE_LIMIT_FILE), exist_ok=True)
    with open(RATE_LIMIT_FILE, 'w') as f:
        json.dump(limits, f, indent=2)

def check_rate_limit(webhook_name):
    """Check if the webhook has exceeded its hourly quota (circuit breaker)."""
    limits = load_rate_limits()
    now = time.time()
    
    # Initialize if missing
    if webhook_name not in limits:
        limits[webhook_name] = []
        
    # Clean up timestamps older than 1 hour
    limits[webhook_name] = [ts for ts in limits[webhook_name] if now - ts < 3600]
    
    if len(limits[webhook_name]) >= MAX_REQUESTS_PER_HOUR:
        return False, limits
        
    # Log the new request
    limits[webhook_name].append(now)
    return True, limits

def trigger_webhook(webhook_name, payload):
    """Safely trigger an n8n webhook."""
    # Air-gapped URL retrieval (Risk #4 Mitigation)
    # The agent does not know the actual URL, it just provides the generic name.
    # We look it up in the environment variable.
    env_var_name = f"N8N_WEBHOOK_{webhook_name.upper().replace('-', '_')}"
    webhook_url = os.environ.get(env_var_name)
    
    if not webhook_url:
        print(f"ERROR: Webhook '{webhook_name}' is not configured in the environment.")
        print(f"Please ensure {env_var_name} is set in the secure .env file.")
        sys.exit(1)
        
    allowed, new_limits = check_rate_limit(webhook_name)
    if not allowed:
        print(f"ERROR: Rate limit exceeded for webhook '{webhook_name}'.")
        print(f"Maximum allowed is {MAX_REQUESTS_PER_HOUR} requests per hour.")
        print("Circuit breaker activated. Please queue this action for human approval or wait.")
        sys.exit(1)
        
    print(f"Triggering automation via {webhook_name}...")
    
    # Fire the webhook
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(webhook_url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')
            print("✅ Webhook triggered successfully.")
            save_rate_limits(new_limits)
            return result
    except urllib.error.URLError as e:
        print(f"❌ Webhook trigger failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AIOS Automation Bridge: Safely trigger n8n webhooks.")
    parser.add_argument("--webhook", required=True, help="The generic name of the webhook to trigger (e.g., 'slack-notify').")
    parser.add_argument("--payload", required=True, help="Path to a JSON file containing the payload payload.")
    args = parser.parse_args()
    
    if not os.path.exists(args.payload):
        print(f"ERROR: Payload file '{args.payload}' not found.")
        sys.exit(1)
        
    with open(args.payload, 'r') as f:
        try:
            payload_data = json.load(f)
        except json.JSONDecodeError:
            print(f"ERROR: Payload file '{args.payload}' is not valid JSON.")
            sys.exit(1)
            
    trigger_webhook(args.webhook, payload_data)
