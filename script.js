// static/script.js
// Autocomplete for movie titles
fetch('/titles')
    .then(res => res.json())
    .then(data => {
        const datalist = document.getElementById('titleSuggestions');
        data.forEach(title => {
            let option = document.createElement('option');
            option.value = title;
            datalist.appendChild(option);
        });
    });

// Submit movie form
document.getElementById('movieForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const movieName = document.getElementById('movieName').value;

    fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ movie: movieName })
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('recommendations');
        resultDiv.innerHTML = '<h2>Recommended Movies:</h2><ul>' +
            data.recommendations.map(movie => `<li>${movie}</li>`).join('') + '</ul>';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
