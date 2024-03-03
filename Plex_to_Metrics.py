import prometheus_client
from prometheus_client import start_http_server, Gauge
import requests
import time
from dotenv import load_dotenv
import os
from os.path import join, dirname

prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)

def fetch_plex_sessions(base_url,port,token):
    url = f"http://{base_url}:{port}/status/sessions"

    payload={}
    headers = {
      'Accept': 'application/json',
      'X-Plex-Token': token
    }

    api_response = requests.request("GET", url, headers=headers, data=payload)

    json_obj = api_response.json()

    output_data = []

    try:
        for item in json_obj['MediaContainer']['Metadata']:
            output_obj = {}
            output_obj['User'] = item['User']['title']
            output_obj['ip_address'] = item['Player']['remotePublicAddress']
            output_obj['device'] = item['Player']['device']
            output_obj['bandwith'] = item['Session']['bandwidth']
            output_obj['watching'] = item['title']
            output_data.append(output_obj)
    except KeyError:
        pass
        #no data returned form api endpoint

    return output_data


def return_gauge_objs(data,metric):
    collect = []
    for record in data:
        collect.append(metric.labels(**record).set("1"))
    return collect




if __name__ == '__main__':
    dotenv_path = join(dirname(__file__),'config', '.env')
    load_dotenv(dotenv_path)
    metric = Gauge("Plex_Session_User","Displays labels about plex users and their session", ['User','ip_address','device','bandwith','watching'])
    start_http_server(8989)

    while True:
        metric.clear()
        session_data = fetch_plex_sessions(os.getenv('PLEX_URL'),os.getenv('PLEX_PORT'),os.getenv('PLEX_API_TOKEN'))
        return_gauge_objs(session_data,metric)
        time.sleep(60 * 5)
