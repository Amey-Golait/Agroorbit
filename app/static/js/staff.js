$(document).ready(function () {
    var staffModal = new bootstrap.Modal(document.getElementById('staffModal'));

    $('#addStaffBtn').on('click', function () {
        $('#staffForm')[0].reset();
        $('#staff_id').val('');
        $('#staffModalLabel').text('Add Staff');
        staffModal.show();
    });

    $(document).on('click', '.editStaffBtn', function () {
        const id = $(this).data('id');
        $.getJSON(`/staff/${id}`, function (data) {
            $('#staff_id').val(data.id);
            $('#name').val(data.name);
            $('#email').val(data.email);
            $('#phone').val(data.phone);
            $('#city').val(data.city);
            $('#role').val(data.role);
            $('#manager_name').val(data.manager_name);
            $('#password').val('');
            $('#staffModalLabel').text('Edit Staff');
            staffModal.show();
        }).fail(function () {
            alert('Failed to load staff data.');
        });
    });

    $("#staffForm").on("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        const rawId = formData.get("staff_id");
        const id = rawId && !isNaN(rawId) && rawId !== "" ? parseInt(rawId) : null;

        let url = "/staff/";
        let method = "POST";

        if (id) {
            url = `/staff/${id}`;
            method = "PUT";
        }

        $.ajax({
            url: url,
            type: method,
            data: formData,
            processData: false,
            contentType: false,
            success: function () {
                staffModal.hide();
                window.location.reload(); 
            },
            error: function (xhr) {
                alert("Error: " + xhr.responseText);
            }
        });
    });

    $(".delete-btn").on("click", function () {
        const id = $(this).data("id");
        if (confirm("Are you sure you want to delete this staff?")) {
            $.ajax({
                url: `/staff/${id}`,
                type: "DELETE",
                success: function () {
                    window.location.reload();
                },
                error: function (xhr) {
                    alert("Error deleting staff: " + xhr.responseText);
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
            alert("No staff selected for deletion.");
            return;
        }

        if (confirm(`Delete ${ids.length} staff?`)) {
            const formData = new FormData();
            ids.forEach(id => formData.append("staff_ids", id));

            $.ajax({
                url: "/staff/bulk_delete",
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
