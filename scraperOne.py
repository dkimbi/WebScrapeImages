import io
import time
from selenium.webdriver.common.by import By
import requests
from selenium import webdriver
from PIL import Image

PATH = "C:\Program Files (x86)\seleniumWebdrivers\chromedriver.exe"

wd = webdriver.Chrome(PATH)


def get_images_from_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = "https://www.google.com/search?q=hill&rlz=1C1GCEU_enUS901US901&hl=en&sxsrf=AOaemvJCPISgqqNe3HKhqnSyS-l-lD8Mtw:1635522359066&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiNre_J--_zAhUboHIEHYVSBVkQ_AUoAXoECAEQAw&biw=1073&bih=1312&dpr=1"
    wd.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        # TODO: clicking right image? correct class name?

        for img in thumbnails[len(image_urls): max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")

    return image_urls


def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Saved!")
    except Exception as e:
        print('Failed -', e)


# download_image("", image_url, "testing.jpg")

urls = get_images_from_google(wd, 2, 5)

for i, url in enumerate(urls):
    download_image("imagesDir/", url, str(i) + ".jpg")

wd.quit()
