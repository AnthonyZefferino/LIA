$(document).ready(function () {
    var companyApiEndpoint = '/aziende/companies/api/';

// Richiedi la lista delle company dall'API.
    function getApiData(apiUrl, callback) {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", apiUrl, true);
        xhr.responseType = "json";
        xhr.onload = function () {
            var status = xhr.status;
            if (status === 200) {
                callback(null, xhr.response);
            } else {
                callback(status, xhr.response);
            }
        };
        xhr.send();
    };

// Ottieni i dati JSON delle compagnie.
    getApiData(companyApiEndpoint, function (err, data) {
        if (err !== null) {
            console.log("Something went wrong: " + err);
        } else {
            // Si presume che 'data' sia un array di oggetti con proprietà corrispondenti ai tuoi modelli Django.
            loadCompanyDataToTable(data);
        }
    });

    function loadCompanyDataToTable(datas) {
        var detailUrlTemplate = $('#company-table').data('detail-url').replace('PLACEHOLDER', '%s');
        var editUrlTemplate = $('#company-table').data('edit-url').replace('PLACEHOLDER', '%s');
        table = $('#company-table').DataTable({
            data: datas,
            dom: 'Bfrtip',
            select: true,
            searchBuilder: {
                columns: [1, 2, 3, 4, 5, 6],
                button: 'Ricerca Avanzata',
            },
            language: {
                url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/it-IT.json',
            },
            fixedHeader: true,
            buttons: [
                'copy',
                {
                    extend: 'print',
                    customize: function (win) {
                        $(win.document.body)
                            .css('font-size', '10pt')
                            .css('padding', '30pt')
                            .prepend(
                                '<img src="http://127.0.0.1:8000/static/images/logo-light.png" style="position:absolute; top:0; left:0;height: 30px" />'
                            );

                        $(win.document.body).find('table')
                            .addClass('compact')
                            .addClass('table')
                            .addClass('table-condensed')
                            .css('font-size', 'inherit');
                    }
                },
                {
                    extend: 'spacer',
                    style: 'bar',
                    text: 'Export files:'
                },
                'csv',
                'excel',
                'spacer',
                'pdf',
                'spacer',
                {
                    extend: 'spacer',
                    style: 'bar',
                    text: 'Ricerca:'
                },
                'searchBuilder'
            ],
            order: [[0, 'desc']],
            columns: [
                {data: "name"},
                {data: "macro_switch"},
                {data: "industry.name"},
                {data: "sector.name"},
                {data: "email"},
                {data: "phone_mobile"},
                {data: "phone_number"},

                {
                    data: "address",
                    render: function (data, type, full) {
                        return isDescriptionLegh(full.address);
                    },
                },
                {data: "website"},
                {
                    data: "description",
                    render: function (data, type, full) {
                        return isDescriptionLegh(full.description);
                    },
                },
                {
                    data: null,
                    'bSortable': false,
                    render: function (data, type, full) {
                        var detailUrl = $('#company-table').data('detail-url').replace('0', full.id);
                        var editUrl = $('#company-table').data('edit-url').replace('0', full.id);
                        return '<ul class="list-unstyled hstack gap-1 mb-0">\
                            <li data-bs-toggle="tooltip" data-bs-placement="top" data-bs-title="View">\
                                <a href="' + detailUrl + '" class="btn btn-sm btn-soft-primary" target="_blank"><i class="mdi mdi-eye-outline"></i></a>\
                            </li>\
                            <li data-bs-toggle="tooltip" data-bs-placement="top" data-bs-title="Edit">\
                                <a href="' + editUrl + '" class="btn btn-sm btn-soft-info" target="_blank"><i class="mdi mdi-pencil-outline"></i></a>\
                            </li>\
                            <li data-bs-toggle="tooltip" data-bs-placement="top" data-bs-title="Delete">\
                                <a href="#CompanyDelete" data-bs-toggle="modal" class="btn btn-sm btn-soft-danger"><i class="mdi mdi-delete-outline"></i></a>\
                            </li>\
                        </ul>';
                    },
                },
            ]
        });

        table.on('click', 'tbody tr', function (e) {
            e.currentTarget.classList.toggle('selected');
        });

        document.querySelector('#button').addEventListener('click', function () {
            alert(table.rows('.selected').data().length + ' row(s) selected');
        });
        $('#company-table').on('click', '.btn-soft-danger', function () {
            var rowData = table.row($(this).parents('tr')).data();
            $('#company-to-delete-name').text(rowData.name);
            $('#confirm-delete').off('click').on('click', function () {
                performDelete(rowData.id);
            });
        });

        function isDescriptionLegh(description) {
            // Taglia la stringa a 150 caratteri o 30 parole e aggiungi '...'
            const maxChars = 50;
            const maxWords = 10;

            if (description.length > maxChars) {
                return description.substring(0, maxChars) + '...';
            }

            let words = description.split(' ');
            if (words.length > maxWords) {
                // Unisci le prime 30 parole e aggiungi '...'
                return words.slice(0, maxWords).join(' ') + '...';
            }

            return description;
        }

        $('.dataTables_paginate').addClass('pagination-rounded');
    }

    function performDelete(companyId) {
        // La funzione per eseguire la cancellazione dal database si attiva dal modal
        var deleteEndpoint = '/aziende/companies/api/delete/' + companyId + '/';

        fetch(deleteEndpoint, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')  // Assicurati che il cookie CSRFToken sia disponibile
            }
        }).then(response => {
            if (response.ok) {
                // Rimuovi la riga dalla DataTable e nascondi il modal
                $('#company-table').DataTable().row($(`button[data-company-id="${companyId}"]`).parents('tr')).remove().draw();
                $('#CompanyDelete').modal('hide');
                alert('{% trans "Company deleted successfully." %}');
            } else {
                alert('{% trans "Error deleting company." %}');
            }
        }).catch(error => console.error('Error:', error));
    }


    if ($.fn.DataTable.isDataTable('#company-table')) {
        $('#company-tablet').DataTable().destroy();
    }
});