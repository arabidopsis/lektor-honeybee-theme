API.add_css =function(url) {
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = url
    const head = document.querySelector('head')
    head.appendChild(link)
}