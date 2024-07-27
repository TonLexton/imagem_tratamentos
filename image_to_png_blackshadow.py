from google.colab import files
from PIL import Image, ImageFilter, ImageOps
import os

# Função para processar e adicionar sombra a uma imagem
def add_shadow(image_path, border_width):
    image = Image.open(image_path)

    # Aplicar sombra às bordas com efeito de gradiente
    border = border_width  # Largura da sombra
    expanded_image = ImageOps.expand(image, border=border, fill=(0, 0, 0, 0))

    # Criar uma máscara de gradiente
    mask = Image.new('L', (expanded_image.width, expanded_image.height), 0)
    for i in range(border):
        gradient_value = int(255 * (i / border))  # Gradiente de 100% a 0%
        mask.paste(gradient_value, (i, i, expanded_image.width - i, expanded_image.height - i))

    # Aplicar a máscara de gradiente à imagem expandida
    shadow = expanded_image.copy()
    shadow.putalpha(mask)
    shadow = shadow.filter(ImageFilter.GaussianBlur(border // 2))

    # Criar uma camada de sombra preta sólida
    black_shadow = Image.new('RGBA', shadow.size, (0, 0, 0, 220))
    black_shadow.putalpha(mask)

    # Compor a sombra com a imagem original
    composite = Image.alpha_composite(black_shadow, shadow)

    # Colar a imagem original sobre a borda sombreada
    composite.paste(image, (border, border), image.convert("RGBA"))

    # Salvar a imagem como PNG com o mesmo nome
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_path = f"{base_name}_shadow.png"
    composite.save(output_path)
    return output_path

# Carregar imagens
uploaded = files.upload()

# Definir a largura da borda (ajuste de acordo com a imagem de exemplo)
border_width = 15  # Ajuste a largura da borda aqui

# Processar cada imagem carregada
output_files = []
for filename in uploaded.keys():
    output_path = add_shadow(filename, border_width)
    output_files.append(output_path)

# Baixar as imagens processadas
for output_file in output_files:
    files.download(output_file)
