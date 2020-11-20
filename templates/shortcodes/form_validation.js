function form_validation($, form, e) {
    e.preventDefault();
    e.stopPropagation();
    const $form = $(form);
    $form.removeClass(['sent','failed','sending'])
    
    $form.addClass('was-validated');
    if (form.checkValidity() === false) {
        return
    }
    const fd = new FormData(form);

    $form.addClass('sending')

    $.ajax({
        url:$form.attr('action'),
        type:$form.attr('method'),
        data:fd,
        processData: false,
        cache: false,
        contentType: false,
        enctype: 'multipart/form-data'
    }).done(function() {
        $form.addClass('sent')
    }).fail(function() {
        $form.addClass('failed')
    }).always(function() { 
        $form.removeClass('sending') 
    })
}