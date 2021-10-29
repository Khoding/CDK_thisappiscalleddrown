import {getCookie} from './modules/cookies.js'
import {displayAlert} from './modules/alerts.js'

window.join = join
window.leave = leave
window.sendInvite = sendInvite
window.copyLink = copyLink

$(document).ready(function () {
    $(function () {
        let href = location.href
        let url = href.split('#')
        let tab = url[url.length - 1]

        $(`[href="#${tab}"]`).tab('show')
    })

    $('#invitationModal').on('shown.bs.modal', function (e) {
        let data = {
            action: "getInvitationLink"
        }

        fetch(location.href, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }
        )
            .then(response => {
                return response.json()
            })
            .then(data => {
                    let url = location.protocol + "//" + location.hostname + ":" + location.port + data.invitationLink
                    $("#invitationLink")[0].value = url
                    $('#shareInvitationLink')[0].href = 'mailto:' + $('#id_email').val() + '?subject=Invitation à rejoindre un groupe sur thisappiscalleddrown&body=Lien : ' + url
                }
            )
            .catch(error => {
                console.error('Error:', error);
                displayAlert("ERROR", "Une erreur est survenue.")
            });
    }).on('hide.bs.modal', function (e) {
        $('#invitationForm')[0].reset()
        $('#shareInvitationLink')[0].href = '#'
    })
})

function join() {
    let data = {
        action: "join"
    }

    fetch(location.href, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }
    )
        .then(result => {
            $("#joinButton").replaceWith('<button id="leaveButton" type="button" class="btn btn-secondary" onclick="leave();">Quitter</button>')
            displayAlert("SUCCESS", "Groupe rejoint avec succès.")
        })
        .catch(error => {
            console.error('Error:', error);
            displayAlert("ERROR", "Une erreur est survenue.")
        });
}

function leave() {
    let data = {
        action: "leave"
    }
    fetch(location.href, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }
    )
        .then(result => {
            $("#leaveButton").replaceWith('<button id="joinButton" type="button" class="btn btn-secondary" onclick="join();">Rejoindre</button>')
            displayAlert("SUCCESS", "Groupe quitté avec succès.")
        })
        .catch(error => {
            console.error('Error:', error);
            displayAlert("ERROR", "Une erreur est survenue.")
        });
}

/* Permet d'envoyer une invitation au groupe à une adresse email */
function sendInvite() {
    let data = {
        action: 'invite',
        form: {
            email: $('#id_email').val(),
            message: $('#id_message').val()
        }
    }

    fetch(location.href, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }
    )
        .then(response => {
            return response.json()
        })
        .then(data => {
                displayAlert(data['message'].severity, data['message'].text)
            }
        )
        .catch(error => {
            console.error('Error:', error);
            displayAlert("ERROR", "Erreur.")
        });
}

function copyLink() {
    let copyTextFrom = $("#invitationLink")[0];

    copyTextFrom.disabled = false;
    copyTextFrom.focus();
    copyTextFrom.select();
    document.execCommand('copy');
    window.getSelection().removeAllRanges();
    copyTextFrom.blur();
    copyTextFrom.disabled = true;
}
