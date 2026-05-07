import os
from scrapy.cmdline import execute

SPIDER = "pagelist_spider"
LOG_DIRECTORY = f"logs/scraping/{SPIDER}"

# Créer le répertoire de logs s'il n'existe pas
if not os.path.exists(LOG_DIRECTORY):
    print(f"Directory not exist : {os.path.exists(LOG_DIRECTORY)} created.")
    os.makedirs(LOG_DIRECTORY)
else:
    print(f"Directory already exist.")

log_file = os.path.join(LOG_DIRECTORY, f"{SPIDER}.log")

try:
    print(f"Clean the logs in file : {log_file}")
    with open(log_file, 'w', encoding="utf-8") as f:
        pass

    print(f"\nExecute spider : {SPIDER}\n")

    execute([
        'scrapy',
        'crawl',
        SPIDER,
        '-s',
        f'LOG_FILE={log_file}'
    ])
except SystemExit as e:
    print(f"\nError, exit script : {e}\n")

print(f"\nExtraction {SPIDER} finish.\n")
