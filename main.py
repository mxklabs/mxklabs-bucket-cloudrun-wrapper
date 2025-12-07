import time
import sys
import os

from google.cloud import storage
from http.server import BaseHTTPRequestHandler, HTTPServer

# Configuration from environment variables.
port        = int(os.getenv("PORT", 8080))
hostname    = os.getenv("HOSTNAME", "0.0.0.0")
bucket_name = os.getenv("BUCKET_NAME")
home_page   = os.getenv("HOME_PAGE", "/index.html")

# Globale variable managing the Cloud Bucket access.
storage_client = storage.Client()

# NOTE: Authentication is handled automagically when running on Cloud Run.

class WrapperFileNotFoundError(Exception):
  pass

class WrapperServer(BaseHTTPRequestHandler):

  def do_GET(self):
    """ Respond to HTTP request. """
    try:
      path = self.path

      if path == '/':
        # Default to home page for root.
        path = home_page

      if path.startswith('/'):
        # Remove forward slash.
        path = path[1:]

      if path.endswith('/'):
        # Add index.html.
        path = path[:-1] + home_page

      # Get the corresponding file from the Cloud Bucket.
      content_type, result = self.get_file_from_bucket(bucket_name, path)

      # Send HTTP 200 response with content.
      self.send_response(200)
      self.send_header("Content-type", content_type)
      self.end_headers()
      self.wfile.write(result)

    except WrapperFileNotFoundError:
      # File not found, send HTTP 404 with a message.
      self.send_response(404)
      self.send_header("Content-type", "text/html")
      self.end_headers()

      self.wfile.write(bytes("<html><head><title>File not found - HTTP 404</title></head>", "utf-8"))
      self.wfile.write(bytes("<body>", "utf-8"))
      self.wfile.write(bytes("<p>There is no file called '%s' on this server.</p>" % self.path, "utf-8"))
      self.wfile.write(bytes("</body></html>", "utf-8"))

  def get_file_from_bucket(self, bucket_name, source_blob_name):
    """ Return a tuple (bytes, mime-type) for a given file in a bucket, else raise exception. """
    bucket = storage_client.bucket(bucket_name)

    if not bucket.exists():
      print(f"ERROR: Unable to find bucket with name '{bucket_name}'")
      sys.exit(1)

    blob = bucket.blob(source_blob_name)

    if not blob.exists():
      raise WrapperFileNotFoundError(f"Unable to find resource called '{source_blob_name}' in bucket {bucket_name}")

    blob_bytes = blob.download_as_bytes()
    return blob.content_type, blob_bytes

if __name__ == "__main__":

  if bucket_name is None:
    print("ERROR: Environment variable BUCKET_NAME was not set")
    sys.exit(1)

  webServer = HTTPServer((hostname, port), WrapperServer)
  print(f"Server started http://{hostname}:{port}")

  try:
    webServer.serve_forever()
  except KeyboardInterrupt:
    pass

  webServer.server_close()
  print("Server stopped.")