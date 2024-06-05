import requests as r
import time as t
import smtplib
import settings
import pokemon_data
print("Initializing" + '\n')
last_spawn=""

def Spawn_Alert(msg, to):
  user = to
  password = settings.password
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(user, password)
  server.sendmail(user, to, msg)
  server.quit()

a_tier_alerts=settings.a_tier_alerts
s_tier_alerts=settings.s_tier_alerts
starter_alerts=settings.starter_alerts
pokemon =settings.pokemon
types=settings.types

if a_tier_alerts is True:
  a_tiers=pokemon_data.a_tiers
  pokemon.extend(a_tiers)
if s_tier_alerts is True:
  s_tiers=pokemon_data.s_tiers
  pokemon.extend(s_tiers)
if starter_alerts is True:
  starters=pokemon_data.starters
  pokemon.extend(starters)

while True:
  Alert=False
  spawn_url = "https://poketwitch.bframework.de/info/events/last_spawn/"
  latest_spawn = r.get(spawn_url).json()
  latest_spawn_timestamp = latest_spawn["event_time"]
  if last_spawn == latest_spawn_timestamp:
    t.sleep(latest_spawn["next_spawn"]+1)
  else:
    last_spawn = latest_spawn_timestamp
    pokemon_id = latest_spawn["order"]
    pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/'
    pokemon_data = r.get(pokemon_url).json()
    typing = [type['type']['name'] for type in pokemon_data['types']]
    if pokemon_id in pokemon:
      Alert=True
    for type in typing:
      if type in types:
        Alert=True
    if Alert is True:
      name = pokemon_data['name'].title()
      user=settings.email
      Spawn_Alert(f'{name} Spawn',user)
      print(f"Sent Alert for {name} spawn")
    t.sleep(latest_spawn["next_spawn"])
