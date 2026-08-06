# ASCII/banner.py

BANNER_COMPLETO = """\033[31m
 ███   ███   ███   ███  █   █    ███  ███    
█ ░░░ █ ░░█ █ ░░░ █ ░░█ █░  █░    █░░█ ░░█   
█░ ░░░█████░█░ ░░░█████░█░░ █░░   █░░█████░  
█░░   █░░░█░█░░   █░░░█░█░░ █░░   █░░█░░░█░░ 
 ███  █░░░█░░███  █░░░█░░███ ░░  ███░█░░░█░░ 
  ░░░  ░░  ░░ ░░░  ░░  ░░ ░░░ ░   ░░░ ░░  ░░ 
   ░░░  ░   ░  ░░░  ░   ░  ░░░     ░░░ ░   ░ 
\033[0m"""

def exibir_banner_principal():
    print(BANNER_COMPLETO)

def exibir_banner_manual():
    print(BANNER_MINI)