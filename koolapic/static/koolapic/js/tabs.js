$(document).ready(function () {
    $(function () {
        let href = location.href
        let url = href.split('#')
        let tab = url[url.length-1]

        $(`[href="#${tab}"]`).tab('show')
    })

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        let href = e.target.href

        location.assign(href)
    })
})