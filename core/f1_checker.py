import requests
from bs4 import BeautifulSoup

def obter_proxima_corrida_monza():
    """Busca informações da próxima corrida da F1 na web."""
    try:
        url = "https://ergast.com/api/f1/current/next.json"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            race = data['MRData']['RaceTable']['Races'][0]
            nome_gp = race['raceName']
            data_gp = race['date'] # yyyy-mm-dd
            hora_gp = race.get('time', '10:00:00Z')[:5]
            
            partes = data_gp.split('-')
            data_fmt = f"{partes[2]}/{partes[1]}/{partes[0]}"
            
            return f" {nome_gp}", f"{data_fmt} {hora_gp}"
    except Exception:
        pass
    
    # Retorno padrão caso a rede esteja sem internet ou a API falhe
    return "Senhor, verifique a rede e/ou a API, sistema com falhas"