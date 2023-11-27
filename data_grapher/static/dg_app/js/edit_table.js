function addRow() {
    var newRow = $('<tr>');
    $('thead th').each(function() {
        newRow.append('<td contenteditable="true"></td>');
    });
    $('tbody').append(newRow);
}

function addColumn() {
    $('thead tr').append('<th contenteditable="true"></th>');
    $('tbody tr').each(function() {
        $(this).append('<td contenteditable="true"></td>');
    });
}

function deleteRow() {
    $('tbody tr:last').remove();
}

function deleteColumn() {
    $('thead th:last').remove();
    $('tbody tr').each(function() {
        $(this).find('td:last').remove();
    });
}

function getColumns() {
    var headers = document.querySelectorAll('thead th[contenteditable="true"]');
    return Array.from(headers).map(function (header) {
        return header.textContent.trim();
    });
}

function getResults() {
    var rows = document.querySelectorAll('tbody tr');
    var results = [];

    rows.forEach(function (row) {
        var rowData = [];
        var cells = row.querySelectorAll('td[contenteditable="true"]');
        
        cells.forEach(function (cell) {
            rowData.push(cell.textContent.trim());
        });

        results.push(rowData);
    });

    return results;
}

function saveChanges() {
    var url = $('button[data-url]').data('url');
    var data = {
        "columns": getColumns(),
        "results": getResults()
    };
    
    var csrfToken = $('[name=csrfmiddlewaretoken]').val();

    $.ajax({
        type: "POST",
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        headers: {
            'X-CSRFToken': csrfToken
        },
        dataType: "JSON",
        success: function (response) {
            // Handle success response
            if (response.status === 'success') {
                // Handle the success response, e.g., show a success message
                console.log('Data saved successfully!');
                
                // Redirect to the specified URL
                window.location.href = response.redirect_url;
            } else {
                // Handle other cases if needed
                console.error('Data saving failed:', response);
            }
        },
        error: function (error) {
            // Handle error
            console.log(error);
        }
    });
}