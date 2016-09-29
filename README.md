# orka
Projeto de TCC 2016 Engenharia da Computação - UNIFEI

Branches | Conteúdo
-------- | --------
Master | Default code tree
Monografia | Edição dos arquivos em LaTeX


## Instalação Dev:

  - Criar ambiente virtual
  
  > Necessário pacote python-virtualenv

  ```bash
  git clone https://github.com/diogoamatos/orka.git
  cd orka  
  virtualenv venv
  . venv/bin/activate
  pip install -r requirements.txt
  ```
  
  > Caso encontre algum erro na instalação do Pillow , no Ubuntu instalar os seguintes pacotes:
  
  ```bash
  sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
  sudo apt-get build-dep python-imaging
  ```
  

  - Executar servidor
  
  ```bash
  fabmanager run
  ```
  
  - Abrir navegador em localhost:8080


## Configurações Finais
   
  > Criar Admin

  ```bash
  fabmanager create-admin
  ```
  Complete os dados e isto irá criar o usuário administrador

  > Internacionalização
  
  Execute ao menos uma vez este comando para sincronizar os idiomas
  
  ```bash
  fabmanager babel-compile
  ```

## Let's code !
