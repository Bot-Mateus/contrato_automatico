function generateContract() {
    // Exibir mensagem de carregamento
    document.getElementById('loading').style.display = 'block';

    // Obter os dados do formulário
    var formData = new FormData(document.querySelector('form'));

    // Criar uma solicitação AJAX para gerar o contrato
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/generate_contract', true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            // Ocultar mensagem de carregamento
            document.getElementById('loading').style.display = 'none';
            // Exibir mensagem de sucesso
            document.getElementById('success-message').style.display = 'block';
            // Exibir o link de download
            document.getElementById('download-link').style.display = 'block';
            // Extrair o nome do arquivo do contrato gerado da resposta JSON
            var response = JSON.parse(xhr.responseText);
            var contractFilename = response.contract_filename;
            // Atualizar o link de download com o nome do arquivo do contrato gerado
            var contractId = response.contract_id;
            document.getElementById('download-link').href = "/download_contract?contract_id=" + contractId;
        } else {
            alert('Erro ao gerar o contrato. Por favor, tente novamente.');
            // Ocultar mensagem de carregamento em caso de erro
            document.getElementById('loading').style.display = 'none';
        }
    };
    xhr.send(formData);
}
