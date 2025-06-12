import numpy as np
# Importe 'footprint_rectangle' para substituir 'square' depreciado
from skimage.morphology import disk, erosion, dilation, reconstruction, footprint_rectangle 
# Removido 'square' do import, pois será substituído

def remove_small_objects_reconstruction(image, marker_size=5): # Removido element_structuring dos parâmetros
    """
    Remove pequenos objetos de uma imagem em tons de cinza usando reconstrução morfológica.
    Baseado na abertura morfológica seguida de reconstrução.

    Args:
        image (np.array): Imagem de entrada em tons de cinza (float [0,1]).
        marker_size (int): Tamanho do elemento estruturante para a abertura (disco).
                           Um disco de tamanho 'marker_size' é usado para a abertura.

    Returns:
        np.array: Imagem resultante com pequenos objetos removidos.
    """
    # Para a reconstrução geodésica (method='dilation'), o 'selem' geralmente
    # não é um argumento direto da função reconstruction em versões mais recentes.
    # O elemento estruturante é implicitamente um elemento de conectividade (e.g., 4-conectividade).
    # Se você precisar de um elemento estruturante específico para a erosão/dilatação
    # que antecede a reconstrução, aplique-o nas etapas 'erosion' e 'dilation' separadamente.

    # 1. Aplica uma erosão na imagem original para criar o marcador
    # O elemento estruturante para a erosão inicial deve ser grande o suficiente para remover ruído
    se_open = disk(marker_size) # Elemento estruturante para a erosão inicial
    eroded_image = erosion(image, se_open)
    
    # Em seguida, reconstruímos a partir da imagem erodida (marcador)
    # usando a imagem original como máscara.
    # Removido o argumento 'selem' de reconstruction()
    reconstructed_image = reconstruction(eroded_image, image, method='dilation')
    
    return reconstructed_image

def fill_holes_reconstruction(image): # Removido element_structuring dos parâmetros
    """
    Preenche buracos em objetos de uma imagem em tons de cinza usando reconstrução morfológica.
    Adaptado para imagens em níveis de cinza onde "buracos" são regiões de menor intensidade.

    Args:
        image (np.array): Imagem de entrada em tons de cinza (float [0,1]).

    Returns:
        np.array: Imagem resultante com buracos preenchidos.
    """
    # O elemento estruturante para a dilatação geodésica interna à reconstrução
    # é tipicamente um elemento de conectividade padrão, não precisa ser explicitado.
    # Substituído square(3) por footprint_rectangle(3, 3) conforme o FutureWarning.
    # No entanto, para a função reconstruction, esse selem não é um argumento direto.
    # A linha abaixo é apenas para fins de referência se um selem fosse necessário para outras operações.
    # se_fill = footprint_rectangle(3, 3) 

    # Imagem complemento (inverte a imagem para que buracos se tornem "picos")
    max_val = np.max(image)
    image_complement = max_val - image

    # Crie o marcador: zero em todos os lugares, exceto nas bordas.
    # Os pixels de fronteira da imagem complementar são os "marcadores"
    # a partir dos quais a reconstrução irá preencher as "cavidades" (buracos).
    marker = np.zeros_like(image_complement)
    marker[0, :] = image_complement[0, :]
    marker[-1, :] = image_complement[-1, :]
    marker[:, 0] = image_complement[:, 0]
    marker[:, -1] = image_complement[:, -1]

    # Reconstrução por dilatação da imagem complementar
    # O marcador é o ponto de partida, a imagem complementar é a máscara.
    # Removido o argumento 'selem' de reconstruction()
    reconstructed_complement = reconstruction(marker, image_complement, method='dilation')

    # Inverte de volta para obter a imagem original com os buracos preenchidos
    filled_image = max_val - reconstructed_complement
    
    return filled_image