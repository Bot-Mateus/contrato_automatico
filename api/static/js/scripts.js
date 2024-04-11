function showPreview(modelo) {
    var previews = document.querySelectorAll('.contract-preview');
    previews.forEach(function(preview) {
        preview.style.display = 'none';
    });

    document.getElementById('preview-' + modelo).style.display = 'block';
}

function submitForm(modelo) {
    // Criar um formulário invisível
    var form = document.createElement('form');
    form.method = 'GET'; // Use GET para enviar o modelo como um parâmetro na URL
    form.action = '/formulario';

    // Adicionar um campo oculto para o modelo
    var modeloInput = document.createElement('input');
    modeloInput.type = 'hidden';
    modeloInput.name = 'modelo';
    modeloInput.value = modelo;
    form.appendChild(modeloInput);

    // Adicionar o formulário à página e enviá-lo
    document.body.appendChild(form);
    form.submit();
}
