import json
import numpy as np

def make_pokemat(fname='pokeml.json'):
  with open(fname) as file:
    pokedata = json.load(file)

  pokedex = pokedata['pokedex']
  pokelist = list(pokedex.keys())
  movelist = pokedata['moves']
  abilitylist = pokedata['abilities']
  typelist = pokedata['types']  

  hp_stats = sorted(list(set([pokedex[p]['stats']['hp'] for p in pokelist])))
  atk_stats = sorted(list(set([pokedex[p]['stats']['atk'] for p in pokelist])))
  def_stats = sorted(list(set([pokedex[p]['stats']['def'] for p in pokelist])))
  spa_stats = sorted(list(set([pokedex[p]['stats']['spa'] for p in pokelist])))
  spd_stats = sorted(list(set([pokedex[p]['stats']['spd'] for p in pokelist])))
  spe_stats = sorted(list(set([pokedex[p]['stats']['spe'] for p in pokelist])))

  pokemat = np.zeros((len(pokelist), len(typelist) + 1 + 6 + len(hp_stats) + len(atk_stats) + len(def_stats) \
        + len(spa_stats) + len(spd_stats) + len(spe_stats) +  len(abilitylist) + len(movelist)))

  for i,p in enumerate(pokelist):
    for t in pokedex[p]['types']:
        pokemat[i,typelist.index(t)] = 1
    if pokedex[p]['hasEvo'] > 0:
        pokemat[i,18] = 1
    pokemat[i,19] = pokedex[p]['stats']['hp']
    pokemat[i,20] = pokedex[p]['stats']['atk']
    pokemat[i,21] = pokedex[p]['stats']['def']
    pokemat[i,22] = pokedex[p]['stats']['spa']
    pokemat[i,23] = pokedex[p]['stats']['spd']
    pokemat[i,24] = pokedex[p]['stats']['spe']
    idx = 25
    pokemat[i,idx+hp_stats.index(pokedex[p]['stats']['hp'])] = 1
    idx += len(hp_stats)
    pokemat[i,idx+atk_stats.index(pokedex[p]['stats']['atk'])] = 1
    idx += len(atk_stats)
    pokemat[i,idx+def_stats.index(pokedex[p]['stats']['def'])] = 1
    idx += len(def_stats)
    pokemat[i,idx+spa_stats.index(pokedex[p]['stats']['spa'])] = 1
    idx += len(spa_stats)
    pokemat[i,idx+spd_stats.index(pokedex[p]['stats']['spd'])] = 1
    idx += len(spd_stats)
    pokemat[i,idx+spe_stats.index(pokedex[p]['stats']['spe'])] = 1
    idx += len(spe_stats)
    for a in pokedex[p]['abilities']:
        pokemat[i,idx+abilitylist.index(a)] = 1
    idx += len(abilitylist)
    for m in pokedex[p]['learnset']:
        pokemat[i,idx+movelist.index(m)] = 1
        
  pokemat[pokelist.index('silvally'),:18] = 1/18        

  index_lookup = {'Type: ' + t: i for i,t in enumerate(typelist)}
  index_lookup['Has Evo'] = 18
  index_lookup['HP'] = 19
  index_lookup['Atk'] = 20
  index_lookup['Def'] = 21
  index_lookup['SpA'] = 22
  index_lookup['SpD'] = 23
  index_lookup['Spe'] = 24
  idx = 25
  for i,s in enumerate(hp_stats):
      index_lookup['HP %d'%s] = idx + i
  idx += len(hp_stats)
  for i,s in enumerate(atk_stats):
      index_lookup['Atk %d'%s] = idx + i
  idx += len(atk_stats)
  for i,s in enumerate(def_stats):
      index_lookup['Def %d'%s] = idx + i
  idx += len(def_stats)
  for i,s in enumerate(spa_stats):
      index_lookup['SpA %d'%s] = idx + i
  idx += len(spa_stats)
  for i,s in enumerate(spd_stats):
      index_lookup['SpD %d'%s] = idx + i
  idx += len(spd_stats)
  for i,s in enumerate(spe_stats):
      index_lookup['Spe %d'%s] = idx + i
  idx += len(spe_stats)
  for i,a in enumerate(abilitylist):
      index_lookup['Ability: ' + a] = idx + i
  idx += len(abilitylist)
  for i,m in enumerate(movelist):
      index_lookup['Move: ' + m] = idx + i
  index_name = [''] * len(index_lookup)
  for m,i in index_lookup.items():
      index_name[i] = m

  return pokedex, pokelist, typelist, movelist, abilitylist, pokemat, index_lookup, index_name
