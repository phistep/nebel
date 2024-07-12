curl -X POST \
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     -H "x-goog-user-project: nebel-429020" \
     -H "Content-Type: application/json; charset=utf-8" \
     -d @request.json \
     "https://vision.googleapis.com/v1/files:asyncBatchAnnotate"