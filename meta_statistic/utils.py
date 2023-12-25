import os
import requests
from dotenv import load_dotenv
from instaloader import Profile, Instaloader
import urllib.request

from meta_statistic.settings import MEDIA_ROOT

load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

load = Instaloader()
# load.context.login(USER, PASSWORD)


def get_profile_photo(profile_name: str) -> str:
    profile = Profile.from_username(load.context, profile_name)
    profile_data = profile.profile_pic_url
    return profile_data


def get_profile_followers(profile_name: str) -> int:
    profile = Profile.from_username(load.context, profile_name)
    profile_data = profile.followers
    return profile_data


def get_save_profile_pictures(profile_name: str) -> str:
    profile = Profile.from_username(load.context, profile_name)
    url = profile.profile_pic_url
    filename = f"{profile.username}.jpg"
    destination_folder = os.path.join(MEDIA_ROOT, 'influencers', 'profile_images')
    os.makedirs(destination_folder, exist_ok=True)
    full_path = os.path.join(destination_folder, filename)
    urllib.request.urlretrieve(url, filename=full_path)
    return "\\".join(full_path.split("\\")[5::])




# profile = Profile.from_username(load.context, USERNAME)
# file_path = "C:\\meta_statistic\\app\\meta_statistic\\media\\1.jpg"
# # Создать директорию, если она не существует
# directory = os.path.dirname(file_path)
# os.makedirs(directory, exist_ok=True)
#
# print(profile)
# print(profile.followers)
# img_url = profile.profile_pic_url
# print(img_url)

# # Скачать изображение
# response = requests.get(img_url)
# with open(file_path, 'wb') as file:
#     file.write(response.content)


