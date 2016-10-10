# Orka

##Projeto de TFG 2016 
###**UNIFEI** - Engenharia da Computação 


----------------------------------
Branches | Conteúdo
-------- | --------
Master | Versão Estável
Develop | Versão em Desenvolvimento
Monografia | Edição dos arquivos em LaTeX
Revisao_Bibliografica | Pesquisa e embasamento teórico
Workshop | Apresentação e Documentação
Eng_Soft | Modelagem e Estruturação




## Instalação Dev:

  - Criar ambiente virtual
  
  > Necessário pacote python-virtualenv

  ```
  git clone https://rlimaeco@bitbucket.org/tfgorka/orka.git
  cd orka  
  virtualenv venv
  . venv/bin/activate
  pip install -r requirements.txt
  ```
  
  > Caso encontre algum erro na instalação do Pillow , no Ubuntu instalar os seguintes pacotes:
  
  ```
  sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
  sudo apt-get build-dep python-imaging
  ```
  

  - Executar servidor
  
  ```
  fabmanager run
  ```
  
  - Abrir navegador em localhost:8080


## Configurações Finais
   
  * Criar usuário administrador

  ```
  fabmanager create-admin
  ```
  Complete os dados e isto irá criar o usuário administrador

   * Internacionalização
  
  Execute ao menos uma vez este comando para sincronizar os idiomas
  
  ```
  fabmanager babel-compile
  ```

## Executar Redis

   * Para o funcionamento do Celery é necessário iniciar o redis
   
   ```
   ./run-redis.sh
   ```
   
   * Iniciar pelo menos um worker com:
   
   ```
   cd orka
   celery worker --app=app.celery --loglevel=DEBUG
   ```
   
## Let's code !
