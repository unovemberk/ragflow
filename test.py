Invoke-WebRequest -Uri "http://192.168.29.130:8000/api/v1/retrieve" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{
    "knowledge_base_id": "22aa3e56b2d611f09af1e666fc2e801e",
    "query": "user_test1的ID号",
    "top_k": 3
  }'
