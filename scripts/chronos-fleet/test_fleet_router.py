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

    def test_failover_if_first_node_unreachable(self):
        upstream=ThreadingHTTPServer(('127.0.0.1',0),MockNode)
        threading.Thread(target=upstream.serve_forever, daemon=True).start()
        # Allocate and immediately release a port: deliberately unreachable.
        import socket
        s=socket.socket(); s.bind(('127.0.0.1',0)); dead_port=s.getsockname()[1]; s.close()
        router=ThreadingHTTPServer(('127.0.0.1',0),RouterHandler)
        router.nodes={'nodes':[
            {'name':'dead','enabled':True,'tier':'agent','priority':1,'timeout':1,
             'url':f'http://127.0.0.1:{dead_port}/v1','model':'dead-model','supports_tools':True},
            {'name':'backup','enabled':True,'tier':'agent','priority':2,'timeout':2,
             'url':f'http://127.0.0.1:{upstream.server_port}/v1','model':'backup-model','supports_tools':True}
        ]}
        threading.Thread(target=router.serve_forever, daemon=True).start()
        try:
            url=f'http://127.0.0.1:{router.server_port}/v1/chat/completions'
            payload={'model':'cronos-local','messages':[{'role':'user','content':'hi'}]}
            req=Request(url,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
            with urlopen(req,timeout=5) as res:
                self.assertEqual(res.headers['X-Cronos-Node'],'backup')
                self.assertEqual(json.loads(res.read())['choices'][0]['message']['content'],'Hello backup-model')
        finally:
            router.shutdown();router.server_close();upstream.shutdown();upstream.server_close()

    def test_tools_without_agent_node_return_503(self):
        from urllib.error import HTTPError
        router=ThreadingHTTPServer(('127.0.0.1',0),RouterHandler)
        router.nodes={'nodes':[{'name':'phone','enabled':True,'tier':'light','priority':1,
            'url':'http://127.0.0.1:9999/v1','model':'tiny','supports_tools':False}]}
        threading.Thread(target=router.serve_forever,daemon=True).start()
        try:
            url=f'http://127.0.0.1:{router.server_port}/v1/chat/completions'
            payload={'model':'cronos-light','messages':[{'role':'user','content':'hi'}],
                     'tools':[{'type':'function','function':{'name':'do','parameters':{'type':'object'}}}]}
            req=Request(url,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
            with self.assertRaises(HTTPError) as cm: urlopen(req,timeout=5)
            self.assertEqual(cm.exception.code,503)
        finally: router.shutdown();router.server_close()


if __name__=='__main__': unittest.main()