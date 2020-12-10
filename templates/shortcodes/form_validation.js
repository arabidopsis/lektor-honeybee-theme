window.API = window.API || {}
API.form_validation = function(form, e) {
    e.preventDefault();
    e.stopPropagation();
    form.classList.remove('sent','failed','sending')
    
    form.classList.add('was-validated');
    if (form.checkValidity() === false) {
        return
    }
    const fd = new FormData(form);

    const url = form.getAttribute('action');

    const options = {
        method:form.getAttribute('method'),
        body: fd,
    }

    const always = () => form.classList.remove('sending')

    form.classList.add('sending')
    fetch(url, options)
        .then((resp) => {
            if (!resp.ok) {
                form.classList.add('failed')
            } else {
                form.classList.add('sent')
            }

        })
        .then(always)
        .catch(() => { form.classList.add('failed'); always();} )

}