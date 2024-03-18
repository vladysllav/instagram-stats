import os
from pathlib import Path
from typing import Any

from django.conf import settings
from dotenv import load_dotenv
import urllib.request

from instagrapi.exceptions import LoginRequired

from meta_statistic.settings import MEDIA_ROOT
from instagrapi import Client
load_dotenv()


class ProfileClient:
    """
    Class for working with the Instagram API.
    """
    def __init__(self):
        self.session_file = Path(settings.BASE_DIR) / 'instagram_session.json'  # Path to store session data
        self.client = Client()
        self.load_or_create_session()
        self.profile_cache = {}

    def load_or_create_session(self):
        """
        Load existing session or create a new one.
        """
        if os.path.exists(self.session_file):
            self.client.load_settings(self.session_file)
        else:
            self.create_new_session()

    def create_new_session(self):
        """
        Create a new session and save it.
        """
        username = os.getenv("ACCOUNT_USERNAME")
        password = os.getenv("ACCOUNT_PASSWORD")
        self.client.login(username, password, relogin=True)
        self.client.dump_settings(self.session_file)

    def user_info_by_username(self, profile_name) -> Any:
        """
        Get user info by username.
        :param profile_name: The name of the profile whose information you want to find
        :return: User info
        """
        try:
            return self.client.user_info_by_username_v1(profile_name)
        except LoginRequired:
            self.create_new_session()

    def get_profile_photo(self, profile_name) -> str:
        """s
        Get profile photo by username.
        :param profile_name: The name of the profile whose information you want to find
        :return: url to profile photo
        """
        profile = self.user_info_by_username(profile_name)
        return profile.profile_pic_url_hd

    def get_profile_followers(self, profile_name) -> int:
        """
        Get profile followers by username.
        :param profile_name: The name of the profile whose information you want to find
        :return: count of profile followers
        """
        profile = self.user_info_by_username(profile_name)
        return profile.follower_count

    def get_save_profile_pictures(self, profile_name) -> str:
        """
        Get profile photo by username and save it to the media folder.
        :param profile_name: The name of the profile whose information you want to find
        :return: url to profile photo in media folder absolute path
        """
        profile = self.user_info_by_username(profile_name)
        url = str(profile.profile_pic_url)
        filename = f"{profile.username}.jpg"
        destination_folder = os.path.join(settings.MEDIA_ROOT, 'influencers', 'profile_images')
        os.makedirs(destination_folder, exist_ok=True)
        full_path = os.path.join(destination_folder, filename)
        urllib.request.urlretrieve(url, filename=full_path)

        relative_path = os.path.relpath(full_path, settings.MEDIA_ROOT)

        return relative_path.replace(os.path.sep, '/')


client = ProfileClient()
