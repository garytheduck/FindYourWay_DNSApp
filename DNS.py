from http.server import BaseHTTPRequestHandler, HTTPServer
import dns.resolver
import geocoder
hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        self.wfile.write(bytes("<html><head><title>LOCATIE IP</title></head>", "utf-8"))
        self.wfile.write(bytes("<body background=""https://cdn.mos.cms.futurecdn.net/6Kr3EWY2GKe738gpELRSAX.jpg"">", "utf-8"))
        self.wfile.write(bytes("<form action=""http://localhost:8080/"">", "utf-8"))
        self.wfile.write(bytes("<label style=""color:#DFFF00"" for=""adress"">Adresa: </label>", "utf-8"))
        self.wfile.write(bytes("<input %s id=""adress"" name=""adress""><br><br>" % self.path, "utf-8"))
        self.wfile.write(bytes("<input type=""submit"" value=""Submit"">", "utf-8"))
        self.wfile.write(bytes("</form>", "utf-8"))
        verifica = 0 # :)
        string = self.path[1:] 
        if string != "" and string != "favicon.ico":
            adresa = string.split("=",1)[1]
            try:
                result = dns.resolver.resolve(adresa, 'A')
            except dns.resolver.NXDOMAIN:
                self.wfile.write(bytes("<p style=""color:#DFFF00""> Adresa introdusa nu exista!</p>" , "utf-8"))
                verifica = verifica + 1
            except dns.resolver.NoNameservers:
                self.wfile.write(bytes("<p style=""color:#DFFF00""> Adresa introdusa nu exista!</p>" , "utf-8"))
                verifica = verifica + 1
            except dns.resolver.NoAnswer:
                self.wfile.write(bytes("<p style=""color:#DFFF00""> Inca nu ati introdus o adresa!</p>" , "utf-8"))
                verifica = verifica + 1
            if verifica==0:
                self.wfile.write(bytes("<p style=""color:#DFFF00""> Adresa introdusa: %s</p>" % self.path[9:], "utf-8"))
            for ipval in result:
                self.wfile.write(bytes("<p style=""color:#DFFF00""> IP : %s</p>" % ipval.to_text(), "utf-8"))
            ipval = result[0]
            g = geocoder.ip(ipval.to_text())
            coordonate = g.latlng
            self.wfile.write(bytes("<p style=""color:#DFFF00""> Coordonate server : %s</p>" % coordonate, "utf-8"))
            link = "<iframe width=\"1000\" height=\"500\" frameborder=\"0\" style=\"border:0\" src=\"https://www.google.com/maps/embed/v1/place?key=AIzaSyCP2Rn6dZ9OKtmx4Au2c74hYRdT3r1HNEs&q={0},{1}\" allowfullscreen> </iframe>"
            link = link.format(coordonate[0], coordonate[1])
            print(link)
            self.wfile.write(bytes(link, "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
    
    
    
    
    
    
    

