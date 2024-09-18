document.getElementById('html_data').dataset.bsTheme = get_current_theme();
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll("svg").forEach(svg => svg.addEventListener('click', (event) => change_theme(event)));
    document.getElementById('html_data').dataset.bsTheme = get_current_theme();
})


function change_theme(event) {
    const theme = document.getElementById('html_data')
    if (theme.dataset.bsTheme == 'dark' && event.target.getAttribute("id") == 'sun') {
        set_theme('light', 'black')
    } else if (theme.dataset.bsTheme == 'light' && event.target.getAttribute("id") == 'moon') {
        set_theme('dark', 'white')
    }
}


function set_theme(theme_color, color) {
    const theme = document.getElementById('html_data');
    theme.dataset.bsTheme = theme_color;
    document.querySelector('#sun').setAttribute('color', color);
    document.querySelector('#sun').setAttribute('fill', color);
    document.querySelector('#moon').setAttribute('color', color);
    document.querySelector('#moon').setAttribute('fill', color);
    localStorage['bsTheme'] = theme_color;
    set_label_class(`labels-${color}`)
}

function get_current_theme() {
    theme = getCache('bsTheme')
    if (theme == 'light' || theme == null) {
        set_theme('light', 'black');
        set_label_class('labels-black')
        theme = 'light'
    } else if (theme == 'dark') {
        set_theme('dark', 'white');
        set_label_class('labels-white')

    }
    return theme
}
function getCache(name) {
    if (localStorage[name] != null) {
        return localStorage[name];
    }
    return null;
}


function set_label_class(class_name) {
    document.querySelectorAll('label').forEach(function (label) {
        label.classList.add('col-form-label');
        if (document.getElementsByClassName("login-form-1")) {
            class_name = "labels-white"
        } else {
            if (label.classList.contains('labels-black')) {
                label.classList.remove('labels-black');
            } else {
                label.classList.remove('labels-white');
            }
        }
        label.classList.add(class_name);
    });

}