from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['DEBUG'] = True

FILENAME = 'mydir/shimeitokuten.xlsx'
FILEPATH = 'mydir/shimeitokuten.xlsx'

@app.route('/')
def preview():
    filename = FILENAME
    filepath = FILEPATH

    sheets_data = []

    if filename.endswith(('.xlsx', '.xls')):
        app.logger.debug('Excelファイルの処理を開始します')
        try:
            excel_file = pd.ExcelFile(filepath)
            for sheet_name in excel_file.sheet_names:
                app.logger.debug(f'シート "{sheet_name}" を処理中')
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                sheets_data.append({
                    'sheet_name': sheet_name,
                    'header': df.columns.tolist(),
                    'record': df.values.tolist()
                })
            app.logger.debug('Excelファイルの処理が完了しました')
        except Exception as e:
            app.logger.error(f'Excelファイルの処理中にエラーが発生しました: {str(e)}')
    elif filename.endswith('.csv'):
        app.logger.debug('CSVファイルの処理を開始します')
        try:
            df = pd.read_csv(filepath, encoding='utf-8')
            app.logger.debug('UTF-8エンコーディングでCSVファイルを読み込みました')
        except UnicodeDecodeError:
            app.logger.debug('UTF-8での読み込みに失敗しました。Shift-JISで試行します')
            try:
                df = pd.read_csv(filepath, encoding='shift-jis')
                app.logger.debug('Shift-JISエンコーディングでCSVファイルを読み込みました')
            except Exception as e:
                app.logger.error(f'CSVファイルの読み込み中にエラーが発生しました: {str(e)}')
                return render_template('error.html', error_message='CSVファイルの読み込みに失敗しました')
        sheets_data.append({
            'sheet_name': 'Sheet1',
            'header': df.columns.tolist(),
            'record': df.values.tolist()
        })
        app.logger.debug('CSVファイルの処理が完了しました')
    else:
        app.logger.error('サポートされていないファイル形式です')
        return render_template('error.html', error_message='サポートされていないファイル形式です')

    app.logger.debug(f'シートデータの数: {len(sheets_data)}')
    return render_template('preview.html', sheets_data=sheets_data)

if __name__ == '__main__':
    app.run(debug=True)