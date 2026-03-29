from src.core.renderer import Renderer


def main():
    html_template = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <style>
        @font-face {
            font-family: 'RegularFont';
            src: url('{{ resource_path }}/fnt.ttf') format('truetype');
        }
        @font-face {
            font-family: 'BoldFont';
            src: url('{{ resource_path }}/fntb.ttf') format('truetype');
        }
        body {
            font-family: 'RegularFont', sans-serif;
            width: 210mm;
            margin: 20mm auto;
            padding: 0 10mm;
            background: white;
            color: black;
            line-height: 1.4;
        }
        .bold { font-family: 'BoldFont', sans-serif; }
        .header {
            display: flex;
            align-items: center;
            gap: 15px;
            border-bottom: 1px solid #ccc;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .header img { height: 70px; }
        .header-text { font-size: 11pt; }
        .title {
            font-size: 18pt;
            font-family: 'BoldFont', sans-serif;
            text-align: left;
            margin: 2px 0;
        }
        .content { font-size: 12pt; }
        .signature {
            margin-top: 30px;
            display: flex;
            justify-content: space-between;
        }
        .vacations { margin: 15px 0; }
        .personal-info {
            text-align: center;
            margin-bottom: 10px
        }
    </style>
</head>
<body>
    <div class="header">
        <img src="{{ resource_path }}/sesc_urfu_logo.jpg" alt="Логотип">
        <div class="header-text">
            Министерство науки и высшего образования РФ<br>
            ФГАОУ ВО «УрФУ имени первого Президента России Б.Н. Ельцина»<br>
            Специализированный учебно-научный центр<br>
            Данилы Зверева ул., 30, Екатеринбург 620137<br>
            Тел./факс +7 343 341-06-59. E-mail lyceum@urfu.ru<br>
            ОКПО 02069208 ОГРН 1026604939855 ИНН/КПП 6660003190/667001001
        </div>
    </div>

    <div class="title">СПРАВКА</div>

    <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
        <span>{{ certificate_date }}         № {{ certificate_number }}</span>
        <span>Территориальный орган 
            Социального фонда России по 
            месту жительства</span>
    </div>

    <div class="content">
        <p class="personal-info">
            <span class="bold">{{ fio }}, рожд. {{ birth_date }}</span>
        </p>
        <p>
            является учащимся {{ class }} класса школы-интерната Специализированного учебно-научного центра
            ФГАОУ ВО «Уральский федеральный университет имени первого Президента России Б.Н. Ельцина» (СУНЦ УрФУ).
        </p>
        <p>Форма обучения — очная, дневная. Срок обучения — с {{ start_date }} по {{ end_date }}.<br>
        Приказ о зачислении от {{ order_date }} № {{ order_number }}.<br>
        График каникул в 2022/2023 учебном году:</p>
        <ul class="vacations">
            {% for v in vacations %}
            <li>с {{ v.start }} по {{ v.end }};</li>
            {% endfor %}
        </ul>
        <p>
            СУНЦ УрФУ соответствует статусу общеобразовательной школы и осуществляет образовательную деятельность
            по основным общеобразовательным программам; свидетельство о государственной аккредитации от 14.03.2019 № 3017,
            срок действия — бессрочно, выдано Федеральной службой по надзору в сфере образования и науки.
        </p>
    </div>

    <div class="signature">
        <div>Академический директор</div>
        <div>{{ academic_director }}</div>
    </div>
</body>
</html>
"""

    info = {
        "resource_path": "",  
        "fio": "Пушкинов Александр Сергеевич",
        "birth_date": "06.06.1799",
        "class": "8А",
        "start_date": "01.09.2022",
        "certificate_date": "16.09.2022",
        "certificate_number": "1",
        "end_date": "30.06.2023",
        "order_date": "27.06.2022",
        "order_number": "444/05",
        "vacations": [
            {"start": "30.10.2022", "end": "06.11.2022"},
            {"start": "30.12.2022", "end": "08.01.2023"},
            {"start": "19.03.2023", "end": "30.03.2023"}
        ],
        "academic_director": "М. С. Рябцев"
    }

    renderer = Renderer()
    renderer.render(html_template, info)


if __name__ == "__main__":
    main()