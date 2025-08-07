
DOWNLOAD = {"USERNAME" : "","PASSWORD" : "","URL" : "https://kartmjoso.net/Kartarkiv/"}
UPLOAD = {"USERNAME" : "","PASSWORD" : "","URL" : "https://doma.huoghei.com/"}


MAPS_PATH = "maps"

#Dont touch the rest if not needed

DOWNLOAD_WSDL_WEBSERVICE_URL = DOWNLOAD["URL"] + "webservice.php?wsdl"
UPLOAD_WSDL_WEBSERVICE_URL = UPLOAD["URL"] + "webservice.php?wsdl"

DOWNLOAD_MAPS_URL = DOWNLOAD["URL"] + "show_map.php?user=" + DOWNLOAD["USERNAME"] + "&map="

# Partial file upload size in bytes
CHUNK_SIZE = 512 * 1024
RATE_LIMIT = 30  # seconds between requests to avoid server issues



