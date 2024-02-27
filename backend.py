import os
import requests
from PIL import Image, ImageFilter, ImageOps
from tqdm import tqdm

'''
Links para testar o Download:
https://t.ctcdn.com.br/JlHwiRHyv0mTD7GfRkIlgO6eQX8=/640x360/smart/i257652.jpeg

https://s2-techtudo.glbimg.com/G9XdtYb1LUg1x5v4QLVeNBYj7X4=/400x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_08fbf48bc0524877943fe86e43087e7a/internal_photos/bs/2022/c/u/15eppqSmeTdHkoAKM0Uw/dall-e-2.jpg
'''

class Imagem:
  def __init__(self, caminho):
      self.caminho = caminho 
      self.nome_arquivo = os.path.basename(caminho) # indentify the path and the name of the file

  def carregar_imagem(self):
      try:
          imagem = Image.open(self.caminho) # abrir a imagem
          print("Imagem carregada com sucesso!\n")   
          return imagem
      except FileNotFoundError: # Tratar uma abertura falha = avisar ao cliente + forma de solução
          print("Arquivo não encontrado\n",
                "Verifique se você digitou imagens/nome-do-arquivo\n")
      except Exception as e:
          print(f"Erro ao carregar a imagem: {str(e)}\n") # 2ª possibilidade de erro!
          return None

  def salvar_imagem(self, imagem, filtro):
      nome_arquivo_sem_extensao, extensao = os.path.splitext(self.nome_arquivo) # separa o nome da extensão
      caminho_saida = os.path.join('imagens', f"{nome_arquivo_sem_extensao}_{filtro}{extensao}") # junta dnv, só que com tratamento

      # verificar se pode salvar desse modo ou não
      if os.path.exists(caminho_saida):
          resposta = input("Arquivo já existente. Deseja substituí-lo? [s/n] ").lower()
          if resposta != 's':
              print("Operação Cancelada!\n")
              return
            
      try:
          imagem.save(caminho_saida)
          print("Imagem salva com sucesso.\n")
          return
      except Exception as e:
          print(f"Erro ao salvar a imagem: {str(e)}\n")
          raise Exception

class Download:
  def __init__(self, url, path_arquivo):
    self.url = url
    self.path_arquivo = path_arquivo

  @staticmethod
  def extrair_nome_extensao_url(url):
    try:
      if url.startswith("http://") or url.startswith("https://"):
        caminho_arquivo = url.split('/')[-1]
      else:
        raise ValueError("Protocolo não suportado. Use 'http://' ou 'https://'.")

      if not caminho_arquivo:
        raise ValueError("URL inválida")

      nome_arquivo, extensao = os.path.splitext(caminho_arquivo)
      return nome_arquivo, extensao
    except Exception as ex:
      print(f"Erro ao extrair nome e extensão da URL: {str(ex)}")
      raise Exception

  def executa(self):
    try:
        print("\nAguarde...")
        response = requests.get(self.url, stream=True)
        response.raise_for_status()  # Verifica se houve algum erro na requisição

        tamanho_total = int(response.headers.get('content-length', 0))
        progresso = tqdm(total=tamanho_total, unit='iB', unit_scale=True)

        with open(self.path_arquivo, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    progresso.update(len(chunk))
                    file.write(chunk)

        progresso.close()

        if tamanho_total != 0 and progresso.n != tamanho_total:
            print("Erro, algo deu errado durante o download.")
            raise Exception
        else:
            print(f"Download completo. Arquivo salvo em: {self.path_arquivo}\n")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer o download: {str(e)}\n")
        return None

# Classe Mãe Filtro
class Filtro():
  @staticmethod
  def aplicar_filtro(filtro, imagem):
      try:
          return filtro().aplicar(imagem)
      except Exception as e:
          print(f"Erro ao aplicar o filtro {str(e)}\n")
          raise Exception

  # classes filhas de Filtro:
  class EscalaCinza:
      def aplicar(self, imagem):
          imagem = ImageOps.grayscale(imagem)
          return imagem

  class PretoBranco:
      def aplicar(self, imagem):
          # Converte para escala de cinza e inverte as cores para virar BW
          imagem = imagem.convert('L')
          imagem = imagem.convert('1')
          return imagem

  class Cartoon:
      def aplicar(self, imagem):
          imagem = imagem.filter(ImageFilter.CONTOUR)
          return imagem

  class FotoNegativa:
      def aplicar(self, imagem):
          # Verifica se a imagem possui fundo transparente 
          if imagem.mode == "RGBA":
              imagem = imagem.convert("RGB")

          # Aplica um filtro negativo padrão
          imagem = ImageOps.invert(imagem)
          return imagem

  class Contorno:
      def aplicar(self, imagem):
          # converter para grayscale
          imagem = imagem.convert('L')

          # ajustar as bordas
          imagem = imagem.filter(ImageFilter.EDGE_ENHANCE)

          # definição de bordas
          imagem = imagem.filter(ImageFilter.FIND_EDGES)

          # Aplica um filtro de contorno
          imagem = ImageOps.invert(imagem)
          return imagem

  class Blurred:
      def aplicar(self, imagem):
          imagem = imagem.filter(ImageFilter.BLUR)
          return imagem

class Principal():
  # construtor
  def __init__(self):
    self.imagem = None
    self.filtros = None
    self.caminho = None

  # Receber a informação do caminho da imagem
  def informar_Caminho(self, caminho):
    self.caminho = caminho
    if caminho.startswith("http") or caminho.startswith("https"):
      # Prepara o download
      nome, extensao = Download.extrair_nome_extensao_url(caminho)
      nome_arquivo = nome + extensao
      path_foto = "imagens" + "/" + nome_arquivo
      download_manager = Download(caminho, path_foto)
      download_manager.executa()

      # Carrega a imagem
      self.imagem = Imagem(path_foto).carregar_imagem()
    elif os.path.exists(caminho):
       self.imagem = Imagem(caminho).carregar_imagem()
    else:
       print("Esse arquivo não existe.")
       return None
      

    if self.imagem is None:
      print("Não foi possível carregar a imagem.\n")
      return

  def Escolher_Filtro(self):
    if self.imagem is None:
      print("Nenhuma imagem carregada.\n")
      return

    # tuplas com as opções de filtros
    filtros = {
        1: Filtro.EscalaCinza,
        2: Filtro.PretoBranco,
        3: Filtro.Cartoon,
        4: Filtro.FotoNegativa,
        5: Filtro.Contorno,
        6: Filtro.Blurred
    }

    # Mostra o menu de filtros
    print()
    print("------ MENU DE FILTROS ------")
    print("1 - Escala de Cinza",
          "2 - Preto e Branco",
          "3 - Filtro Cartoon",
          "4 - Modo Foto Negativa",
          "5 - Modo Contorno",
          "6 - Modo Blurred",
          sep="\n")
    print("-----------------------------")

    try:
      opcao = int(input("Escolha uma opção: "))
      print("\n")
      if opcao in filtros:
        opcao = int(opcao)
        filtro_selecionado = filtros[opcao]
        
        imagem_filtrada = Filtro.aplicar_filtro(filtro_selecionado, self.imagem)
        Imagem(self.caminho).salvar_imagem(imagem_filtrada, filtro_selecionado.__name__)
      else:
        print("Opção inválida.\n")
        return
    except ValueError:
      print("Por favor, digite um número.\n")
    except Exception as e:
      print(f"Erro ao aplicar o filtro: {str(e)}\n")
      return


  def Listar_Arquivos_Imagem(self):
    print("\nArquivos de imagem disponíveis: ")
    imagens = []

    for arquivo in os.listdir('imagens'):
      if arquivo.endswith(".jpg") or arquivo.endswith(".png") or arquivo.endswith(".jpeg"):
        imagens.append(arquivo)

    if len(imagens) == 0:
      print("Nenhum arquivo de imagem disponível.")
    else:
      for imagem in imagens:
        print(imagem)
    print("\n")

  def executar(self):
    while True:
      print("----------------------------------------")
      print("MENU PRINCIPAL".center(40))
      print("----------------------------------------")

      print("1 - Informar o caminho da imagem",
            "2 - Escolher um filtro",
            "3 - Listar arquivos de imagem do diretório corrente",
            "4 - Sair",
            sep="\n")

      try:
        opcao = int(input("Escolha uma opção: "))
        if opcao > 4 or opcao < 1:
          print("Opção inválida.\n")
          continue
        elif opcao == 1:
          caminho = input("Por favor, informe o caminho da imagem (local ou URL): ")
          self.informar_Caminho(caminho)
        elif opcao == 2:
          self.Escolher_Filtro()
        elif opcao == 3:
          self.Listar_Arquivos_Imagem()
        else:
          print("Saindo...")
          break
      except ValueError:
        print("Por favor, digite um número.\n")

# Instancia a classe Principal e executa o programa
if __name__ == "__main__":
  programa = Principal()
  programa.executar()