let formData = new FormData($('#orderForm')[0]);

$.ajax({
    url: '/orders/',
    type: 'POST',
    data: formData,
    processData: false,
    contentType: false,
    ...
});


$('#saveOrderBtn').click(function () {
    const orderId = $('#order_id').val();
    const url = orderId ? `/orders/${orderId}` : '/orders/';
    const method = orderId ? 'PUT' : 'POST';

    const data = {
        customer_id: parseInt($('#customer_id').val()),
        product_id: parseInt($('#product_id').val()),
        quantity: parseInt($('#quantity').val())
    };

    $.ajax({
        url: url,
        type: method,
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function () {
            $('#orderModal').modal('hide');
            loadOrders();
        },
        error: function (xhr) {
            console.error("Error:", xhr.responseText);
        }
    });
});
