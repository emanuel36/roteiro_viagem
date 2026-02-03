#!/usr/bin/env python3
"""
Script para cortar PDF removendo margens brancas.
"""

import os
import sys
import tempfile
import shutil
import argparse

try:
    import fitz  # PyMuPDF
    from PIL import Image, ImageChops
except ImportError as e:
    print(f"Erro: Biblioteca necessária não encontrada: {e}")
    print("Instale com: pip install PyMuPDF pillow")
    sys.exit(1)


def trim_image(image):
    """
    Remove todas as bordas brancas de uma imagem PIL.
    """
    # Criar uma imagem de referência com a cor de fundo
    bg = Image.new(image.mode, image.size, image.getpixel((0, 0)))
    diff = ImageChops.difference(image, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    
    # Encontrar o bounding box
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    return image


def crop_pdf(input_path, output_path, dpi=300):
    """
    Corta PDF removendo margens brancas.
    """
    print(f"Processando: {input_path}")
    
    doc = fitz.open(input_path)
    temp_dir = tempfile.mkdtemp()
    
    try:
        image_paths = []
        
        for page_num in range(len(doc)):
            # Renderizar página como imagem
            page = doc[page_num]
            pix = page.get_pixmap(dpi=dpi)
            
            # Converter para PIL Image
            if pix.n == 4:
                img_mode = 'RGBA'
            elif pix.n == 3:
                img_mode = 'RGB'
            else:
                img_mode = 'L'
            
            img = Image.frombytes(img_mode, (pix.width, pix.height), pix.samples)
            
            # Aplicar trim para remover bordas brancas
            trimmed = trim_image(img)
            
            # Salvar imagem temporária
            temp_img_path = os.path.join(temp_dir, f'page_{page_num:04d}.png')
            trimmed.save(temp_img_path, 'PNG', dpi=(dpi, dpi))
            image_paths.append(temp_img_path)
        
        # Criar novo PDF com as imagens cortadas
        output_doc = fitz.open()
        
        for img_path in image_paths:
            img_pdf = fitz.open(img_path)
            pdfbytes = img_pdf.convert_to_pdf()
            img_pdf.close()
            
            img_pdf = fitz.open("pdf", pdfbytes)
            output_doc.insert_pdf(img_pdf)
            img_pdf.close()
        
        # Salvar PDF final
        output_doc.save(output_path, garbage=4, deflate=True, clean=True)
        output_doc.close()
        
        print(f"PDF salvo em: {output_path}")
        
    finally:
        shutil.rmtree(temp_dir)
        doc.close()


def main():
    parser = argparse.ArgumentParser(description="Remove margens brancas de PDF")
    parser.add_argument("input", help="Arquivo PDF de entrada")
    parser.add_argument("-o", "--output", help="Arquivo PDF de saída")
    parser.add_argument("-d", "--dpi", type=int, default=300,
                       help="Resolução DPI (default: 300)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Erro: Arquivo não encontrado: {args.input}")
        sys.exit(1)
    
    if not args.output:
        name, ext = os.path.splitext(args.input)
        args.output = f"{name}_cortado{ext}"
    
    try:
        crop_pdf(args.input, args.output, args.dpi)
        print("✅ Concluído!")
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
