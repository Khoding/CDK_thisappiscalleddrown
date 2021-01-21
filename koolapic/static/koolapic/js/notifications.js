import {getCookie} from './modules/cookies.js'
import {displayAlert} from './modules/alerts.js'

/**
 * Visibilité du mot de passe.
 * Nécessite :
 * JQuery (Slim supporté)
 **/
$(document).ready(function () {
    $(function () {
        let notifications = $('.notification')

        for (let i = 0; i < notifications.length; i++) {
            stylizeNotification(notifications[i])
        }

        createToggleReadButtons()
    });

    function createToggleReadButtons() {
        let buttons = $('.toggle-read-btn')

        for (let i = 0; i < buttons.length; i++) {
            buttons[i].addEventListener('click', toggleCheckboxListener)
        }
    }

    function toggleCheckboxListener(event) {
        let button = $(event.currentTarget)[0]
        let notificationId = button.dataset.notificationId
        let notification = $('[data-notification-id=' + notificationId + ']')[0]

        let data = {
            action: "toggleStatus",
            notification: notificationId
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
                    if (button.classList.contains('checked')) {
                        button.innerHTML = '<i class="far fa-square"></i>'
                        button.classList.toggle('checked')
                        notification.classList.toggle('notification-read')
                        notification.classList.toggle('notification-unread')
                    } else {
                        button.innerHTML = '<i class="far fa-check-square"></i>'
                        button.classList.toggle('checked')
                        notification.classList.toggle('notification-read')
                        notification.classList.toggle('notification-unread')
                    }
                    stylizeNotification(notification)
                    setBadgeNumber(data.unreadNotificationNumber)
                }
            )
            .catch(error => {
                console.error('Error:', error);
                displayAlert("ERROR", "Une erreur est survenue.")
            });
    }

    function stylizeNotification(notification) {
        let bgImage = notification.getAttribute('data-bg-image')
        if (notification.classList.contains('image-notification')) {
            if (notification.classList.contains('notification-read')) {
                notification.style = "background-image: linear-gradient(to right, #FFFFFF 70%, transparent 80%, transparent), url('" + bgImage + "');"
            } else if (notification.classList.contains('notification-unread')) {
                notification.style = "background-image: linear-gradient(to right, #6358EB 70%, transparent 80%, transparent), url('" + bgImage + "');"
            }
        }
    }

    function setBadgeNumber(number) {
        let button = $("#notificationBtn")[0]

        if (number !== 0) {
            button.innerHTML = '<i class="fas fa-bell"></i>' +
                '<span class="badge badge-danger notification-badge">' +
                number +
                '</span>'
        } else {
            button.innerHTML = '<i class="fas fa-bell"></i>'
        }
    }
});

