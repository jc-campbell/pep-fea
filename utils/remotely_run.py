import subprocess
import shlex


def copy_directory_to_server(local_dir, remote_user, remote_host, remote_dir):
    """
    Copies a local directory to a remote server using scp.
    """
    command = f"scp -r {local_dir} {remote_user}@{remote_host}:{remote_dir}"
    print(f"Copying {local_dir} to {remote_user}@{remote_host}:{remote_dir}")
    subprocess.run(shlex.split(command), check=True)


def run_commands_on_server(remote_user, remote_host, commands):
    """
    Runs a list of commands on a remote server via SSH, waiting for each to complete.
    """
    for cmd in commands:
        # Build the SSH command
        full_command = f"ssh {remote_user}@{remote_host} {shlex.quote(cmd)}"
        print(f"Executing remote command: {cmd}")
        subprocess.run(full_command, shell=True, check=True)


def copy_directory_from_server(remote_user, remote_host, remote_dir, local_dir):
    """
    Copies a directory from a remote server to the local machine using scp.
    """
    command = f"scp -r {remote_user}@{remote_host}:{remote_dir} {local_dir}"
    print(f"Copying {remote_user}@{remote_host}:{remote_dir} to {local_dir}")
    subprocess.run(shlex.split(command), check=True)


if __name__ == "__main__":
    # Configuration parameters
    local_dir = "/path/to/local/directory"         # Directory on your laptop
    # Destination directory on the server
    remote_dir = "/path/to/remote/directory"
    # Your SSH username on the server
    remote_user = "username"
    # The server's address (hostname or IP)
    remote_host = "server.address"

    # List of commands to run on the server. Adjust these as needed.
    commands = [
        "cd /path/to/remote/directory && ./run_computation.sh",
        # Add more commands here if needed
    ]

    try:
        # Copy the local directory to the server
        copy_directory_to_server(
            local_dir, remote_user, remote_host, remote_dir)

        # Run the required commands on the server
        run_commands_on_server(remote_user, remote_host, commands)

        # Retrieve the modified directory from the server
        # This copies to a new directory on your laptop (e.g., local_dir_modified)
        target_local_dir = local_dir + "_modified"
        copy_directory_from_server(
            remote_user, remote_host, remote_dir, target_local_dir)

        print("Operations completed successfully.")
    except subprocess.CalledProcessError as e:
        print("An error occurred during remote operations:")
        print(e)
