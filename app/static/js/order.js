$(document).ready(function () {
  const orderModal = new bootstrap.Modal(document.getElementById('orderModal'));
  let allProducts = [];

  function loadCustomersDropdown(selectedId = null) {
    $.ajax({
      url: '/customers/?skip=0&limit=1000',
      type: 'GET',
      success: function (customers) {
        const $dropdown = $('#customer_id').empty().append('<option value="">Select Customer</option>');
        customers.forEach(c => {
          const sel = selectedId == c.id ? 'selected' : '';
          $dropdown.append(`<option value="${c.id}" ${sel}>${c.name}</option>`);
        });
      }
    });
  }

  function loadAllProducts(cb) {
    if (allProducts.length) return cb();
    $.get('/products/?skip=0&limit=1000', products => {
      allProducts = products;
      cb();
    });
  }

  function addProductRow(pid = '', qty = '') {
    const options = allProducts.map(p =>
      `<option value="${p.id}" ${p.id==pid?'selected':''}>${p.product_name}</option>`
    ).join('');
    $('#productContainer').append(`
      <div class="input-group mb-2">
        <select class="form-select product-select" required>
          <option value="">Select Product</option>${options}
        </select>
        <input type="number" class="form-control quantity-input" min="1" placeholder="Qty" value="${qty}" required>
        <button type="button" class="btn btn-danger removeProductRowBtn">&times;</button>
      </div>
    `);
  }

  $(document).on('click', '.removeProductRowBtn', function(){
    $(this).closest('.input-group').remove();
  });

  $('#addProductRowBtn').click(() => addProductRow());

  $('#addOrderBtn').click(function(){
    $('#orderForm')[0].reset();
    $('#order_id').val('');
    loadCustomersDropdown();
    loadAllProducts(() => {
      $('#productContainer').empty();
      addProductRow();
    });
    $('#orderModalLabel').text('Add Order');
    orderModal.show();
  });

  $(document).on('click', '.editOrderBtn', function(){
    const id = $(this).data('id');
    $.get(`/orders/${id}`, order => {
      $('#order_id').val(order.id);
      $('#delivery_date').val(order.delivery_date);
      $('#order_status').val(order.order_status);
      $('#payment_status').val(order.payment_status);
      $('#payment_mode').val(order.payment_mode);
      $('#tax_percent').val(order.tax_percent);
      $('#discount').val(order.discount);
      $('#discount_type').val(order.discount_type);
      $('#shipping_charge').val(order.shipping_charge);

      loadCustomersDropdown(order.customer_id);
      loadAllProducts(() => {
        $('#productContainer').empty();
        if (order.order_items.length) {
          order.order_items.forEach(item => addProductRow(item.product_id, item.quantity));
        } else {
          addProductRow();
        }
      });

      $('#orderModalLabel').text('Edit Order');
      orderModal.show();
    });
  });

  $('#orderForm').submit(function(e){
    e.preventDefault();

    const customerId = $('#customer_id').val();
    if (!customerId) return alert('Select a customer.');

    const pids = [], qtys = [];
    let valid = true;

    $('#productContainer .input-group').each(function(){
      const pid = $(this).find('.product-select').val();
      const q   = $(this).find('.quantity-input').val();
      if (!pid || !q || q <= 0) {
        alert('Each product row needs a product and valid quantity.');
        valid = false;
        return false;
      }
      pids.push(pid);
      qtys.push(q);
    });
    if (!valid) return;

    const formData = new FormData();
    formData.append('customer_id', customerId);
    formData.append('delivery_date', $('#delivery_date').val());
    formData.append('order_status', $('#order_status').val());
    formData.append('payment_status', $('#payment_status').val());
    formData.append('payment_mode', $('#payment_mode').val());
    formData.append('tax_percent', $('#tax_percent').val());
    formData.append('discount', $('#discount').val());
    formData.append('discount_type', $('#discount_type').val());
    formData.append('shipping_charge', $('#shipping_charge').val());

    formData.append('product_id', pids.join(','));
    formData.append('quantity',   qtys.join(','));

    const id = $('#order_id').val();
    const url = id ? `/orders/${id}` : '/orders/';
    const method = id ? 'PUT' : 'POST';

    $.ajax({
      url, method,
      data: formData,
      processData: false,
      contentType: false,
      success: () => {
        orderModal.hide();
        location.reload();
      },
      error: xhr => alert('Error: ' + xhr.responseText)
    });
  });

  $(".delete-btn").on("click", function () {
        const id = $(this).data("id");
        if (confirm("Are you sure you want to delete this order?")) {
            $.ajax({
                url: `/orders/${id}`,
                type: "DELETE",
                success: function () {
                    window.location.reload();
                },
                error: function (xhr) {
                    alert("Error deleting order: " + xhr.responseText);
                }
            });
        }
    });

    $("#selectAll").on("change", function () {
        $(".selectBox").prop("checked", this.checked);
    });

    $("#bulkDeleteBtn").on("click", function () {
        const ids = $(".selectBox:checked").map(function () {
            return $(this).val();
        }).get();

        if (ids.length === 0) {
            alert("No order selected for deletion.");
            return;
        }

        if (confirm(`Delete ${ids.length} order?`)) {
            const formData = new FormData();
            ids.forEach(id => formData.append("order_ids", id));

            $.ajax({
                url: "/orders/bulk_delete",
                type: "POST",
                data: formData,
                processData: false,
                contentType: false,
                success: function () {
                    window.location.reload();
                },
                error: function (xhr) {
                    alert("Error during bulk delete: " + xhr.responseText);
                }
            });
        }
    });

});
