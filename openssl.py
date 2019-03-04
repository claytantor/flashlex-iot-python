try:
  import ssl
  version = ssl.OPENSSL_VERSION
  print("true")
except:
  print("false")
