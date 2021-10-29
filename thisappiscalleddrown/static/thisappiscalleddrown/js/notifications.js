import {getCookie} from './modules/cookies.js'
import {displayAlert} from './modules/alerts.js'

/**
 * Visibilité du mot de passe.
 * Nécessite :
 * JQuery (Slim supporté)
 **/

window.markAllAsRead = markAllAsRead

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
            buttons[i].addEventListener('click', deleteNotificationListener)
        }
    }

    function deleteNotificationListener(event) {
        let button = $(event.currentTarget)[0]
        let notificationId = button.dataset.notificationId
        let notification = $('[data-notification-id=' + notificationId + ']')[0]

        let data = {
            action: "deleteNotification",
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
                    notification.remove()
                    if (data.unreadNotificationNumber === 0) {
                        $("#notificationsList")[0].innerHTML = '<div class="empty text-primary">Vous n\'avez pas de notification...</div>'
                    }
                    setBadgeNumber(data)
                }
            )
            .catch(error => {
                console.error('Error:', error);
                displayAlert("ERROR", "Une erreur est survenue.")
            });
    }
});

function stylizeNotification(notification) {
    if (notification.classList.contains('image-notification')) {
        let bgImage = notification.getAttribute('data-bg-image')
        notification.style = "background-image: linear-gradient(to right, #6358EB 70%, transparent 80%, transparent), url('" + bgImage + "');"
    }
}

function setBadgeNumber(notifications_counts) {
    let button = $("#notificationBtn")[0]

    if (notifications_counts.all_unread_notifications_number !== 0) {
        button.innerHTML = '<i class="fas fa-bell"></i>' +
            '<span class="badge badge-danger notification-badge">' +
            notifications_counts.all_unread_notifications_number +
            '</span>'
        $("#notificationsTab")[0].innerHTML = 'Notifications <span class="badge badge-danger notification-badge">' +
            notifications_counts.unread_notifications_number +
            '</span>'
        $("#groupInvitationsTab")[0].innerHTML = 'Notifications <span class="badge badge-danger notification-badge">' +
            notifications_counts.group_invitations_number +
            '</span>'
    } else {
        button.innerHTML = '<i class="fas fa-bell"></i>'
    }
}

function markAllAsRead() {
    let data = {
        action: "deleteAllNotifications"
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
            let notifications = $('.notification')

            for (let i = 0; i < notifications.length; i++) {
                let notification = notifications[i]
                notification.remove()

                stylizeNotification(notification)
                setBadgeNumber(0)
            }

            $("#notificationsList")[0].innerHTML = '<div class="empty text-primary">Vous n\'avez pas de notification...</div>'
        })
        .catch(error => {
            console.error('Error:', error);
            displayAlert("ERROR", "Une erreur est survenue.")
        });
}

