# Aplicativo de Filtro de Imagens

## Introdução
- Este aplicativo em Python foi desenvolvido em um trabalho em grupo realizado no final do período 2023.2.
- O usuário carrega uma imagem (local ou disponibiliza o link público dela) e poderá aplicar um filtro nela, que será salva com um nome descritivo.

## Recursos
- Informar o Caminho da Imagem: Permite carregar uma imagem informando o caminho local do arquivo ou uma URL da imagem.
- Escolher um Filtro: Após carregar a imagem, você pode escolher entre diferentes filtros para aplicar à imagem, como Escala de Cinza, Preto e Branco, Cartoon, Foto Negativa, Contorno e Blurred.
- Listar Arquivos de Imagem: Lista os arquivos de imagem disponíveis no diretório corrente.

## Uso
- Via terminal: Executar o arquivo `backend.py`
- Via interface gráfica: Executar o arquivo `frontend.py`

## Bibliotecas necessárias
- `requests`: faz o download da imagem
- `PIL`: manipula as imagens e aplica filtros
- `tqdm`: atualiza a barra de progresso de download via terminal
- `os`: manipula o diretório de imagens
