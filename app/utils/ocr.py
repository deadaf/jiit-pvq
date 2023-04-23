from PIL import Image, ImageFilter
from .converters import to_async
from pdf2image import convert_from_path
import typing as T
import pytesseract
import re

CONFIG = "--oem 3 --psm 12"
LANG = "eng"


class ExamPDF:
    def __init__(self, pdf_name: str) -> None:
        self.pdf_name = pdf_name
        self.images: T.List[Image.Image] = []

    async def pdf_to_image(self):
        images = convert_from_path(self.pdf_name)
        for image in images:
            self.images.append(image.convert("L").filter(ImageFilter.SHARPEN))

    @to_async()
    def image_to_text(self):
        text = ""
        for image in self.images:
            w, h = image.size
            image = image.resize((w * 5, h * 5)).filter(ImageFilter.SHARPEN)

            try:
                text += pytesseract.image_to_string(
                    image, lang=LANG, config=CONFIG
                )  # noqa = E501
            except pytesseract.TesseractError:
                continue

        return text

    @staticmethod
    def count_co(text: str, co: str):
        count = 0
        for _ in text.split("\n"):
            if co in _:
                count += 1
        return count

    @staticmethod
    async def analyse_cos(texts: T.List[str]):
        for t in texts:
            print(t)
            for _ in t.split("\n"):
                _ = _.lower()
                regex = re.compile("^co[a-z0-9]{1}\s?$")
                print(_)
                if regex.match(_[:3]):
                    print(_)
                    # co_num = _[:3].strip().replace("/n", "")
                    # co_count = ExamPDF.count_co(t, co)
                    # print(f"{co_num} {co} {co_count}")
