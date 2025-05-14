$(document).ready(function() {
    $('#ahpForm').on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            url: '/ahp',
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                let resultHtml = '<h3>Kết quả AHP</h3>';
                resultHtml += '<p><strong>Trọng số tiêu chí:</strong> Mức lương tối thiểu: ' + response.criteria_weights[0].toFixed(3) + ', Tổng chi phí: ' + response.criteria_weights[1].toFixed(3) + '</p>';
                resultHtml += '<table class="table table-bordered"><thead><tr><th>Vùng</th><th>Điểm</th></tr></thead><tbody>';
                response.result.forEach(function(item) {
                    resultHtml += '<tr><td>' + item.region + '</td><td>' + item.score.toFixed(3) + '</td></tr>';
                });
                resultHtml += '</tbody></table>';
                resultHtml += '<p><strong>Vùng tốt nhất:</strong> ' + response.result[0].region + ' (Điểm: ' + response.result[0].score.toFixed(3) + ')</p>';
                $('#result').html(resultHtml);
            },
            error: function(error) {
                $('#result').html('<p class="text-danger">Có lỗi xảy ra, vui lòng thử lại!</p>');
            }
        });
    });
});