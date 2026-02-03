# Gerador de Guias de Viagem

Sistema para gerar guias de viagem personalizados com roteiros interativos em HTML e exportação otimizada para impressão.

## Estrutura do Projeto

- `roteiro.html` - Arquivo HTML com o roteiro interativo da viagem (inclui botão de exportação)
- `remove_margens.py` - Script Python para processar o HTML exportado e remover margens desnecessárias

## Como Usar

### Pré-requisitos
- Python 3 instalado
- Navegador web para visualizar o HTML

### Passos

1. Abra o arquivo `roteiro.html` no navegador.
2. Exporte o roteiro usando o botão.
   - No arquivo HTML aberto, clique no botão "Exportar"
   - Salve o arquivo HTML exportado
3. Use o script `remove_margens.py` para remover as margens desnecessárias.
   ```bash
   python remove_margens.py
   ```

## Resultado Final

**[Clique aqui para baixar o PDF completo](guia.pdf)**
