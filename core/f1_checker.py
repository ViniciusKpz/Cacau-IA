import requests
from datetime import datetime
from dateutil import parser
import zoneinfo

def obter_proxima_corrida():
    """Busca a próxima corrida da F1 de forma totalmente dinâmica via API."""
    endpoints = [
        "https://api.jolpi.ca/ergast/f1/current/next.json",
        "https://ergast.com/api/f1/current/next.json"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'}

    for url in endpoints:
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                races = data.get('MRData', {}).get('RaceTable', {}).get('Races', [])
                
                if races:
                    race = races[0]
                    nome_gp = race.get('raceName', 'GP de F1')
                    data_str = race.get('date')
                    hora_str = race.get('time', '13:00:00Z')

                    # Parse completo de Data e Hora com Fuso Horário de Brasília
                    dt_utc = parser.parse(f"{data_str}T{hora_str}")
                    fuso_br = zoneinfo.ZoneInfo("America/Sao_Paulo")
                    dt_local = dt_utc.astimezone(fuso_br)

                    data_fmt = dt_local.strftime("%d/%m/%Y")
                    hora_fmt = dt_local.strftime("%H:%M")

                    return f"Próxima Corrida: {nome_gp}", f"{data_fmt} {hora_fmt}"
        except Exception:
            continue

    # Caso a conexão falhe, retorna um aviso genérico sem travar o código com dados antigos
    return "Próxima Corrida: F1 (Sem conexão)", "Verifique a rede"