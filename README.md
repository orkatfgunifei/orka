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
   
  * Criar usuário administrador

  ```bash
  fabmanager create-admin
  ```
  Complete os dados e isto irá criar o usuário administrador

   * Internacionalização
  
  Execute ao menos uma vez este comando para sincronizar os idiomas
  
  ```bash
  fabmanager babel-compile
  ```

## Let's code !


## TFG Infos:
Grupo no Facebook:
https://www.facebook.com/groups/1516143168644693/

Seguem as datas importantes para o desenvolvimento do Trabalho Final de Graduação do curso de Engenharia da Computação da Universidade Federal de Itajubá para os alunos que pretendem defender suas monografias no ano de 2016:

----------------------------------
Etapa    | Prazo Máximo
-------- | --------
Entrega da Proposta de Trabalho (Impressa. Baixar modelo em Modelos) |  15/08/2016 (PRORROGADO)
Entrega da Revisão Bibliográfica (por e-mail edmarmo@unifei.edu.br) |  05/09
Workshop - Apresentação de Seminários | 07/10
Entrega da Monografia - Primeira Versão | 07/11
Defesa do Trabalho | 16-18/11
Entrega da Monografia Versão Corrigida | Defesa em Novembro: 30/11


### Algumas observações Importantes:
Os trabalhos devem ser desenvolvidos em grupos de até TRÊS alunos. Um aluno de outros cursos pode fazer parte de um grupo. No entanto, deve ser apresentada ao coordenador de TFG da ECO uma carta do orientador de TFG do curso do aluno, demonstrando que está de acordo. Além disso, o aluno deverá se sujeitar a todos os passos e avaliações do TFG de ECO.

####Cada fase receberá uma nota proporcional à sua importância:
- Revisão bibliográfica: 15 pontos
- Workshop: 15 pontos
- Parecer do orientador: 10 pontos
- Monografia e defesa: 60 pontos

Os documentos devem ser, OBRIGATORIAMENTE, escritos utilizando LaTeX, exceto pela apresentação do workshop, que pode ser feita com qualquer editor de apresentações e exportada em PDF.

### Contato com a Coordenação:
Coordenador TFG-ECO: Prof. Dr. Edmilson Marmo Moreira
- E-mail: edmarmo@unifei.edu.br
- Sala: I 4.2.11 (Segundo andar do bloco da elétrica, bloco novo)

### Material de Apoio
    https://sites.google.com/site/tfgeco/material-de-apoio