import json
import os
import threading
import unittest
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen

from fleet_router import RouterHandler, eligible_nodes, load_nodes


class MockNode(BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def do_POST(self):
        n = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(n))
        output = json.dumps({'choices': [{'index':0,'message':{'role':'assistant','content':f"Hello {body['model']}"},'finish_reason':'stop'}]}).encode()
        self.send_response(200)
        self.send_header('Content-Length', str(len(output)))
        self.end_headers()
        self.wfile.write(output)
    def do_GET(self):
        b = json.dumps({'data':[]}).encode()
        self.send_response(200); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)

class TestRouting(unittest.TestCase):
    def test_routing(self):
        cfg={'nodes':[
            {'name':'phone','enabled':True,'tier':'light','priority':1,'supports_tools':False},
            {'name':'tower','enabled':True,'tier':'agent','priority':10,'supports_tools':True},
        ]}
        self.assertEqual([x['name'] for x in eligible_nodes(cfg,'cronos-local',True)],['tower'])
        self.assertEqual([x['name'] for x in eligible_nodes(cfg,'cronos-light',False)],['phone','tower'])
        self.assertEqual([x['name'] for x in eligible_nodes(cfg,'cronos-light',True)],['tower'])
    def test_server(self):
        upstream=ThreadingHTTPServer(('127.0.0.1',0),MockNode)
        threading.Thread(target=upstream.serve_forever, daemon=True).start()
        router=ThreadingHTTPServer(('127.0.0.1',0),RouterHandler)
        router.nodes={'nodes':[{'name':'tower','enabled':True,'tier':'agent','priority':10,
            'url':f'http://127.0.0.1:{upstream.server_port}/v1','model':'qwen3:4b','supports_tools':True}]}
        threading.Thread(target=router.serve_forever, daemon=True).start()
        url=f'http://127.0.0.1:{router.server_port}'
        try:
            res=json.loads(urlopen(url+'/health').read())
            self.assertTrue(res['nodes'][0]['ready'])
            req=Request(url+'/v1/chat/completions',data=json.dumps({'model':'cronos-local','messages':[{'role':'user','content':'hi'}]}).encode(),headers={'Content-Type':'application/json'})
            reply=json.loads(urlopen(req).read())
            self.assertEqual(reply['choices'][0]['message']['content'],'Hello qwen3:4b')
        finally:
            router.shutdown(); router.server_close()
            upstream.shutdown(); upstream.server_close()

if __name__=='__main__': unittest.main()