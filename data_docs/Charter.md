# Project Charter

## Business background

O projeto será pensado para escolas e faculdades que queiram personalizar os estudos de seus alunos através de uma trilha individual gerada por IA.

## Scope
* Um modelo de machine learning que será alimentado com as notas dos alunos e retornará o que eles precisam focar para melhorar seus estudos.
* Os alunos irão receber um arquivo pdf contendo links e informações úteis para as matérias que tem mais dificuldade.

## Personnel
* Who are on this project:
	* AI Learn:
		* Project lead - Gustavo Carneiro Alves
		* Data scientist(s) - Gustavo Carneiro Alves
	* Client:
		* Data administrator - Escolas e Faculdades
		* Business contact - Diretores e Reitores
	
## Metrics
* What are the qualitative objectives? (e.g. reduce user churn)
Ajudar de forma masi íntima os estudos das pessoas.
* What is a quantifiable metric  (e.g. reduce the fraction of users with 4-week inactivity)
Aumentar a média das notas dos alunos.
* How will we measure the metric? (e.g. A/B test on a specified subset for a specified period; or comparison of performance after implementation to baseline)
Após criação do projeto será feito casos reais com pessoas que aceitem ceder seus históricos escolares e boletins.

## Plan
* Phases (milestones), timeline, short description of what we'll do in each phase.
- Conseguir ler as notas dos alunos.
- Indentificar quais notas precisam de reforço e quais não.
- Separar quais conteúdos poderiam ajudar em cada matéria.
- Gerar o PDF contendo as matérias que precisam de atenção e o material de apoio.

## Architecture
* Data
  * What data do we expect? Raw data in the customer data sources (e.g. on-prem files, SQL, on-prem Hadoop etc.)
  Os dados de notas dos alunos, informações sobre as matérias e sobre as provas que cada nota representa.

* Usability
  O programa funcionará como uma API que recebe os dados como excel ou csv, trata internamente e envia via email dos alunos os PDFs personalizados.

## Communication
* How will we keep in touch? Weekly meetings?
  
* Who are the contact persons on both sides?
