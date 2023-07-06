import os
from unittest import TestCase
from hamcrest import assert_that, contains_string
from switcheroo.publisher.key_publisher import LocalPublisher
from switcheroo import paths


class LocalPublisherTests(TestCase):

    """Tests for local publisher class"""

    def test_local_publish(self):
        """Test for local publisher"""
        host = "ExampleServer"
        user_id = "1234567"
        localpub = LocalPublisher(host, user_id)
        public_key = localpub.publish_new_key()
        public_key_path = paths.local_public_key_loc(host, user_id, None)
        private_key_path = paths.local_private_key_loc(host, user_id, None)
        with open(public_key_path, encoding="utf-8") as public_key_file:
            file_contents = public_key_file.read()
            assert_that(file_contents, contains_string(public_key))
        os.remove(public_key_path)
        os.remove(private_key_path)