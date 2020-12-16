/**
 * Script pour les activités.
 * Nécessite :
 * JQuery (Slim supporté)
 * Anime.js
 */

import {alert} from './modules/alerts.js'

$(document).ready(function () {
    $(function () {
        addEventsListeners()
    })

    function addEventsListeners() {
        let activities = $(".infocard")

        for (let i = 0; i < activities.length; i++) {
            //activities[i].addEventListener('click', activityClickListener);
            // TODO revoir comment faire l'UX
        }
    }

    function activityClickListener(event) {
        let modal = $('#activityModal')

        let targetActivity = $(event.currentTarget)
        let activityId = targetActivity.data('activityId')


        let request = new XMLHttpRequest()

        request.open('GET', '/api/activity/' + activityId, true)

        request.onload = function () {
            let data = JSON.parse(this.response)

            if (request.status >= 200 && request.status < 400) {
                console.log(data)
                let modalHeader = modal.find('#activityModalTitle')[0]
                modalHeader.innerHTML = data.name



                modal.modal('show')
            } else {
                alert('ERROR', "Une erreur s'est produite lors de la réception des données.")
            }
        }

        request.send()
    }

    function resetModal() {

    }
})