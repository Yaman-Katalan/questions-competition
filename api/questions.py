# api_url: https://opentdb.com/api.php?amount=10
# vercel_link: https://questions-competition-pi.vercel.app/


import requests
from http.server import BaseHTTPRequestHandler
from urllib import parse

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):

        my_path = self.path
        url_component = parse.urlsplit(my_path)
        query_string_list = parse.parse_qsl(url_component.query)
        my_dict = dict(query_string_list)


        extra_info = ""
        url = "https://opentdb.com/api.php?amount=0"


        if "amount" in my_dict and "category" in my_dict:
            url = f"https://opentdb.com/api.php?amount={my_dict['amount']}&category={my_dict['category']}"
        elif "amount" in my_dict:
            url = f"https://opentdb.com/api.php?amount={my_dict['amount']}"
        elif "category" in my_dict:
            url = f"https://opentdb.com/api.php?amount=10&category={my_dict['category']}"


        my_request = requests.get(url)
        request_data = my_request.json()
        request_data = request_data["results"]


        self.send_response(200)
        self.send_header('Content-type', 'text/html') #text/plain
        self.end_headers()
        

        if len(request_data) > 49:
            extra_info = f"Maximum number of results this API can give is: {len(request_data)}"
            self.wfile.write(f"<p>{extra_info}</p><hr/>".encode())
        index = 1
        if request_data:
            for Q_A in request_data:
                self.wfile.write(f"<h3>Q{index}: {Q_A["question"]}</h3><p>Correct Answer: {Q_A["correct_answer"]}</p><h3>Category: {Q_A["category"]}</h3><hr/>".encode())
                index += 1
        else:
            self.wfile.write("<h1>Wrong query!!!</h1>".encode())

        return