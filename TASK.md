# Models
    -  Usuario
        - tipo_usuario
    - Restaurante
       - Nome
       - dono (Usuario)
       - Duracao da reserva
       - Horario de abertura
       - Horario de fechamento
       - logo
       - imagem de fundo
       - descricao
    - Mesa
        - Tipo de mesa (redonda, quadrada, 2 ou 4 lugares):será um txt do nome do icone
        - numero de assentos(baseado no item acima consigo definir qnt assentos cada mesa gem)
        - restaurante( a qual restaurante pertence)
    - Reserva
        - data (dia e hora)
        - usuario que reservou
        - mesa 

Como calcular o horario de reserva
        tempo de reserva = (reserva_desejada + duracao reserva)
        tempo de reserva_2 = (reserva_desejada - duracao reserva)
        restaurante.mesas,reservas.filtro( nao pode ser data maior q tempo de reserva  e menor q tempo de reserva_2)



Ideias 
ver a possibilidade de montar um background semelhante  ao restaurante
permitir o usuario a personalizar cada mesa
Dois tipos de usuarios o dono do restaurante e o usuario que consome
busca de restaurante por nome like
tela do restaurante com algunmas infos
tela onde o cliente pode visualizar as reservas que ele possui
tela onde o dono do restaurante pode visualizar as reservas por dia e em ordem 
Obrigar nome completo
tela onde o cliente seleciona o horario, a mesa e realiza a reserva sendo redirecionado para a tela de reserva
Tentar utilizar o tdd para o desenvolvimento, 

- Orde de dev
   [x]models
   [x]test models
   [x]views de cadastro de usuario(cliente, fornecedor)
   [x]view de cadastro de restaurante(mesas automaticas, mesas personalizadas)
   [x]view de visualiaçao de restaurante com descriçao e imagem de fundo semelhante ao ifood
   [x]view de reserva
   [x]view de busca de restaurantes
   [x]view de lista  de restaurantes de um dono
   [x]view do restaurante com todos os agendamentos para aquele dia X 
   [x] view do cliente para todos os seus agendamento com status waiting
   [X] view com dados de contato do cliente apenas no maximo telefone
   [X] view de editar restaurante
   [x] view de editar mesas
   [X] view de editar dados do usuario(verificar para utilzar as mesmas ja existentes)
   


   cluckin bell
   ichiraku ramen
   central perk