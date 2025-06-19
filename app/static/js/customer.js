$(document).ready(function () {
    var customerModal = new bootstrap.Modal(document.getElementById('customerModal'));

    $('#addCustomerBtn').on('click', function () {
        $('#customerForm')[0].reset();
        $('#customer_id').val('');
        $('#customerModalLabel').text('Add Customer');
        customerModal.show();
    });

    $(document).on('click', '.editCustomerBtn', function () {
        const id = $(this).data('id');
        $.get(`/customers/${id}`, function (data) {
            $('#customer_id').val(data.id);
            $('#name').val(data.name);
            $('#firm_name').val(data.firm_name);
            $('#phone').val(data.phone);
            $('#email').val(data.email);
            $('#pan_no').val(data.pan_no);
            $('#user_type').val(data.user_type);
            $('#address').val(data.address);
            $('#licence_no').val(data.licence_no);
            $('#licence_expiry_date').val(data.licence_expiry_date);
            $('#password').val('');
            customerModal.show();
        }).fail(function () {
        alert('Failed to load customer data.');
        });
    });

    $("#customerForm").on("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        const rawId = formData.get("customer_id");
        const id = rawId && !isNaN(rawId) && rawId !== "" ? parseInt(rawId) : null;

        let url = "/customers/";
        let method = "POST";

        if (id) {
            url = `/customers/${id}`;
            method = "PUT";
        }

        $.ajax({
            url: url,
            type: method,
            data: formData,
            processData: false,
            contentType: false,
            success: function () {
                customerModal.hide();
                window.location.reload(); 
            },
            error: function (xhr) {
                alert("Error: " + xhr.responseText);
            }
        });
    });

    $(".delete-btn").on("click", function () {
        const id = $(this).data("id");
        if (confirm("Are you sure you want to delete this customer?")) {
            $.ajax({
                url: `/customers/${id}`,
                type: "DELETE",
                success: function () {
                    window.location.reload();
                },
                error: function (xhr) {
                    alert("Error deleting customer: " + xhr.responseText);
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
            alert("No customer selected for deletion.");
            return;
        }

        if (confirm(`Delete ${ids.length} customer?`)) {
            const formData = new FormData();
            ids.forEach(id => formData.append("customer_ids", id));

            $.ajax({
                url: "/customers/bulk_delete",
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
