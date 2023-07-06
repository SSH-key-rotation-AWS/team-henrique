"Tests the server with keys stored locally"
from io import StringIO
import socket
from getpass import getuser
from unittest import IsolatedAsyncioTestCase
from hamcrest import assert_that, has_item, contains_string
from paramiko.client import SSHClient, AutoAddPolicy
from paramiko import RSAKey
from switcheroo.server.server import Server
from switcheroo.server.data_stores import FileSystemDataStore
from switcheroo.custom_keygen import KeyGen
from switcheroo import paths


class TestServerLocal(IsolatedAsyncioTestCase):
    "Test server with local keys"

    async def test_retrieve_public_keys_locally(self):
        data_store = FileSystemDataStore(temp=True)
        async with Server(data_store=data_store) as server:
            server: Server = server
            host = socket.getfqdn()
            random_host_dir = paths.local_key_dir(host, getuser(), data_store.home_dir)
            private_key, _ = KeyGen.generate_private_public_key_in_file(random_host_dir)
            key: RSAKey = RSAKey.from_private_key(StringIO(private_key.decode()))
            key_fingerprint = key.fingerprint  # type: ignore
            client = SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(
                "127.0.0.1",
                port=server.port,
                pkey=key,
            )
            logs = await server.logs
            assert_that(logs, has_item(contains_string(key_fingerprint)))
