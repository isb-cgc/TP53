gsutil cp "gs://${DEPLOYMENT_BUCKET}/${WEBAPP_RUNTIME_SA_KEY}" ./privatekey.json
gsutil cp "gs://${DEPLOYMENT_BUCKET}/client_secret.json" ./client_secret.json
gsutil cp "gs://${DEPLOYMENT_BUCKET}/sitemap.xml" ./sitemap.xml
gsutil cp "gs://${DEPLOYMENT_BUCKET}/urllist.txt" ./urllist.txt
gsutil cp "gs://${DEPLOYMENT_BUCKET}/app.yaml" ./app.yaml