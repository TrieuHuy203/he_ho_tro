# from flask import Flask, render_template, request, jsonify
# import numpy as np

# app = Flask(__name__)

# # Dữ liệu cứng (hard-coded) về vùng lương tối thiểu và chi phí bảo hiểm
# regions_data = [
#     {"name": " Bảo Việt Nhân Thọ", "min_salary": 4680000, "bhyt_cost": 210600, "bhxh_cost": 1193400, "total_cost": 1497600},
#     {"name": " Prudential Việt Nam", "min_salary": 4160000, "bhyt_cost": 187200, "bhxh_cost": 1060800, "total_cost": 1331200},
#     {"name": " Dai-ichi Việt Nam", "min_salary": 3640000, "bhyt_cost": 163800, "bhxh_cost": 928200, "total_cost": 1164800},
#     {"name": " Hanwha Life Việt Nam", "min_salary": 3250000, "bhyt_cost": 146250, "bhxh_cost": 828750, "total_cost": 1040000},
# ]

# # Hàm tính toán AHP
# def calculate_ahp(criteria_matrix, alternatives_matrices):
#     # Bước 1: Chuẩn hóa ma trận tiêu chí
#     criteria_matrix = np.array(criteria_matrix)
#     criteria_sum = criteria_matrix.sum(axis=0)
#     normalized_criteria = criteria_matrix / criteria_sum
#     criteria_weights = normalized_criteria.mean(axis=1)

#     # Bước 2: Chuẩn hóa ma trận phương án cho từng tiêu chí
#     alternatives_weights = []
#     for alt_matrix in alternatives_matrices:
#         alt_matrix = np.array(alt_matrix)
#         alt_sum = alt_matrix.sum(axis=0)
#         normalized_alt = alt_matrix / alt_sum
#         alt_weights = normalized_alt.mean(axis=1)
#         alternatives_weights.append(alt_weights)

#     # Bước 3: Tính điểm cuối cùng cho từng phương án
#     alternatives_weights = np.array(alternatives_weights).T  # Chuyển vị để nhân ma trận
#     final_scores = alternatives_weights.dot(criteria_weights)

#     return criteria_weights, final_scores

# @app.route('/')
# def index():
#     return render_template('index.html', regions=regions_data)


# @app.route('/main')
# def main():
#     return render_template('home.html', regions=regions_data)

# @app.route('/compare')
# def compare():
#     return render_template('compare.html', regions=regions_data)

# @app.route('/data-entry')
# def data_entry():
#     return render_template('data entry.html', regions=regions_data)

# @app.route('/propose')
# def propose():
#     return render_template('propose.html', regions=regions_data)

# @app.route('/report')
# def report():
#     return render_template('report.html', regions=regions_data)

# @app.route('/show-data')
# def show_data():
#     return render_template('show data.html', regions=regions_data)

# @app.route('/support')
# def support():
#     return render_template('support.html', regions=regions_data)

# @app.route('/trend')
# def trend():
#     return render_template('trend.html', regions=regions_data)

# @app.route('/update-user')
# def update_user():
#     return render_template('update user.html', regions=regions_data)

# @app.route('/user-management')
# def user_management():
#     return render_template('user management.html', regions=regions_data)




# @app.route('/ahp', methods=['GET', 'POST'])
# def ahp():
#     if request.method == 'POST':
#         # Lấy dữ liệu từ form
#         criteria_matrix = [
#             [float(request.form[f'criteria_{i}_{j}']) for j in range(2)]
#             for i in range(2)
#         ]

#         # Ma trận so sánh từng cặp cho từng tiêu chí (4 vùng)
#         alternatives_matrices = []
#         for crit in range(2):  # 2 tiêu chí: min_salary và total_cost
#             alt_matrix = [
#                 [float(request.form[f'alt_{crit}_{i}_{j}']) for j in range(4)]
#                 for i in range(4)
#             ]
#             alternatives_matrices.append(alt_matrix)

#         # Tính toán AHP
#         criteria_weights, final_scores = calculate_ahp(criteria_matrix, alternatives_matrices)

#         # Tạo kết quả
#         result = [
#             {"region": regions_data[i]["name"], "score": final_scores[i]}
#             for i in range(len(regions_data))
#         ]
#         result = sorted(result, key=lambda x: x['score'], reverse=True)

#         return jsonify({
#             "criteria_weights": criteria_weights.tolist(),
#             "final_scores": final_scores.tolist(),
#             "result": result
#         })
#     return render_template('ahp.html', regions=regions_data)

# if __name__ == '__main__':
#     app.run(debug=True)from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Dữ liệu đầu vào (ma trận so sánh cặp cho các tiêu chí)
criteria_matrix = np.array([
    [1, 3, 5, 7, 9],
    [1/3, 1, 3, 5, 7],
    [1/5, 1/3, 1, 3, 5],
    [1/7, 1/5, 1/3, 1, 3],
    [1/9, 1/7, 1/5, 1/3, 1]
])

# Ma trận so sánh cặp cho các phương án dưới mỗi tiêu chí
insurance_comparison_matrices = {
    'Chi phí & mức phí bảo hiểm': np.array([
        [1, 3, 5, 7],
        [1/3, 1, 3, 5],
        [1/5, 1/3, 1, 3],
        [1/7, 1/5, 1/3, 1]
    ]),
    'Phạm vi bảo hiểm': np.array([
        [1, 1/3, 1/5, 1/7],
        [3, 1, 1/3, 1/5],
        [5, 3, 1, 1/3],
        [7, 5, 3, 1]
    ]),
    'Uy tín & đánh giá': np.array([
        [1, 5, 3, 7],
        [1/5, 1, 1/3, 3],
        [1/3, 3, 1, 5],
        [1/7, 1/3, 1/5, 1]
    ]),
    'Dịch vụ khách hàng': np.array([
        [1, 7, 5, 3],
        [1/7, 1, 1/3, 1/5],
        [1/5, 3, 1, 1/3],
        [1/3, 5, 3, 1]
    ]),
    'Điều khoản hợp đồng': np.array([
        [1, 3, 7, 5],
        [1/3, 1, 5, 3],
        [1/7, 1/5, 1, 1/3],
        [1/5, 1/3, 3, 1]
    ])
}

# Hàm tính toán trọng số từ ma trận so sánh
def calculate_weights(matrix):
    # Tính tổng theo cột
    column_sum = np.sum(matrix, axis=0)
    
    # Chuẩn hóa ma trận
    normalized_matrix = matrix / column_sum
    
    # Tính trọng số bằng trung bình các hàng
    weights = np.mean(normalized_matrix, axis=1)
    
    return weights

# Hàm tính toán điểm cho các phương án dựa trên trọng số
def calculate_scores(weighted_matrix, weights):
    scores = np.dot(weighted_matrix, weights)
    return scores

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Tính trọng số của các tiêu chí
    weights = calculate_weights(criteria_matrix)
    
    # Tính điểm cho các phương án dựa trên trọng số của mỗi tiêu chí
    scores = {}
    for criterion, matrix in insurance_comparison_matrices.items():
        normalized_matrix = matrix / np.sum(matrix, axis=0)
        scores[criterion] = calculate_scores(normalized_matrix, weights)
    
    # Vẽ biểu đồ các điểm
    fig, ax = plt.subplots(figsize=(8, 6))
    for criterion, score in scores.items():
        ax.plot(['Bảo Việt Nhân Thọ', 'Prudential Việt Nam', 'Dai-ichi Việt Nam', 'Hanwha Life Việt Nam'],
                score, label=criterion)

    ax.set_xlabel('Các công ty bảo hiểm')
    ax.set_ylabel('Điểm')
    ax.set_title('So sánh các công ty bảo hiểm theo tiêu chí')
    ax.legend()
    
    # Lưu đồ thị vào bộ nhớ và chuyển đổi sang base64 để hiển thị trên trang web
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf8')
    
    return render_template('result.html', img_data=img_base64)

if __name__ == '__main__':
     app.run(debug=True, port=5004)  # Change 5001 to any available port
