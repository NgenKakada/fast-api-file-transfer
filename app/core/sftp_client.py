import paramiko

class SFTPClient:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.sftp = None
        self.transport = None

    def connect(self):
        self.transport = paramiko.Transport((self.host, 22))
        self.transport.connect(username=self.username, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def disconnect(self):
        if self.sftp:
            self.sftp.close()
        if self.transport:
            self.transport.close()

    def get(self, remote_file_path, local_file_path):
        self.sftp.get(remote_file_path, local_file_path)

    def put(self, local_file_path, remote_file_path):
        self.sftp.put(local_file_path, remote_file_path)
