import socket
import ssl

HTTP = "http"
HTTPS = "https"

class URL:
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        assert self.scheme in [HTTP, HTTPS]
        
        # Use different port for different scheme
        if self.scheme == HTTP:
            self.port = 80
        elif self.scheme == HTTPS:
            self.port = 443
        
        if '/' not in url:
            url = url + '/'
        self.host, url = url.split('/', 1)
        self.path = '/' + url
        
    def request(self):
        # Make & Connect the socket
        sock = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        sock.connect((self.host, self.port))
        # Need to wrap HTTPS connections with TLS (Transport-Layer Security)
        if self.scheme == HTTPS:
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=self.host)
            
        
        # Format the request
        ## (Read https://browser.engineering/http.html for how this stuff works) 
        request = f"GET {self.path} HTTP/1.0\r\n"
        request += f"Host: {self.host}\r\n"
        request += "\r\n"
        sock.send(request.encode("utf8"))
        
        # Get & read the response
        response = sock.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)
        
        ## Make a map of the response's headers to their respective values
        response_headers = dict()
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()
            
        ## These headers mean the data we're accessing is sent in a weird way
        ## So, if we see them, let's just explode the program for good measure
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers
        content = response.read()
        sock.close()
        
        return content


def show(body):
    in_tag = False
    for character in body:
        if character == "<":
            in_tag = True
        elif character == ">":
            in_tag = False
        elif not in_tag:
            print(character, end="")
            
        

if __name__ == "__main__":
    url = URL("https://browser.engineering")
    response = url.request()
    if response:
        show(response)
    else:
        raise Exception("Response bad! Me explode now!")
    