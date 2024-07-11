import os

def rename_images_in_folder(folder_path):
    # پشتیبانی از فرمت‌های مختلف تصویر
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

    # لیست تمام فایل‌های موجود در پوشه
    files = os.listdir(folder_path)

    for file_name in files:
        # بررسی فرمت فایل‌ها برای اطمینان از اینکه فایل یک تصویر است
        if any(file_name.lower().endswith(ext) for ext in image_extensions):
            new_file_name = file_name.replace('20%', '')
            # مسیر کامل فایل‌های قدیمی و جدید
            old_file_path = os.path.join(folder_path, file_name)
            new_file_path = os.path.join(folder_path, new_file_name)
            
            # تغییر نام فایل
            os.rename(old_file_path, new_file_path)
            print(f'Renamed: {file_name} -> {new_file_name}')

# فراخوانی تابع برای پوشه جاری
if __name__ == "__main__":
    folder_path = os.getcwd()  # استفاده از پوشه جاری
    rename_images_in_folder(folder_path)
