$(function(){
  const productModal = new bootstrap.Modal($('#productModal')[0]);

  $('#addProductBtn').click(() => {
    $('#productForm')[0].reset();
    $('#product_id').val('');
    $('#productModalLabel').text('Add Product');
    productModal.show();
  });

  $(document).on('click', '.editProductBtn', function(){
    const id = $(this).data('id');
    $.get(`/products/${id}`, data => {
      $('#product_id').val(data.id);
      $('#product_name').val(data.product_name);
      $('#product_code').val(data.product_code);
      $('#category').val(data.category);
      $('#brand').val(data.brand);
      $('#unit_price').val(data.unit_price);
      $('#box_price').val(data.box_price);
      $('#cash_on_delivery').val(data.cash_on_delivery);
      $('#published').val(data.published);
      // file inputs are not prefilled
      $('#productModalLabel').text('Edit Product');
      productModal.show();
    }).fail(() => alert('Failed loading product'));
  });

  $('#productForm').submit(function(e){
    e.preventDefault();
    const formData = new FormData(this);
    const id = formData.get('product_id');
    const method = id ? 'PUT' : 'POST';
    const url = id ? `/products/${id}` : '/products/';

    ['unit_price', 'box_price', 'cash_on_delivery', 'published'].forEach(field => {
  const value = formData.get(field);
    if (value === '') {
      formData.delete(field);
    }
  });

    $.ajax({
      url, type: method, data: formData,
      processData: false, contentType: false,
      success: () => window.location.reload(),
      error: xhr => alert('Error: ' + xhr.responseText),
    });
  });

  $('.deleteProductBtn').click(function(){
    const id = $(this).data('id');
    if(confirm('Delete this product?')){
      $.ajax({
        url: `/products/${id}`, type:'DELETE',
        success: () => window.location.reload(),
        error: xhr => alert('Delete error: ' + xhr.responseText),
      });
    }
  });

  $('#selectAll').change(function(){
    $('.selectBox').prop('checked', this.checked);
  });

  $('#bulkDeleteBtn').click(function(){
    const ids = $('.selectBox:checked').map((_,el)=> el.value ).get();
    if(!ids.length) return alert('No products selected');
    if(confirm(`Delete ${ids.length} products?`)){
      const fd = new FormData();
      ids.forEach(id=> fd.append('product_id', id));
      $.ajax({
        url:'/products/bulk_delete', type:'POST',
        data:fd, processData:false, contentType:false,
        success: () => window.location.reload(),
        error: xhr => alert('Bulk delete error: ' + xhr.responseText),
      });
    }
  });

  $('#downloadCsvBtn').click(() => {
    window.location = '/products/download/csv';
  });
});
