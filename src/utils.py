import cv2
import numpy as np
import os

def load_image(image_path, grayscale=True):
    """
    Carrega uma imagem.
    Args:
        image_path (str): Caminho para a imagem.
        grayscale (bool): Se True, carrega a imagem em tons de cinza.
    Returns:
        np.array: A imagem carregada.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Imagem não encontrada: {image_path}")

    if grayscale:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # OpenCV carrega BGR, converter para RGB

    if img is None:
        raise ValueError(f"Não foi possível carregar a imagem: {image_path}. Verifique o formato ou se o arquivo está corrompido.")
    
    # Normaliza para float entre 0 e 1, útil para algumas operações
    return img.astype(np.float32) / 255.0 if img.dtype == np.uint8 else img

def save_image(image, output_path):
    """
    Salva uma imagem. Assume que a imagem está em float [0,1] ou uint8 [0,255].
    Args:
        image (np.array): A imagem a ser salva.
        output_path (str): Caminho para salvar a imagem.
    """
    # Converte de volta para uint8 se for float
    if image.dtype == np.float32 or image.dtype == np.float64:
        image = (image * 255).astype(np.uint8)

    # Se a imagem for 3 canais mas não RGB (e.g., está em RGB), converte para BGR para OpenCV
    if len(image.shape) == 3 and image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    cv2.imwrite(output_path, image)
    print(f"Imagem salva em: {output_path}")

def create_output_dir(path="images/output"):
    """Cria o diretório de saída se ele não existir."""
    os.makedirs(path, exist_ok=True)
    print(f"Diretório de saída criado ou já existe: {path}")