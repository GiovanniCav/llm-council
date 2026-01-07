#!/usr/bin/env python3
import httpx
import json
import uuid

def verify_contract():
    url = "http://localhost:8010/api/gate"
    payload = {
        "project": "contract_verification",
        "security_mode": "standard",
        "user_prompt": "Test contract",
        "draft_output": "Stable output",
        "evidence": {"citations": [], "retrieved_chunks": []}
    }
    
    print(f"Testing {url}...")
    try:
        with httpx.Client() as client:
            response = client.post(url, json=payload, timeout=180.0)
            if response.status_code != 200:
                print(f"FAIL: Request failed with {response.status_code}")
                print(f"Error detail: {response.text}")
                return False
            data = response.json()
        
        required_fields = [
            "gate_passed",
            "final_synthesis",
            "issues_found",
            "required_fixes",
            "deliberation_history",
            "consensus_scores",
            "trace_id",
            "log_ref"
        ]
        
        missing = [field for field in required_fields if field not in data]
        
        if missing:
            print(f"FAIL: Missing fields: {missing}")
            return False
            
        print("Response received:")
        print(json.dumps(data, indent=2))
        
        if data["trace_id"] == data["log_ref"] and len(data["trace_id"]) > 0:
            print("PASS: Contract verified.")
            return True
        else:
            print("FAIL: trace_id and log_ref mismatch or empty.")
            return False
            
    except Exception as e:
        if hasattr(e, 'response') and e.response:
            print(f"FAIL: Request failed with {e.response.status_code}")
            print(f"Error detail: {e.response.text}")
        else:
            print(f"FAIL: Request failed: {e}")
        return False

if __name__ == "__main__":
    if verify_contract():
        exit(0)
    else:
        exit(1)
