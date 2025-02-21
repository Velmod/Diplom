document.getElementById('rental-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const location = document.getElementById('location').value;
    const price = document.getElementById('price').value;

    const rentalList = document.getElementById('rental-list');
    const listItem = document.createElement('li');
    listItem.textContent = `${name} - ${location} - ${price} руб./мес.`;
    rentalList.appendChild(listItem);

    // Очистить форму
    this.reset();
});
