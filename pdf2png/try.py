import tkinter as tk
from tkinter import filedialog, ttk
from pdf2image import convert_from_path
import os

def select_pdf():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_path:
        output_dir = filedialog.askdirectory(title="選擇存檔資料夾")
        if output_dir:
            convert_pdf_to_png(pdf_path, output_dir)

def convert_pdf_to_png(pdf_path, output_dir):
    # 高解析度轉換（dpi 設置越高，畫質越高）
    images = convert_from_path(pdf_path, dpi=300)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # 設定進度條的最大值
    progress_bar["maximum"] = len(images)
    progress_bar["value"] = 0  # 重設進度條
    
    for i, image in enumerate(images):
        # 使用 PIL 圖片庫儲存為 PNG 格式
        image.save(os.path.join(output_dir, f"{pdf_name}_page_{i+1}.png"), "PNG")
        progress_bar["value"] = i + 1  # 更新進度條
        root.update_idletasks()  # 更新 UI 以反映進度條的變動

    print("PDF 已成功轉為高畫質 PNG 圖片！")

# 建立 tkinter 介面
root = tk.Tk()
root.title("PDF 轉 PNG")
root.geometry("300x150")

# 增加按鈕
select_button = tk.Button(root, text="選擇 PDF 檔案", command=select_pdf)
select_button.pack(pady=10)

# 增加進度條
progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress_bar.pack(pady=10)

# 啟動介面
root.mainloop()
