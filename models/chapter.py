from dataclasses import dataclass
import typing as tp
import urllib.request
import os
import os.path
import ssl
import requests
import threading

requests.packages.urllib3.disable_warnings()

unverified = ssl._create_unverified_context
ssl._create_default_https_context = unverified


@dataclass
class Chapter:

    number: tp.Union[int, str]
    images: tp.List[str]
    name: str

    def save(self, path: str) -> None:
        i = 1

        if not os.path.exists(os.path.join(path, self.number)):
            os.mkdir(os.path.join(path, self.number))

        def save_image(image):
            resource =  urllib.request.urlopen(image)
            save_path = None
            save_path = os.path.join(path, self.number, f'{i}.jpg')

            with open(save_path, 'wb') as OUTPUT_FILE:
                OUTPUT_FILE.write(resource.read())

        threads = []

        for image in self.images:
            thr = threading.Thread(target=save_image, args=(image,))
            threads.append(thr)
            thr.start()
            thr.join()
            i += 1
        
