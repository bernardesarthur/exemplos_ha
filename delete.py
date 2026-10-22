import requests
import urllib.parse

COOKIE = """cole o cookie aqui"""
CSRF = "cole o csrf aqui"
HOST = "https://alexa.amazon.com.br"

HEADERS = {
    "Cookie": COOKIE,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

def listar():
    r = requests.post(f"{HOST}/nexus/v1/graphql", headers=HEADERS, json={
        "query": "query { endpoints { items { friendlyName legacyAppliance { applianceId } } } }"
    })
    return r.json()["data"]["endpoints"]["items"]

def deletar(aid):
    url = f"{HOST}/api/phoenix/appliance/{urllib.parse.quote(aid, safe='')}"
    return requests.delete(url, headers={**HEADERS, "csrf": CSRF}).status_code

def rodada():
    devices = [d for d in listar()
               if d.get("legacyAppliance") and d["legacyAppliance"].get("applianceId")]
    total = len(devices)
    print(f"=== Passando por {total} dispositivos ===")
    for i, d in enumerate(devices, 1):
        status = deletar(d["legacyAppliance"]["applianceId"])
        print(f"[{i}/{total}] {status} {d['friendlyName'][:50]}")
    sobrou = [d for d in listar()
              if d.get("legacyAppliance") and d["legacyAppliance"].get("applianceId")]
    print(f"Resultado da rodada: {total} -> {len(sobrou)} restantes")
    return len(sobrou)

if __name__ == "__main__":
    n = rodada()          # primeira rodada
    rodada_num = 2
    while n > 0 and rodada_num <= 10:
        print(f"=== Rodada {rodada_num} ===")
        n = rodada()      # a Amazon às vezes responde 200 sem apagar; repita até zerar
        rodada_num += 1
    print("Fim. Restantes:", n)
