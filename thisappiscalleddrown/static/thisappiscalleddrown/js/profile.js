import {getCookie} from './modules/cookies.js'
import {displayAlert} from './modules/alerts.js'

window.deleteInvitation = deleteInvitation

$(document).ready(function () {
    $(function () {
        let delInvitationsButtons = $(".del-invitation-btn")

        for (let i = 0; i < delInvitationsButtons.length; i++) {
            delInvitationsButtons[i].addEventListener('click', deleteInvitation, false)
        }
    })
})

function deleteInvitation(event) {
    let button = event.currentTarget
    let slug = button.dataset.invitationSlug

    let data = {
        action: "deleteInvitation",
        invitationSlug: slug
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
            $('div[data-invitation-slug=' + slug + ']').remove()
            displayAlert("SUCCESS", "Invitation supprimée.")
        })
        .catch(error => {
            console.error('Error:', error);
            displayAlert("ERROR", "Une erreur est survenue.")
        });
}