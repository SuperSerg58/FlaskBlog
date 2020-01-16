from flask import Blueprint, render_template, request
from collections import Counter
import re

blueprint = Blueprint('logs', __name__, url_prefix='/logs')


@blueprint.route('/', methods=['POST', 'GET'])
def logs():
    if request.method == 'POST':
        f = request.files['file'].read()  # получаем битовый вид файла
        txt = str(f.decode('utf-8'))  # Чтобы получить строковый вид из файла

        pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        ips = re.findall(pattern, txt)
        result = Counter(ips).most_common(10)  # список кортежей из двух элементов

        ban = []
        for key, value in result:
            if value > 100:
                ban.append({'ip': key,
                            'frequency': value})

        return render_template('analizelog/log.html', ips=ban)

    return render_template('analizelog/log.html')
