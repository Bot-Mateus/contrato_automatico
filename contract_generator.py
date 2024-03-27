from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT


def fill_contract_template(data, template_path, output_path):
    # Abrir o documento modelo
    doc = Document(template_path)

    # Percorrer todas as seções do documento
    for paragraph in doc.paragraphs:
        # Substituir marcadores de posição pelos dados do contrato
        for key, value in data.items():
            if key in paragraph.text:
                run = paragraph.runs[0]
                run.text = run.text.replace(key, value)

    # Salvar o contrato preenchido
    doc.save(output_path)


# Exemplo de dados do contrato
contract_data = {
    '{{ landlord_name }}': 'Cristina Almeida',
    '{{ tenant_name }}': 'Ingrid Vanessa',
    '{{ property_address }}': 'Rua Barra de Guabiraba, 258, Itaquera - São Paulo, SP',
    '{{ rent_amount }}': 'R$800',
    '({{ valor_extenso }}': 'oitocentos reais',
    '{{ start_date }}': '01/04/2024',
    '{{ end_date }}': '01/04/2025',
    '{{ cidade_foro }}': 'São Paulo'
}

# Caminho do modelo de contrato e do contrato de saída
template_path = 'template_contract.docx'
tenant_name = contract_data['{{ tenant_name }}']
output_path = f'generated_contract_{tenant_name}.docx'

# Preencher o contrato
fill_contract_template(contract_data, template_path, output_path)
