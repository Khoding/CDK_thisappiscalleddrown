import {getCookie} from './modules/cookies.js'
import {displayAlert} from './modules/alerts.js'

window.join = join
window.leave = leave

function join() {
    let data = {
        action: "join"
    }

    fetch(location.href, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
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