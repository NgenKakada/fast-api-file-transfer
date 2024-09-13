import paramiko

class SFTPClient:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.sftp = None
        self.transport = None

    def connect(self):
        try:
            self.transport = paramiko.Transport((self.host, 22))
            self.transport.connect(username=self.username, password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        except paramiko.SSHException as e:
            raise ConnectionError(f"Failed to connect to {self.host}. Error: {str(e)}")

    def disconnect(self):
        try:
            if self.sftp:
                self.sftp.close()
            if self.transport:
                self.transport.close()
        except Exception as e:
            raise ConnectionError(f"Error during disconnect: {str(e)}")

    def get(self, remote_file_path, local_file_path):
        try:
            self.sftp.get(remote_file_path, local_file_path)
        except Exception as e:
            raise FileNotFoundError(f"Failed to download {remote_file_path}. Error: {str(e)}")

    def put(self, local_file_path, remote_file_path):
        try:
            self.sftp.put(local_file_path, remote_file_path)
        except Exception as e:
            raise FileNotFoundError(f"Failed to upload {local_file_path}. Error: {str(e)}")

    def listdir(self, path):
        """
        List all files in the given directory.
        """
        try:
            return self.sftp.listdir(path)
        except Exception as e:
            raise FileNotFoundError(f"Failed to list directory {path}. Error: {str(e)}")

    def stat(self, path):
        """
        Get file statistics (e.g., creation time) for a specific file.
        """
        try:
            return self.sftp.stat(path)
        except Exception as e:
            raise FileNotFoundError(f"Failed to get file stats for {path}. Error: {str(e)}")
