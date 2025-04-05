document.getElementById('billing-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    fetch('/bill', {
        method: 'POST',
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            const resultDiv = document.getElementById('result');
            if (data.error) {
                alert(data.error);
                return;
            }

            resultDiv.innerHTML = `
                <h3>Order Summary</h3>
                <p><strong>Item:</strong> ${data.item_name}</p>
                <p><strong>Quantity:</strong> ${data.quantity}</p>
                <p><strong>Total Cost:</strong> ₹${data.total}</p>
            `;
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Something went wrong. Please try again.');
        });
});
