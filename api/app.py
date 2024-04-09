import binascii
import os
import uuid  # Importe a biblioteca uuid para gerar identificadores únicos

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from docx import Document

app = Flask(__name__)

# Gere uma sequência aleatória de bytes e converta para hexadecimal
secret_key = binascii.hexlify(os.urandom(24)).decode('utf-8')

# Definir uma chave secreta para o aplicativo Flask
app.secret_key = 'sua_chave_secreta_aqui'

# Defina os campos para cada modelo de contrato
model_fields = {
    'modelo1': ['landlord_name', 'tenant_name', 'property_address', 'rent_amount', 'valor_extenso', 'start_date', 'end_date', 'cidade_foro'],
    'modelo2': ['nome_locador', 'nacionalidade_locador', 'estado_civil_locador', 'profissao_locador',
                'identidade_locador', 'cpf_locador', 'endereco_locador', 'nome_locatario',
                'nacionalidade_locatario', 'estado_civil_locatario', 'profissao_locatario',
                'identidade_locatario', 'cpf_locatario', 'endereco_locatario', 'nome_fiador1',
                'nacionalidade_fiador1', 'estado_civil_fiador1', 'profissao_fiador1',
                'identidade_fiador1', 'cpf_fiador1', 'endereco_fiador1', 'nome_fiador2',
                'nacionalidade_fiador2', 'estado_civil_fiador2', 'profissao_fiador2',
                'identidade_fiador2', 'cpf_fiador2', 'endereco_fiador2', 'endereco_imovel',
                'duracao', 'data_inicio', 'data_fim', 'dia_vencimento', 'valor_aluguel',
                'cidade_foro']
}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        modelo = request.form.get('modelo')
        return redirect(url_for('formulario', modelo=modelo))
    else:
        return render_template('index.html', model_fields=model_fields)


@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        modelo = request.form.get('modelo')
        campos = model_fields.get(modelo, [])
        return render_template('formulario.html', campos=campos, modelo=modelo)
    else:
        modelo = request.args.get('modelo')
        campos = model_fields.get(modelo, [])
        return render_template('formulario.html', campos=campos, modelo=modelo)


@app.route('/generate_contract', methods=['POST'])
def generate_contract():
    # Obtenha os dados do formulário
    contract_data = {campo: request.form[campo] for campo in request.form}

    # Determine o caminho do modelo de contrato com base na escolha do usuário
    modelo_contrato = request.form.get('modelo')
    if modelo_contrato == 'modelo1':
        template_path = 'static/template_contract1.docx'
    elif modelo_contrato == 'modelo2':
        template_path = 'static/template_contract2.docx'
    else:
        # Caso o modelo não seja reconhecido, retorne uma resposta JSON com erro
        return jsonify({'success': False, 'error': 'Modelo de contrato não reconhecido'})

    # Gere um identificador único para o contrato
    contract_id = str(uuid.uuid4())  # Isso gera um identificador único global (GUID)

    # Construa o nome do arquivo do contrato com o identificador único
    output_filename = f'contratos/generated_contract_{contract_id}.docx'

    # Preencha o modelo de contrato com os dados do formulário
    fill_contract_template(contract_data, template_path, output_filename)

    # Retorne uma resposta JSON indicando sucesso e o nome do arquivo do contrato gerado
    return jsonify({'success': True, 'contract_filename': output_filename, 'contract_id': contract_id})


@app.route('/download_contract')
def download_contract():
    contract_id = request.args.get('contract_id')
    contract_filename = f'generated_contract_{contract_id}.docx'
    contract_path = os.path.join('contratos', contract_filename)
    return send_file(contract_path, as_attachment=True)


def fill_contract_template(data, template_path, output_path):
    doc = Document(template_path)
    for paragraph in doc.paragraphs:
        for key, value in data.items():
            if key in paragraph.text:
                paragraph.text = paragraph.text.replace(key, value)
    doc.save(output_path)

if __name__ == '__main__':
    app.run(debug=True)