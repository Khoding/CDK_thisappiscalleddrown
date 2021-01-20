import {getCookie} from './modules/cookies.js'
import {displayAlert} from './modules/alerts.js'

window.join = join
window.leave = leave
window.sendInvite = sendInvite

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
                console.log(data)
                displayAlert(data['message'].severity, data['message'].text)

            }
        )
        .catch(error => {
            console.error('Error:', error);
            displayAlert("ERROR", "Erreur.")
        });

    console.log(data)
}