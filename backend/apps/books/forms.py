from django import forms

class BookImportForm(forms.Form):
    csv_file = forms.FileField(label='上传CSV文件')

    def save(self):
        # 解析CSV文件并保存到数据库
        pass