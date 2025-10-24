#!/bin/bash

# Simple curl-based API tests for Byte in Bottle

BASE_URL="http://localhost:8000"

echo "🍾 Byte in Bottle API Tests"
echo "Powered by bytes. Driven by attitude."
echo ""

# Test 1: Health Check
echo "1️⃣  Testing Health Endpoint..."
curl -s "${BASE_URL}/health" | python3 -m json.tool
echo -e "\n"

# Test 2: Root Endpoint
echo "2️⃣  Testing Root Endpoint..."
curl -s "${BASE_URL}/" | python3 -m json.tool
echo -e "\n"

# Test 3: List Models
echo "3️⃣  Listing Available Models..."
curl -s "${BASE_URL}/models" | python3 -m json.tool
echo -e "\n"

# Test 4: Chat Completion
echo "4️⃣  Testing Chat Endpoint..."
curl -s -X POST "${BASE_URL}/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "messages": [
      {"role": "user", "content": "Say hello in one sentence!"}
    ]
  }' | python3 -m json.tool
echo -e "\n"

# Test 5: Text Generation
echo "5️⃣  Testing Generate Endpoint..."
curl -s -X POST "${BASE_URL}/generate?model=llama3.2&prompt=Hi!" | python3 -m json.tool
echo -e "\n"

echo "✅ All tests completed!"
