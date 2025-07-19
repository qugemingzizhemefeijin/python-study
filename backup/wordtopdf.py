import os
import sys
from datetime import datetime

import win32com.client


# pip install pywin32
# win32com.client：用来操作 Word 应用（需要 Windows 系统+装了 Office）
# 或者跨平台一点的玩法，用 LibreOffice + subprocess，不过今天我们先来讲讲最稳最简单的方式：用 Word 本尊来干活
def word_to_pdf(input_path, output_path):
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False  # 不弹窗，后台运行
    doc = word.Documents.Open(input_path)
    doc.SaveAs(output_path, FileFormat=17)  # 17 是 PDF 格式
    doc.Close()
    word.Quit()


# 1. 系统必须是 Windows，而且得装了 MS Office (这玩意底层其实就是用 COM 调用了 Word 的功能，所以没有装 Word 是用不了的)
# 2. 文档里有宏的、被保护的，可能转不了 (有些文档打开会弹窗提示宏或者密码，那个得手动改设置，程序跑不过去)
# 3. 文件名不要太长、路径不要有中文/空格 (文件名不要太长、路径不要有中文/空格)
def batch_convert(folder_path):
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False

    for file in os.listdir(folder_path):
        if file.endswith(".doc") or file.endswith(".docx"):
            doc_path = os.path.join(folder_path, file)
            pdf_path = os.path.splitext(doc_path)[0] + ".pdf"
            try:
                doc = word.Documents.Open(doc_path)
                doc.SaveAs(pdf_path, FileFormat=17)
                doc.Close()
                print(f"✅ 转换成功：{file}")
            except Exception as e:
                print(f"❌ 转换失败：{file}，原因：{e}")

    word.Quit()


def get_real_path():
    """兼容开发与打包环境的路径获取"""
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)  # EXE文件所在目录[1,7](@ref)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    return base_dir


# 生成时间戳文件夹
def gen_output_folder(folder):
    # folder = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = os.path.join(folder, f"pdf_{timestamp}")
    os.makedirs(output_folder, exist_ok=True)
    return output_folder


# 自动获取当前脚本目录下的 Word 文件
def get_word_files_from_current_folder(folder):
    # folder = os.path.dirname(os.path.abspath(__file__))
    word_files = []
    for file in os.listdir(folder):
        if file.endswith(".doc") or file.endswith(".docx"):
            word_files.append(os.path.join(folder, file))
    return word_files


# 检测 Office 和 WPS 的方法
def detect_office_or_wps():
    try:
        word = win32com.client.gencache.EnsureDispatch("Word.Application")
        return "office"
    except:
        try:
            wps = win32com.client.gencache.EnsureDispatch("Kwps.Application")
            return "wps"
        except:
            return None


# 自动选择引擎并批量转换
def convert_word_to_pdf_auto(input_path, output_path, engine):
    if engine == "office":
        app = win32com.client.Dispatch("Word.Application")
    elif engine == "wps":
        app = win32com.client.Dispatch("Kwps.Application")
    else:
        print("没有检测到可用的 Office 或 WPS")
        return

    # 设置可见性（默认不可见）
    app.Visible = False

    try:
        doc = app.Documents.Open(input_path)
        doc.SaveAs(output_path, FileFormat=17)
        doc.Close()
        print(f"转换成功：{input_path}")
    except Exception as e:
        print(f"转换失败：{input_path}，原因：{e}")

    try:
        app.Quit()
    except:
        print("当前环境不支持 Quit，跳过退出。")


# 主函数
def batch_convert_here():
    engine = detect_office_or_wps()
    if not engine:
        print("系统里没有安装 Office 或 WPS，没法转换")
        return

    folder = get_real_path()
    word_files = get_word_files_from_current_folder(folder)

    if not word_files:
        print("当前文件夹没有发现 Word 文件")
        return

    output_folder = gen_output_folder(folder)

    for word_file in word_files:
        filename = os.path.splitext(os.path.basename(word_file))[0]
        pdf_path = os.path.join(output_folder, f"{filename}.pdf")
        convert_word_to_pdf_auto(word_file, pdf_path, engine)

    print("所有文件转换完成啦！PDF 都在 'output_folder' 文件夹里")


# 示例用法
word_to_pdf("C:/发票.docx", "C:/发票.pdf")

# batch_convert(r"C:\Users\你的用户名\Desktop\word文件夹")

# 做成 EXE 给小白用户用（pyinstaller）
# pyinstaller -F word2pdf.py
# 生成的 dist/word2pdf.exe 就是可执行文件（系统要有 Word）。

if __name__ == "__main__":
    try:
        batch_convert_here()
        print("按 Enter 键退出...")
        input()  # 等待用户按 Enter 键
    except Exception as e:
        print(e)
        print("程序运行错误，按 Enter 键退出...")
        input()  # 等待用户按 Enter 键
