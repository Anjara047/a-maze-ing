with open("config.txt", "r") as f:
    l_configs = [l.strip()
                 for l in f if l != l.capitalize() and not l.startswith("#")]

# Gestion d'erreur: si width/height, tsy afaka castena ho int
# mettre configs comme configs par defaut si jamais on fournit des valeurs
# invalides dans config.txt
configs = {
    'WIDTH': 20,
    'HEIGHT': 20,
    'ENTRY': '0,0',
    'EXIT': '',
    'OUTPUT_FILE': 'maze.txt',
    'PERFECT': True
}
configs['EXIT'] = (str(configs['WIDTH']) + ',' + str(configs['HEIGHT'])),
for l_config in l_configs:
    config = l_config.split('=')
    if config[0] == 'WIDTH' or config[0] == 'HEIGHT':
        configs[config[0]] = int(config[1])
    else:
        configs[config[0]] = config[1]
