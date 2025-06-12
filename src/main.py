import os
import matplotlib.pyplot as plt
from utils import load_image, save_image, create_output_dir
from morph_reconstruction import remove_small_objects_reconstruction, fill_holes_reconstruction

def plot_images(original, processed, title_original, title_processed, output_filename=None):
    """
    Plota as imagens original e processada lado a lado.
    Args:
        original (np.array): Imagem original.
        processed (np.array): Imagem processada.
        title_original (str): Título para a imagem original.
        title_processed (str): Título para a imagem processada.
        output_filename (str): Nome do arquivo para salvar o gráfico.
    """
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.imshow(original, cmap='gray')
    plt.title(title_original)
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(processed, cmap='gray')
    plt.title(title_processed)
    plt.axis('off')

    plt.tight_layout()
    if output_filename:
        output_path = os.path.join("images/output", output_filename)
        plt.savefig(output_path)
        print(f"Gráfico salvo em: {output_path}")
    plt.show()

def main():
    create_output_dir()

    # --- Exemplo 1: Eliminação de Pequenos Objetos Indesejados (Remoção de Ruído) ---
    print("\n--- Executando Exemplo 1: Remoção de Pequenos Objetos ---")
    input_noisy_image_path = "images/input/noisy_image.jpg" # Certifique-se de ter esta imagem
    output_denoised_image_path = "images/output/denoised_image.jpg"
    output_denoised_plot_path = "denoised_image_plot.jpg"

    try:
        noisy_image = load_image(input_noisy_image_path)
        print(f"Imagem '{input_noisy_image_path}' carregada.")
        
        # O marker_size para a abertura deve ser maior que o tamanho dos objetos a serem removidos
        # e menor que o tamanho dos objetos a serem preservados.
        # Experimente com diferentes valores para 'marker_size'.
        denoised_image = remove_small_objects_reconstruction(noisy_image, marker_size=10)
        
        save_image(denoised_image, output_denoised_image_path)
        plot_images(noisy_image, denoised_image, 
                    "Imagem Original com Ruído", 
                    "Pequenos Objetos Removidos (Reconstrução Morfológica)", 
                    output_denoised_plot_path)
        print("Exemplo 1 concluído.")

    except FileNotFoundError as e:
        print(f"Erro: {e}. Por favor, crie uma imagem '{os.path.basename(input_noisy_image_path)}' na pasta 'images/input/' para este exemplo.")
    except Exception as e:
        print(f"Ocorreu um erro no Exemplo 1: {e}")

    # --- Exemplo 2: Preenchimento de Buracos em Objetos ---
    print("\n--- Executando Exemplo 2: Preenchimento de Buracos ---")
    input_holes_image_path = "images/input/image_with_holes.jpg" # Certifique-se de ter esta imagem
    output_filled_holes_path = "images/output/filled_holes_image.jpg"
    output_filled_holes_plot_path = "filled_holes_image_plot.jpg"

    try:
        image_with_holes = load_image(input_holes_image_path)
        print(f"Imagem '{input_holes_image_path}' carregada.")
        
        filled_holes_image = fill_holes_reconstruction(image_with_holes)
        
        save_image(filled_holes_image, output_filled_holes_path)
        plot_images(image_with_holes, filled_holes_image, 
                    "Imagem Original com Buracos", 
                    "Buracos Preenchidos (Reconstrução Morfológica)", 
                    output_filled_holes_plot_path)
        print("Exemplo 2 concluído.")

    except FileNotFoundError as e:
        print(f"Erro: {e}. Por favor, crie uma imagem '{os.path.basename(input_holes_image_path)}' na pasta 'images/input/' para este exemplo.")
    except Exception as e:
        print(f"Ocorreu um erro no Exemplo 2: {e}")

if __name__ == "__main__":
    main()