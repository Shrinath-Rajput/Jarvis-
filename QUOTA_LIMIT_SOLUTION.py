#!/usr/bin/env python3
"""
SOLUTION TO GEMINI QUOTA ISSUE:

The Gemini API key has hit its free-tier quota limit (429 error).

OPTIONS:

1. GET A NEW GEMINI API KEY (Free)
   - Go to https://ai.google.dev/
   - Create a new API key with a different Google account
   - Set it in your environment:
     $env:GEMINI_API_KEY="your-new-key"

2. USE CLAUDE INSTEAD
   - If you have an Anthropic API key, set it:
     $env:ANTHROPIC_API_KEY="your-anthropic-key"
   - The app will use Claude automatically

3. WAIT FOR QUOTA RESET
   - Gemini free tier quotas reset after some time
   - Usually daily or hourly depending on quota type

4. UPGRADE YOUR ACCOUNT
   - Go to https://ai.google.dev/billing
   - Add a payment method for higher quotas

CURRENT STATUS:
- Gemini 2.0 Flash: QUOTA EXCEEDED (429 error)
- Claude: NOT CONFIGURED (no ANTHROPIC_API_KEY)
- Fallback planner: Will be added in next update

TO TEST:
$env:GEMINI_API_KEY="your-new-key"
python Backend/test_planner_quick.py

"""

print(__doc__)

# Show quota limit message
print("\n" + "="*70)
print("QUOTA LIMIT REACHED")
print("="*70)
print("\nThe Gemini API key has reached its quota limit.")
print("See above for solutions.")
print("\nTo use JARVIS immediately with a workaround:")
print("1. Get a new Gemini API key from https://ai.google.dev/")
print("2. Set it: $env:GEMINI_API_KEY='your-key'")
print("3. Restart the app")
print("\nOr use Claude if you have an Anthropic API key.")
print("="*70 + "\n")
