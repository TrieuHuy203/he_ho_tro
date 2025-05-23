from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

# Dữ liệu cứng (hard-coded) về vùng lương tối thiểu và chi phí bảo hiểm
regions_data = [
    {"name": " Bảo Việt Nhân Thọ", "min_salary": 4680000, "bhyt_cost": 210600, "bhxh_cost": 1193400, "total_cost": 1497600},
    {"name": " Prudential Việt Nam", "min_salary": 4160000, "bhyt_cost": 187200, "bhxh_cost": 1060800, "total_cost": 1331200},
    {"name": " Dai-ichi Việt Nam", "min_salary": 3640000, "bhyt_cost": 163800, "bhxh_cost": 928200, "total_cost": 1164800},
    {"name": " Hanwha Life Việt Nam", "min_salary": 3250000, "bhyt_cost": 146250, "bhxh_cost": 828750, "total_cost": 1040000},
]

# Hàm tính toán AHP
def calculate_ahp(criteria_matrix, alternatives_matrices):
    # Bước 1: Chuẩn hóa ma trận tiêu chí
    criteria_matrix = np.array(criteria_matrix)
    criteria_sum = criteria_matrix.sum(axis=0)
    normalized_criteria = criteria_matrix / criteria_sum
    criteria_weights = normalized_criteria.mean(axis=1)

    # Bước 2: Chuẩn hóa ma trận phương án cho từng tiêu chí
    alternatives_weights = []
    for alt_matrix in alternatives_matrices:
        alt_matrix = np.array(alt_matrix)
        alt_sum = alt_matrix.sum(axis=0)
        normalized_alt = alt_matrix / alt_sum
        alt_weights = normalized_alt.mean(axis=1)
        alternatives_weights.append(alt_weights)

    # Bước 3: Tính điểm cuối cùng cho từng phương án
    alternatives_weights = np.array(alternatives_weights).T  # Chuyển vị để nhân ma trận
    final_scores = alternatives_weights.dot(criteria_weights)

    return criteria_weights, final_scores

@app.route('/')
def index():
    return render_template('index.html', regions=regions_data)


@app.route('/main')
def main():
    return render_template('home.html', regions=regions_data)

@app.route('/compare')
def compare():
    return render_template('compare.html', regions=regions_data)

@app.route('/data-entry')
def data_entry():
    return render_template('data entry.html', regions=regions_data)

@app.route('/propose')
def propose():
    return render_template('propose.html', regions=regions_data)

@app.route('/report')
def report():
    return render_template('report.html', regions=regions_data)

@app.route('/show-data')
def show_data():
    return render_template('show data.html', regions=regions_data)

@app.route('/support')
def support():
    return render_template('support.html', regions=regions_data)

@app.route('/trend')
def trend():
    return render_template('trend.html', regions=regions_data)

@app.route('/update-user')
def update_user():
    return render_template('update user.html', regions=regions_data)

@app.route('/user-management')
def user_management():
    return render_template('user management.html', regions=regions_data)




@app.route('/ahp', methods=['GET', 'POST'])
def ahp():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        criteria_matrix = [
            [float(request.form[f'criteria_{i}_{j}']) for j in range(2)]
            for i in range(2)
        ]

        # Ma trận so sánh từng cặp cho từng tiêu chí (4 vùng)
        alternatives_matrices = []
        for crit in range(2):  # 2 tiêu chí: min_salary và total_cost
            alt_matrix = [
                [float(request.form[f'alt_{crit}_{i}_{j}']) for j in range(4)]
                for i in range(4)
            ]
            alternatives_matrices.append(alt_matrix)

        # Tính toán AHP
        criteria_weights, final_scores = calculate_ahp(criteria_matrix, alternatives_matrices)

        # Tạo kết quả
        result = [
            {"region": regions_data[i]["name"], "score": final_scores[i]}
            for i in range(len(regions_data))
        ]
        result = sorted(result, key=lambda x: x['score'], reverse=True)

        return jsonify({
            "criteria_weights": criteria_weights.tolist(),
            "final_scores": final_scores.tolist(),
            "result": result
        })
    return render_template('ahp.html', regions=regions_data)

if __name__ == '__main__':
    app.run(debug=True)
