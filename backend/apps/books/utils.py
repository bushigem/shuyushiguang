import pandas as pd
from .models import Book, Category, Location

def import_books_from_excel(file):
    try:
        df = pd.read_excel(file)
        total = len(df)
        success_count = 0
        fail_count = 0
        errors = []

        for index, row in df.iterrows():
            try:
                # 获取或创建分类
                category, _ = Category.objects.get_or_create(
                    name=row['category']
                )
                
                # 获取或创建位置
                location, _ = Location.objects.get_or_create(
                    name=row['location']
                )
                
                # 创建图书记录
                Book.objects.create(
                    title=row['title'],
                    isbn=row['isbn'],
                    author=row['author'],
                    publisher=row['publisher'],
                    category=category,
                    location=location,
                    status='available'
                )
                success_count += 1
            except Exception as e:
                fail_count += 1
                errors.append(f"第 {index + 2} 行导入失败: {str(e)}")
        
        return {
            'success': fail_count == 0,
            'total': total,
            'success_count': success_count,
            'fail_count': fail_count,
            'errors': errors
        }
    except Exception as e:
        return {
            'success': False,
            'total': 0,
            'success_count': 0,
            'fail_count': 0,
            'errors': [f"文件处理失败: {str(e)}"]
        }