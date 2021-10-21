gsutil cp "gs://${DEPLOYMENT_BUCKET}/${WEBAPP_RUNTIME_SA_KEY}" ./privatekey.json
gsutil cp "gs://${DEPLOYMENT_BUCKET}/${SITEMAP_XML_FILE}" ./sitemap.xml
gsutil cp "gs://${DEPLOYMENT_BUCKET}/${SITEMAP_LIST_FILE}" ./urllist.txt